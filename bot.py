try:
    # 👇️ using Python 3.10+
    from collections.abc import Mapping
except ImportError:
    # 👇️ using Python 3.10-
    from collections import Mapping
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
import requests
from telegram import ChatAction
import shutil
import os
import logging
import telegram
import os
from telegram.ext import Updater
import random
import math

logging.basicConfig(
    level= logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()
logging.basicConfig(level=logging.ERROR)
#Solicitar Token
TOKEN = os.environ['TOKEN']

INPUT_NUMBER = 0

number_before = '0'
number_after = '61696' 
message_count = 0
text_init = f'Hola, \n<b>Vamos a calcular en qué momento despega el cohete!!!...</b>\n<ins><b>Fíjate con atención en la siguientes imágenes y dime si en la que eliges el cohete ha despegado o no</b></ins>\n(<i>Un pequeño consejo sería que estés atento al contador de la parte superior derecha de la pantalla (T-): aún no ha despegado, (T+): ya despegó</i>)\nTe preguntaré y contestarás un <b>SI</b> o un <b>NO</b> para ir definiedo el rango donde se encuetra la imagen del despegue, <b>TENGO MÁXIMO 16 INTENTOS PARA LOGRARLO</b>\nSi tienes un muy buen ojo y tu rango se redujo al punto de no poder avanzar, puedes pulsar <b>CALCULAR</b> para que definamos con precisión en que imagen despegó el cohete\n¿Estás listo? /ready para empezar el juego.'

# Inicializamos la conversación y respondemos con un saludo personalizado 
def start(update, context:CallbackContext):
    # Guardamos en memoria el nombre y creamos en memoria los números
    name = update.effective_user['first_name']
    context.user_data['number_before'] = '0'
    context.user_data['number_after'] = '61696'

    # Respuesta
    text_init = f'Hola {name}, \n<b>Vamos a calcular en qué momento despega el cohete!!!...</b>\n<ins><b>Fíjate con atención en la siguientes imágenes y dime si en la que eliges el cohete ha despegado o no</b></ins>\n(<i>Un pequeño consejo sería que estés atento al contador de la parte superior derecha de la pantalla (T-): aún no ha despegado, (T+): ya despegó</i>)\nTe preguntaré y contestarás un <b>SI</b> o un <b>NO</b> para ir definiedo el rango donde se encuetra la imagen del despegue, <b>TENGO MÁXIMO 16 INTENTOS PARA LOGRARLO</b>\n¿Estás listo? /ready para empezar el juego.'
    update.message.reply_text(text=text_init , parse_mode=telegram.ParseMode.HTML)
    context.user_data['text_init'] = text_init
    return INPUT_NUMBER

# Empezamos la orden 
def input_number(update, context:CallbackContext):
    number = update.message.text
    global message_count
    message_count += 1
    # Verificamos si el ingreso es un número válido y tomamos una decisión
    if number == '/no':
            if 'number_after' in context.user_data:
                number_after = context.user_data.get('number_after')
            else:
                number_after = '61696'
            
            print(message_count)
            number_before = context.user_data.get('numero')
            context.user_data['number_before'] = number_before
            bisect_number_before = str(math.floor((int(number_before)+ int(number_after))/2))
            print(bisect_number_before + " Esta entre " + number_before + " y " + number_after)
            if message_count == 17:
                resultado = str(math.floor((int(number_before)+ int(number_after))/2))
                response = requests.get('http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/' + str(resultado), stream=True)
                with open(str(resultado)+'.png', 'wb') as f:
                                response.raw.decode_content = True
                                shutil.copyfileobj(response.raw, f)
                                
                chat = update.message.chat
                send_img(f, chat)
                update.message.reply_text(f'<b>Perfecto el cohete despega en {resultado}</b>\nSi lo deseas, escribe /start para volver a empezar', parse_mode=telegram.ParseMode.HTML)
                clear_cahe(context)
                message_count = 0
                return ConversationHandler.END
            context.user_data['numero'] = bisect_number_before
            response = requests.get('http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/' + bisect_number_before, stream=True)
            with open('temporal_after.png', 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
                
            chat = update.message.chat
            send_img(f, chat)
            update.message.reply_text(f'{bisect_number_before} - <ins><b>¿El cohete ya despegó o aún no ha despegado?</b></ins>\n/yes, <b>Ya despegó</b>,\n /no, <b>Aun no ha despegado</b>Puedes reiniciar el juego con el comando /restart', parse_mode=telegram.ParseMode.HTML)
            
            return ConversationHandler.END    
    
    if number == '/yes':
            if 'number_before' in context.user_data:
                number_before = context.user_data.get('number_before')
            else:
                number_before = '0'
           
            print(message_count)
            number_after = context.user_data.get('numero')
            context.user_data['number_after'] = number_after
            bisect_number_after = str(math.floor((int(number_before)+ int(number_after))/2))
            print(bisect_number_after + " Esta entre " + number_before + " y " + number_after)
            if message_count == 16:
                resultado = str(math.floor((int(number_before)+ int(number_after))/2))
                response = requests.get('http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/' + str(resultado), stream=True)
                with open(str(resultado)+'.png', 'wb') as f:
                                response.raw.decode_content = True
                                shutil.copyfileobj(response.raw, f)
                                
                chat = update.message.chat
                send_img(f, chat)
                update.message.reply_text(f'<b>Perfecto el cohete despega en {resultado}</b>\nSi lo deseas, escribe /start para volver a empezar', parse_mode=telegram.ParseMode.HTML)
                clear_cahe(context)
                message_count = 0
                return ConversationHandler.END
            context.user_data['numero'] = bisect_number_after
            response = requests.get('http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/' + bisect_number_after, stream=True)
            with open('temporal_after.png', 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
                
            chat = update.message.chat
            send_img(f, chat)
            update.message.reply_text(f'{bisect_number_after} - <ins><b>¿El cohete ya despegó o aún no ha despegado?</b></ins>\n/yes, <b>Ya despegó</b>,\n /no, <b>Aun no ha despegado</b>Puedes reiniciar el juego con el comando /restart', parse_mode=telegram.ParseMode.HTML)
            
            return ConversationHandler.END
    
    if number == '/ready':
            bisect_number = str(int((0 + 61696)/2 -1))
            print(message_count)
            if message_count == 16:
                resultado = str(math.floor((int(number_before)+ int(number_after))/2))
                response = requests.get('http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/' + str(resultado), stream=True)
                with open(str(resultado)+'.png', 'wb') as f:
                                response.raw.decode_content = True
                                shutil.copyfileobj(response.raw, f)
                                
                chat = update.message.chat
                send_img(f, chat)
                update.message.reply_text(f'<b>Perfecto el cohete despega en {resultado}</b>\nSi lo deseas, escribe /start para volver a empezar', parse_mode=telegram.ParseMode.HTML)
                clear_cahe(context)
                message_count = 0
                return ConversationHandler.END
            context.user_data['numero'] = bisect_number
            response = requests.get('http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/' + bisect_number, stream=True)
            with open('temporal.png', 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
                
            chat = update.message.chat
            send_img(f, chat)
            update.message.reply_text(f'{bisect_number} - <ins><b>¿El cohete ya despegó o aún no ha despegado?</b></ins>\n/yes, <b>Ya despegó</b>,\n /no, <b>Aun no ha despegado</b>\nPuedes reiniciar el juego con el comando /restart', parse_mode=telegram.ParseMode.HTML)
            
            return ConversationHandler.END
    if number == '/restart':
            clear_cahe(context)
            bisect_number = str(random.randint(0, 61696))
            print(message_count)
            if message_count == 16:
                resultado = str(math.floor((int(number_before)+ int(number_after))/2))
                response = requests.get('http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/' + str(resultado), stream=True)
                with open(str(resultado)+'.png', 'wb') as f:
                                response.raw.decode_content = True
                                shutil.copyfileobj(response.raw, f)
                                
                chat = update.message.chat
                send_img(f, chat)
                update.message.reply_text(f'<b>Perfecto el cohete despega en {resultado}</b>\nSi lo deseas, escribe /start para volver a empezar', parse_mode=telegram.ParseMode.HTML)
                clear_cahe(context)
                message_count = 0
                return ConversationHandler.END
            context.user_data['numero'] = bisect_number
            response = requests.get('http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/' + bisect_number, stream=True)
            with open('temporal.png', 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
                
            chat = update.message.chat
            send_img(f, chat)
            update.message.reply_text(f'{bisect_number} - <ins><b>¿El cohete ya despegó o aún no ha despegado?</b></ins>\n/yes, <b>Ya despegó</b>,\n /no, <b>Aun no ha despegado</b>\nPuedes reiniciar el juego con el comando /restart', parse_mode=telegram.ParseMode.HTML)
            
            return ConversationHandler.END
    else:
            update.message.reply_text('Debes ingresar un número válido.\n Puedes reiniciar el juego con el comando /restart')

# Funciones comunes para las instancias del Bot

# Limpieza de memoria
def clear_cahe(context:CallbackContext):
    context.user_data['number_before'] = '0'
    context.user_data['number_after'] = '61696'
    global message_count
    message_count = 0

def isNumeric(s):
    return s.isdigit()

# Envío de imagen 
def send_img(f, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=50000
    )
    chat.send_photo(
        photo=open(f.name, 'rb')
    )
    os.unlink(f.name)

if __name__ == '__main__':
    #Conexíon a Telegram Bot
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    # Añadimos el  Handler
    dp.add_handler(CommandHandler('start', start))
    
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('ready', input_number),
                    CommandHandler('no', input_number),
                    CommandHandler('yes', input_number),
                    CommandHandler('restart', input_number),
                    
                    ],
        states={
            INPUT_NUMBER: [MessageHandler(Filters.text, input_number)]
        },
        fallbacks=[]
    ))

    # Escucha activa del chat
    updater.start_polling()
    updater.idle()