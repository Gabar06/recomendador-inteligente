from openai import OpenAI
from .models import Libro
import json
import os
from django.conf import settings
import google.generativeai as genai
import tiktoken

# Instancia del cliente Gemini con tu API Key
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')

# Instancia del cliente OpenAI con tu API Key
client = OpenAI(api_key=settings.OPENAI_API_KEY)

texto=""
respuestas=""

##############
libro = Libro.objects.values('titulo')
    
    
###############
TEXTO_ORIGINAL = """
El hombre viejo deposito unas flores ante una tumba, susurro un padrenuestro entre dientes, extrajo un pañuelo del bolsillo y lustro cuidadosamente la litografia de su finada esposa, que parecia mirarlo tristemente desde la pared del panteon. Cumplido el rito camino por la funebre avenida rumbo a la salida. Le llamo la atencion una señora vieja que, frente a una suntuosa tumba, hacia lo que no debia hacerse ante ninguna tumba, suntuosa o humilde: maldecia.
-¿Puedo ayudarle en algo, señora?
-Si, vaya y consiga con el Intendente una resolucion que prohiba hacer caca en este santo lugar.
-No me diga que usted...
-No la hice yo. ¡La pise, señor mio!
Se habia sentado y con infinito asco y esfuerzos musculares olvidados trataba de sacarse el zapato mancillado por la humana miseria.
-¿Me permite...?
El señor viejo ayudo galantemente a la señora vieja a despejarse del zapato, y se puso a limpiarlo cuidadosamente contra el cesped que habia invadido una losa olvidada.
-Es usted muy gentil, señor.
-Jamas paso de largo ante una dama en apuros -dijo el señor viejo-. Parece que el zapato ya esta limpio, aunque todavia huele.
-Gracias -dijo la señora vieja y se calzo el zapato.
"""

PROMPT_BASE = """
Corrige y analiza las palabras ingresadas por el usuario. Para cada fila, devuelve si la palabra con acentuación incorrecta fue una palabra incorrecta, si la corrección y la clase de acento es correcta.

Texto original:
{texto}

Respuestas del usuario:
{respuestas}

Luego indica:
- Cuantas palabras incorrectas fueron identificadas en total de todas las palabras incorrectas del texto.
- Cuáles palabras están bien.
- Cuáles están mal.
- De qué tipo de clasificación de palabras cometió más errores (agudas, graves, etc).
- En qué categoría tuvo menos errores.
- Recomienda un capítulo del libro de los siguientes títulos {libro}  donde se explique más ese tipo de palabras.
- Si todas están bien, felicítalo.

También da el texto corregido con las palabras modificadas en negrita.
 Devuélveme la tabla de resultados y la recomendación
en HTML puro, sin bloques de código, sin etiquetas <html>, <head> ni <body>, solo el contenido
para mostrar dentro de un <div>. No escribas nada fuera de ese HTML.

"""


def analizar_respuestas(json_usuario):
    try:
        respuesta = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "Eres un experto en ortografía que evalúa ejercicios"},
                {"role": "user", "content": PROMPT_BASE.format(texto=TEXTO_ORIGINAL, respuestas=json_usuario, libro=libro )}
            ],
            #verbosity="medium",           # Nuevo parámetro
            #reasoning_effort="minimal",   # Nuevo parámetro
            #max_completion_tokens=200
        )
        #tokenizer=tiktoken.endcoding_for_model("gpt-5")
        #tokens=tokenizer.encode(PROMPT_BASE.format(texto=TEXTO_ORIGINAL, respuestas=json_usuario, libro=libro ))
        #print("La cantidad de tokens es: ",tokens)
        return respuesta.choices[0].message.content
    except Exception as e:
        return f"Error al analizar: {str(e)}"

def gemini_chat(prompt):
    response = model.generate_content(PROMPT_BASE.format(texto=TEXTO_ORIGINAL, respuestas=prompt, libro=libro))
    return response.text  # Puede variar si pides otra cosa que texto


#######################
#Ejercicio1 Acentuación

