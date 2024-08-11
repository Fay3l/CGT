from openai import OpenAI
import os
from dotenv import load_dotenv
import requests

load_dotenv()

# text-embedding-3-large

client = OpenAI(
  organization='org-CFNQXvAhOG0r6WSBlnFgbj78',
  project=os.getenv("PROJECT_ID"),
  api_key=os.getenv("OPENAI_KEY")
)

url = "https://chatgpt-api.shn.hk/v1/"
data = {
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "user", "content": "Hello, how are you?"}]
}
headers={'Content-Type': 'application/json'}

response = requests.post(url=url,data=data,headers=headers)

print(response)
