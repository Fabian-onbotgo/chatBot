# CHATBOT MOVISTAR

Asistente virtual diseñado para proporcionar información sobre un servicio telefónico mediante la inteligencia artificial de OpenAI.

## Primeros pasos

1. Se recomienda trabajar en un entorno virtual. Para ello, utiliza el siguiente comando desde tu consola:

    ```bash
    python -m venv venv
    ```

2. ¿Ya tienes tu entorno virtual? ¡Perfecto! Ahora solo falta activarlo. Utiliza uno de los siguientes comandos:

    #### Forma 1
    ```bash
    source c:/ruta/de/carpeta/python/venv/Scripts/activate
    ```

    #### Forma 2
    Desde VSCode, sigue estos pasos:
    ```
    CTRL + SHIFT + P
    Python: Select Interpreter
    ⭐​Python 3.12.0 ('venv': venv) Recommended
    ```

3. A continuación, realiza la instalación de las librerías para nuestro proyecto. Se proporciona un archivo `requirements.txt` que se instala de la siguiente manera:

    ```bash
    pip install -r requirements.txt
    ```

4. ¡Perfecto! Casi lo tienes. Solo falta generar un archivo `.env` para agregar el token que permitirá utilizar la aplicación:

    ```
    API_KEY='sk-token_de_openai'
    ```

    ⛔​ **Por razones de seguridad, no puedo proporcionar el token. Agradezco tu comprensión.** ⛔​

## Ahora solo queda ejecutar nuestra aplicación

1. Desde la consola, dirígete a la carpeta `chatBot` de tu proyecto:

    ```bash
    cd chatBot
    ```

2. Ejecuta la aplicación con el siguiente comando:

    ```bash
    py main.py
    ```

## 🥳 ¡Felicidades! Ya tienes todo lo necesario para interactuar con la aplicación 🥳
