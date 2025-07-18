import os
import django
from openai import OpenAI
from django.conf import settings
import google.generativeai as genai

#Openai Api
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

#client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
client = OpenAI(api_key=settings.OPENAI_API_KEY)

chat_completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "user", "content": "Hola, ¿cómo estás?"}
    ]
)
#print(chat_completion.choices[0].message.content)


#Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')
prompt = "Explicame la teoría de la relatividad de Einstein en menos de 50 palabras, versión Gen Z."
respuesta = model.generate_content(prompt)

# Imprimir la respuesta
print("Gemini responde:\n")
print(respuesta.text)

