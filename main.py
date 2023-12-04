import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Se carga la variable dentro del .env que contiene el token
openai.api_key=os.getenv('API_KEY')

# Funcion a ejecutar si el input esta relacionado a detalles de la deuda
def detalle_deuda():
    """
    proporciona el detalle de la deuda de un usuario mediante un formato predefinido entre triple comillas dobles
    
    """
    prompt = f"""DETALLE DE LA DEUDA VENCIDA
    Querido/a cliente/a con el siguiente: {input_user} 
    Tiene una deuda por pagar del siguiente monto $10.000. 
    Vencida el 30/11 
    Servicio contratado en AV. Huerfanos 1111. 
    """

    """
    Los datos recolectados se delimitarán por comillas triples invertidas.

    """
    return prompt

def solicitar_recibo():
    """
    Obtener el recibo.

    A continuación, regresa la siguiente información entre comillas triples dobles:
    
    """
    
    prompt = f"""SOLICITAR RECIBO
    Obten tu recibo con solo unos clics https://mirecibo.mosvistar.com.pe/
    """
    
    """

    Los datos recolectados se delimitarán por comillas triples invertidas.

    """
    return prompt

def formas_lugar_pago():
    """
    Proporcionar formas y lugares de pago para el usuario.

    A continuación, regresa la siguiente información entre comillas triples dobles:
    
    """

    prompt = f"""FORMAS Y LUGARES DE PAGO 
    En Movistar te brindamos diversas formas de pago SIN COMISION. Puedes pagar por yape: https://innovacxion.page.link/mVFa
    Desde la web o app de tu banco. 
    Conoce todos los canales de pago en el siguiente link: https://www.movistar.com.pe/atencion-al-cliente/lugares-y-medios-de-pago 
    """

    """

    Los datos recolectados se delimitarán por comillas triples invertidas.

    """
    return prompt

def despedir_resumen():
    """
    Despedirte y agradecer por ser parte de movistar.
    
    A continuación, regresa el siguiente mensaje que esta dentro de las comillas triples dobles:
    
    """
    
    prompt = f"""
    Gracias por preferir Movistar, Esperemos que siga con nosotros, que tenga un buen resto del día.
    """
    
    """

    Los datos recolectados se delimitarán por comillas triples invertidas.

    """
    return prompt


# Una funcion que contiene las herramientas que se utilizaran.
def get_completion_from_messages(messages):
    tools = [
        {
            "type": "function",
                    "function": {
                        # Nombre de la funcion
                        "name": "detalle_deuda",
                        # Breve resumen de lo que hace la funcion
                        "description": "Entregas los detalles de la deuda del usuario.",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                        }
                    },      
        },
        {
            "type": "function",
                    "function": {
                        "name": "solicitar_recibo",
                        "description": "entrega un mensaje predeterminado indicando como solicitar el recibo.",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                        }
                    },
        },
        {
            "type": "function",
                    "function": {
                        "name": "formas_lugar_pago",
                        "description": "entrega un mensaje predeterminado de las formas y lugares que puede pagar.",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                        }
                    },
        },
        {
                    "type": "function",
                    "function": {
                        "name": "despedir_resumen",
                        "description": "Genera una respuesta de despedida junto con un resumen de la conversación.",
                        "parameters": {
                            "type": "object",
                            "properties": {},
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
    response_message = response.choices[0].message
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
        
    #return second_response.choices[0].message.content  # Return para el second_response 
    #else:
    #    return response_message.content # Return si no hay function calls


