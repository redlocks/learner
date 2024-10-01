from typing import Dict, List
from openai import OpenAI
import config
import json5

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.classifier_assistant_id = config.CLASSIFIER_ASSISTANT_ID
        self.content_assistant_id = config.CONTENT_ASSISTANT_ID

    def _create_assistant(self, assistant_config: Dict) -> str:
        assistant = self.client.beta.assistants.create(**assistant_config)
        return assistant.id

    def _run_assistant(self, assistant_id: str, prompt: str) -> Dict:
        thread = self.client.beta.threads.create()
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        if run.status == 'completed': 
        
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        else:
            print(f"Run status: {run.status}")
        return json5.loads(messages.data[0].content[0].text.value)

    def classify_topic(self, topic: str, context: str, existing_topics: str) -> Dict:
        
        prompt = f"topic: {topic}, context: {context} current_topics: {existing_topics}, lang: {config.LANG}"
        return self._run_assistant(self.classifier_assistant_id, prompt)

    def create_content(self, topic: str, subtopic: str) -> Dict:
        prompt = f"topic: {topic}, subtopic: {subtopic}, lang: {config.LANG}"
        return self._run_assistant(self.content_assistant_id, prompt)
