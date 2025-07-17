import os
import django
from openai import OpenAI
from django.conf import settings

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

print(chat_completion.choices[0].message.content)
#print(settings.OPENAI_API_KEY)