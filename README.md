"# Bot Telegram Did the rocket launch yet?" 
## Table of Contents
1. [Información General](#general-info)
2. [Tecnologías](#technologies)
3. [Installatión](#installation)
4. [FAQs](#faqs)
### General Info
***
Bot de Telegram que predice el momento exacto de despegue de un Cohete con la confirmacion (Si/No) del usuario en menos de 16 preguntas y con menos de 200 lineas de código operativo.
Bot realizado con requests y python-telegram-bot
### Screenshot
![Image text](https://i.ibb.co/ZNccqW2/imagen-incial.png)
![Image text](https://i.ibb.co/qpd0ZFg/imagen-segunda.png)
![Image text](https://i.ibb.co/z5XY3Ln/imagen-tercera.png)
## Technologies
***
A list of technologies used within the project:
* [Python](https://www.python.org/): 3.9.13 
* [pyton-telegram-bot](https://python-telegram-bot.org/): 13.15
* [requests](https://requests.readthedocs.io/en/latest/): 2.28.1
## Installation
***
Forma de instalacion Local 
```
$ git clone https://github.com/mario-barrientos-dev/bot-telegram.git
$ pip install -r requirements.txt
$ python3 bot.py

```

## FAQs
***

1. La respuesta ('/start') Inicia la conversación
2. La respuesta ('/ready') Inicia el cuestionario
3. La respuesta ('/no') Acorta la muestra desde momento inicial al sugerido por el usuario.
4. La respuesta ('/si') Acorta la muestra desde momento final al sugerido por el usuario.
4. La respuesta ('/calcular') Opera y arroja el frame aproximado.
