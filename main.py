import openai
import json
import os
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Se carga la variable dentro del .env que contiene el token
openai.api_key=os.getenv('API_KEY')

# Funcion a ejecutar si el input esta relacionado a detalles de la deuda
def detalle_deuda(message):
    prompt = f"""
    ¡Tienes una tarea! Proporcionar detalles sobre la deuda de un usuario.

    Comienza pidiendo al usuario un dato vital para reconocer al cliente: el documento de identidad del titular. Solicita el RUT numérico del titular, \
    con un formato de entre 9 y 10 caracteres, que el guión del RUT sea obligatorio.

    si la persona ingresa un mensaje diferente, vuelve a pedir el RUT de manera amable.

    A continuación, regresa la siguiente información entre comillas triples simples:

    '''DETALLE DE LA DEUDA VENCIDA
    Querido/a cliente/a con el siguiente <RUT>
    Tiene una deuda por pagar del siguiente monto $10.000. \
    Vencida el 30/11
    Servicio contratado en AV. Huerfanos 1111. \
    '''

    Luego, pregunta si el usuario necesita ayuda adicional.

    Los datos recolectados se delimitarán por comillas triples invertidas.

    Mensaje del usuario: ```{message}```
    """
    return prompt

def solicitar_recibo(message):
    return

def formas_lugar_pago(message):
    return

def despedir_resumen(message):
    return

def get_completion_from_messages(messages):
    tools = [
        {
            "type": "function",
                    "function": {
                        # Nombre de la funcion
                        "name": "detalle_deuda",
                        # Breve resumen de lo que hace la funcion
                        "description": "Se obtiene detalles específicos de la deuda consultando la \
                            base de datos a través de un mensaje proporcionado por el usuario. Requiere un mensaje \
                            válido que indique la opción del servicio de detalle de la deuda.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "Se recibe un rut y se verifica en la base de datos si esta registrado",
                                },
                            },
                            "required": ["message"],
                        }
                    },      
        },
        {
            "type": "function",
                    "function": {
                        "name": "solicitar_recibo",
                        "description": "Esta función devuelve una respuesta genérica que puede ser útil para solicitar \
                        un recibo o comprobante. Se espera un mensaje válido para procesar la solicitud correctamente.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "Se recibe un rut y se verifica en la base de datos si esta registrado",
                                },
                            },
                            "required": ["message"],
                        }
                    },
        },
        {
            "type": "function",
                    "function": {
                        "name": "formas_lugares_pago",
                        "description": " Utiliza el mensaje proporcionado para ofrecer opciones relevantes de pago y ubicaciones. \
                        Se requiere un mensaje válido para proporcionar la información adecuada.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "Se recibe un rut y se verifica en la base de datos si esta registrado",
                                },
                            },
                            "required": ["message"],
                        }
                    },
        },
        {
                    "type": "function",
                    "function": {
                        "name": "despedida_resumen",
                        "description": "Genera una respuesta de despedida junto con un resumen de la conversación.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "se recibe un mensaje relacionado con despedida y se genera una respuesta acorde",
                                },
                            },
                            "required": ["message"],
                        }
                    },
        }
    ]
    
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0,
    )
    
    # Aquí se extrae el primer mensaje de response_content
    # Y se intenta obtener las tools calls    
    response_message = response.choices[0].message
    print(response_message)
    tools_calls = response_message.tool_calls
    
    if tools_calls:
        ##### LAS FUNCIONES DISPONIBLES, SON LAS FUNCIONES A LLAMAR DENTRO DEL TOOLS
        available_functions = {
            "detalle_deuda": detalle_deuda,
            "solicitar_recibo": solicitar_recibo,
            "formas_lugar_pago": formas_lugar_pago,
            "despedir_resumen": despedir_resumen
        } 
        messages.append(response_message)
        # Itera de función en funcion hasta llegar a la que coincida con el input
        for tool_call in tools_calls:  
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                message=function_args.get("message"),
            )
            #function_response = function_to_call()
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
            
        second_response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            temperature=0
        )
        
        return second_response.choices[0].message.content  # Return para el second_response 
    else:
        return response_message.content # Return si no hay function calls

# Contexto detallado para que el rol system no tenga alucinaciones
context_sys = [
    {
        'role': 'system',
        'content': """
        Eres el servicio de chat de Movistar, dedicado a proporcionar información detallada sobre la deuda del servicio telefónico de los usuarios. \
        Tu función principal es ofrecer detalles de la deuda, información sobre formas y lugares de pago, así como la capacidad de solicitar un recibo. \
        Esperas recibir la solicitud completa por parte del usuario antes de responder y verificas si hay una conclusión a la conversación. \
        Otórgale tiempo al cliente para agregar más información si así lo desea. \
        Tu estilo de respuesta debe ser amigable, conciso y altamente conversacional, utiliza emojis que tengan logica con el texto \
        Recuerda indicarle al usuario que puede escribir la palabra "SALIR" en cualquier momento para finalizar la conversación.
        """
    }
]

# Mensaje de bienvenida al iniciar la app
response = """
¡Bienvenido al Chat de Movistar!  Estoy aquí para ayudarte. \n
Puedes pedirme información sobre: \n
-Detalles de la deuda vencida  \n
-Solicitar un recibo  \n
-Conocer formas y lugares de pago  \n
-Finalizar la conversación  (Escribe "SALIR") \n
"""

print(response)

while True:
    prompt_client = input('Cliente: ').lower()
    if prompt_client == '' or 'hola' in prompt_client:
        print(response)
    elif 'salir' not in prompt_client:
        context_sys.append({'role': 'user', 'content': prompt_client})
        response = get_completion_from_messages(context_sys)
        context_sys.append({'role': 'assistant', 'content': response})
        print(f'Assistant: {response}\n')
    else:
        break
