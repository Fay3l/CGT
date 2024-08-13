from mistralai import Mistral
import os
from dotenv import load_dotenv

load_dotenv()

# text-embedding-3-large

# client = OpenAI(
#   organization='org-CFNQXvAhOG0r6WSBlnFgbj78',
#   project=os.getenv("PROJECT_ID"),
#   api_key=os.getenv("OPENAI_KEY")
# )

# prompt = f"Créer un jeu 'Qui suis-je?' sur sportif connu avec 5 indices."
# response = client.completions.create(
#     model="gpt-3.5-turbo",  # Utilisez un modèle approprié pour du text embedding
#     prompt=prompt,
#     max_tokens=20
# )

# indices = response.choices[0].text.strip().split('\n')

# print(indices)
from mistralai import Mistral

api_key = os.getenv("MISTRALAPI_KEY")
model = "open-mistral-7b"

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": f"Créer un jeu 'Qui suis-je?' sur un sportif connu avec 5 indices numérotés. Donné la réponse",
        },
    ]
)
print(chat_response.choices[0].message.content)