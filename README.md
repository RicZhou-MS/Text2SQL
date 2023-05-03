# Chat to SQL

This project is made to demo Azure openAI capability (gpt-4, gpt-turbo, gpt-4-32k) for text to SQL. It can grab DB schema (table and columns) from specific SQL database for composing appropriate prompt. The streamlit GUI supports user to ask question, and then it calles GPT to return SQL statement based on DB table definition for user question. it supports multi turn conversation.
![image](https://user-images.githubusercontent.com/75886466/235889811-72df9218-b64a-467d-b89d-9c73d5346aee.png)

## Installation
1. Install Python runtime (This repo is developed with Python 3.11.2)
2. Clone the project onto your local Windows, install the python dependencies:
```
pip install -r ./requirements.txt
```
3. Create your Azure OpenAI service and get your `OPENAI_API_BASE` and `OPENAI_API_KEY`.
4. 
