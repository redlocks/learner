
# Learner

## Description

Script for automatic generation of notes on a given topic based on OpenAI API. Generates notes in md format with tags and links for use with the zettelkasten approach and Obsidian.

## Installation

```
git clone https://github.com/redlocks/learner
cd learner
pip install -r requirements.txt
```

## Usage

`python3 learner.py`
In the input box, enter the topic to be learned and the necessary context (if need)


## Configuration

The first time you run it, you need to create assistants in OpenAI `python3 learn.py --create_ass` 
The values of the assistants id will be automatically updated in the environment variables 
Then you need to set the environment variables `OPENAI_API_KEY` with your API key, `BASE_PATH` with the path to your knowledge base (by default `~/Documents/learner`) and `LEARNER_LANG` - the language of the created notes if your native language is not English. The languages supported are those currently supported by OpenAI




