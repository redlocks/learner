import os
import argparse
import subprocess
from typing import List, Dict, Any
from modules.openai_api import OpenAIClient
import config

class KnowledgeBase:
    def __init__(self):
        self.client = OpenAIClient()
        self.base_path = config.BASE_PATH
        self.existing_topics = self.get_all_existing_topics()

    def get_all_existing_topics(self) -> Dict[str, Any]:
        def build_tree(path: str) -> Dict[str, Any]:
            tree = {}
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    tree[item] = build_tree(item_path)
                else:
                    tree[item] = None  # The files are presented as None
            return tree

        return build_tree(self.base_path)

    def format_topics_for_api(self, topics=None, current_path=''):
        if topics is None:
            topics = self.existing_topics
        
        formatted_topics = []
        for key, value in topics.items():
            new_path = f"{current_path}/{key}" if current_path else key
            
            if isinstance(value, dict):
                # It's a directory
                formatted_topics.append(new_path)
                # Recursive call for nested directories
                formatted_topics.extend(self.format_topics_for_api(value, new_path))
            elif isinstance(value, list):
                # This is a directory with no subdirectories, but with files
                formatted_topics.append(new_path)
        
        return formatted_topics

    def process_topic(self, topic: str,  context: str, current_path: str = "") -> None:
        topics_structure = self.format_topics_for_api()
        print(topics_structure)
        classification = self.client.classify_topic(topic, context, topics_structure)
        print(classification)
        
        parent_topic = classification['parent_topic']

        if not parent_topic or parent_topic == "null":
            parent_topic = ""
        else:
            parent_topic = parent_topic.strip()

        topic_path = os.path.join(self.base_path, parent_topic, topic)
        
        os.makedirs(topic_path, exist_ok=True)
        print(f"Directory created: {topic_path}")

        counter = 0
        core_file = f"{topic}.md"
        core_content = []
       

        for subtopic in classification['subtopics']:
            content = self.client.create_content(topic, subtopic)
            note_filename = f"{counter}. {subtopic.split(':')[-1]}.md"

            with open(os.path.join(topic_path, note_filename), "w", encoding="utf-8") as f:
                f.write(content['content'].replace('parent_placeholder', core_file))
                print(f"File created: {os.path.join(topic_path, f'{counter}. {subtopic}')}")
                counter += 1
                core_content.append(f"[[{counter}. {subtopic}.md]]")

        with open(os.path.join(topic_path, core_file), "w", encoding="utf-8") as f:

            if parent_topic:
                core_content.append(f"**Internal links:** [[{parent_topic}]]")
            f.write('\n'.join(core_content))
            print(f"File created: {core_file}")
            counter += 1
        

    def get_existing_topics(self, path: str) -> List[str]:
        return self.existing_topics.get(path, [])

    def print_knowledge_tree(self):
        def print_tree(tree: Dict[str, Any], prefix: str = ""):
            items = list(tree.items())
            for i, (name, subtree) in enumerate(items):
                is_last = i == len(items) - 1
                print(f"{prefix}{'└── ' if is_last else '├── '}{name}")
                if isinstance(subtree, dict):
                    extension = "    " if is_last else "│   "
                    print_tree(subtree, prefix + extension)

        print("Knowelege base structure:")
        print_tree(self.existing_topics)

    def create_assistant(self, assistant_config: Dict) -> str:
        return self.client._create_assistant(assistant_config)

def main():
    kb = KnowledgeBase()

    parser = argparse.ArgumentParser(description="Knowledge Base Management")
    parser.add_argument("--create_ass", action="store_true", help="Create a new assistant")
    args = parser.parse_args()

    if args.create_ass:
        classifier_ass_id = kb.create_assistant(config.CLASSIFIER_ASSISTANT_CONFIG)
        content_ass_id = kb.create_assistant(config.CONTENT_ASSISTANT_CONFIG)

        os.environ['LEARNER_CLASSIFIER_ASSISTANT_ID'] = classifier_ass_id
        os.environ['LEARNER_CONTENT_ASSISTANT_ID'] = content_ass_id
        
        print("Environment variables LEARNER_CLASSIFIER_ASSISTANT_ID and LEARNER_CONTENT_ASSISTANT_ID have been set.")
        
        exit()
    
    # print(kb.format_topics_for_api())

    # Output the structure of the knowledge base in the form of a tree
    kb.print_knowledge_tree()
    
    topic = input("Enter a topic to create or add to the knowledge base: ").strip()
    context = input("Specify the necessary context if required: ").strip()

    kb.process_topic(topic, context)

    # subprocess.run(["obsidian"])

if __name__ == "__main__":
    main()