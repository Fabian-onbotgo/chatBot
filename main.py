import openai
from fastapi import FastAPI
import os
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
openai.api_key=os.getenv('API_KEY')

class User(BaseModel):
    id: Optional[str] = ''
    message: str

# Función para enviar mensajes al modelo y obtener la respuesta
def get_completion(prompt, model ="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(
      model=model,
      messages=messages,
      temperature=0,
    )
    return response.choices[0].messages.content

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    
    return response.choices[0].message.content

def saludar(saludo="¡Hola! Bienvenid@ al chat de movistar!"):
    return saludo  # Devuelve el saludo en lugar de imprimirlo

@app.post("/bienvenido")
def welcome_movistar(user: User):
    res = []
    messages = [
        {
            'role': 'system',
            'content': 'Eres un agente virtual de movistar y tu objetivo es dar ayuda en lo que necesiten'
        },
        {
            'role': 'user',
            'content': user.message  
        }
    ]
    # Agregar elementos impares como objetos individuales a la lista messages
    tools = [
        ###### LAS FUNCIONES DENTRO DEL TOOLS DEBEN SER FUNCIONES EXTERNAS, NO DENTRO DE LA MISMA FUNCION DE OPENAI
        {
            "type": "function",
            "function": {
                "name": "saludar",
                "description": "Tienes que imprimir el mensaje designado",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
        }
    ]
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    
    for i, valor in enumerate(res):
        role = 'user' if i % 2 == 0 else 'asistencia'
        content = str(valor[0]) if isinstance(valor, list) else str(valor)
        
        messages.append({
            'role': role,
            'content': content
        })
    
    # Se asigna el contenido del primer mensaje a la variable response_content
    # Verifica si response.choices existe, si es así toma el contenido del primer mensaje
    # En caso de estar vacío asigna una cadena vacía ""
    response_content = response.choices[0].message.content if response.choices else ""
    
    # Aquí se extrae el primer mensaje de response_content
    # Y se intenta obtener las tools calls    
    response_message = response.choices[0].message
    tools_calls = response_message.tool_calls
    
    if tools_calls:
        ##### LAS FUNCIONES DISPONIBLES, SON LAS FUNCIONES A LLAMAR DENTRO DEL TOOLS
        available_functions = {"saludar": saludar} 
        messages.append(response_message)
        
        for tool_call in tools_calls:  # Corregir el nombre de la variable (tools_calls en lugar de tool_call)
            function_name = tool_call.function.name
            function_to_call = available_functions.get(function_name)
            if function_to_call is not None:
                #### SI TIENES FUNCIONES CON PARAMETROS DE ENTRADA, NECESITAS AGREGAR UN FUNCTION_ARGS, LO ENCUENTRAS EN EL EJEMPLO DEL FUNCTION CALLING DE OPENAI
                function_response = function_to_call()
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
        )
        
        return second_response.choices[0].message.content  # Return para el second_response
        
    else:
        return response_content  # Return si no hay function calls

        
        ##### TE FALTA EL RETURN DEL IF PARA EL SECOND RESPONSE
        ##### EL SECOND RESPONSE ES LA RESPUESTA DE LOS TOOLS O FUNCTION CALLING
        
    #### TE FALTA EL ELSE QUE PERMITE RETORNAR LA RESPUESTA EN CASO DE NO ENTRAR A LOS FUNCTION CALLING


# Función para verificar el saldo del usuario
def verificar_saldo():
    # Aquí implementa la lógica para verificar el saldo
    # Si el usuario no está registrado, solicita los datos para registrarlo
    # Consulta la información de la cuenta del usuario y muestra el saldo actual
    # Responde al usuario con el saldo actual

    respuesta = "Respuesta personalizada de verificación de saldo."
    print(respuesta)

# Función para pagar una factura
def pagar_factura():
    # Aquí implementa la lógica para pagar una factura
    # Verifica si el usuario está registrado, si no, pide los datos para registrarlo
    # Solicita al usuario el ID de la factura a pagar
    # Obtiene el monto de la factura según el ID proporcionado
    # Procesa el pago y confirma al usuario
    
    respuesta = "Respuesta personalizada de pago de factura."
    print(respuesta)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
