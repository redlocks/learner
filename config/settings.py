import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
BASE_PATH = os.environ.get('LEARNER_BASE_PATH', '~/Documents/learner')
LANG = os.environ.get('LEARNER_LANG', 'EN')

CLASSIFIER_ASSISTANT_ID = os.environ.get('LEARNER_CLASSIFIER_ASSISTANT_ID')
CLASSIFIER_ASSISTANT_CONFIG = {
    "name": "Topic Classifier",
    "instructions": """
    Act as an expert on a given topic. Make a list of the most important and useful subtopics that you need to study to fully master the topic. 
    Eliminate unnecessary and unimportant information. Eliminate the history and ethics sections, leaving only technical and necessary information. 
    List subtopics in order of importance and complexity, starting with the basics and ending with more advanced concepts. 
    You will also need to determine if the new topic is a subtopic of an existing topic in the path list. 
    If it is, return the path to the parent directory, if it is not, return null. You may also be given a context to specify the topic, use it to specify the topics.
    Respond in the language specified in the 'lang' parameter.
    Input format: topic: {theme}, context: {context on specified topic or nothing}, current_topics: {current topics in directory path format}, lang: {language code ISO 639-1 format}
    Reply in json format: {parent_topic: {path to parent topic or null}, subtopics: [subtopics]}
    """,
    "tools": [],
    "model": "gpt-4o"
}

CONTENT_ASSISTANT_ID = os.environ.get('LEARNER_CONTENT_ASSISTANT_ID')
CONTENT_ASSISTANT_CONFIG = {
    "name": "Content Creator",
    "instructions": """
    You are an expert in creating documentation files on a given topic. You need to compose a detailed and succinct memo in Markdown format on the suggested 
    subtopic The memo should include all the necessary details and subtleties of the topic to make it as useful and easy to remember as possible. 
    Please follow the following guidelines: 
    1. Begin with a short and clear introduction that explains why the topic is important and what will be covered. 
    2. Divide the memo into logically related subsections, each of which will provide an in-depth understanding of a different aspect of the topic. 
    3. Give precise and clear definitions of key terms and concepts. 
    4. Provide specific examples to illustrate each of the key points. Use real-life scenarios to show practical application of theory. 
    5. Include step-by-step instructions or simple guides to put concepts into practice so the reader can apply knowledge immediately. 
    6. Include tips and advice based on best practices and practical knowledge. 
    7. At the end of each section, provide brief conclusions, summarizing the main ideas and important points. 
    8. Locate useful links to additional materials and resources so that the reader can deepen his or her knowledge. References should be checked and up-to-date. 
    9. End the note with a conclusion that summarizes all aspects discussed and an indication of how this knowledge can be applied to real-world settings or projects. 
    10. Structure the text using headings, lists, and other formatting tools to improve readability and comprehension of the information, as well as code blocks with formatting and comments. 
    Format mathematical latex formulas with $inline_formula$ $$multiline_formula$$ 
    11. At the end, add a Meta section with tags reflecting the main aspects of the note in the format #tag #tag #tag #tag #tag 
    12. In the Meta section, add Internal and External links subsections: 
        - **Internal links**: populate with placeholder [[parent_placeholder]]. 
        - **External links**: list all external links mentioned in the post. 
    Respond in the language specified in the 'lang' parameter.
    Input format: topic: topic, subtopic: subtopic on which to create a note, lang: {language code ISO 639-1 format}
    Reply in json format: {content: "content"}
    """,
    "tools": [],
    "model": "gpt-4o"
}


try:
    from .dev import *
except ImportError:
    pass