from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
import requests
from telegram import ChatAction
import shutil
import os
import logging
import telegram


logging.basicConfig(
    level= logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()
#Solicitar Token
TOKEN = os.environ['TOKEN']

INPUT_NUMBER = 0

number_before = '0'
number_after = '61696' 
message_count = 0
text_init = '_'

# Inicializamos la conversación y respondemos con un saludo personalizado 
def start(update, context:CallbackContext):
    # Guardamos en memoria el nombre y creamos en memoria los números
    name = update.effective_user['first_name']
    context.user_data['number_before'] = '0'
    context.user_data['number_after'] = '61696'

    # Respuesta
    text_init = f'Hola {name}, \n<b>Vamos a calcular en qué momento despega el cohete!!!...</b>\n<ins><b>Fíjate con atención en la siguientes imágenes y dime si en la que eliges el cohete ha despegado o no</b></ins>\n(<i>Un pequeño consejo sería que estés atento al contador de la parte superior derecha de la pantalla (T-): aún no ha despegado, (T+): ya despegó</i>)\nTe preguntaré y contestarás un <b>SI</b> o un <b>NO</b> para ir definiedo el rango donde se encuetra la imagen del despegue, <b>TENGO MÁXIMO 16 INTENTOS PARA LOGRARLO</b>\nSi tienes un muy buen ojo y tu rango se redujo al punto de no poder avanzar, puedes pulsar <b>CALCULAR</b> para que definamos con precisión en que imagen despegó el cohete\n¿Estás listo? /ready para empezar el juego.'
    update.message.reply_text(text=text_init , parse_mode=telegram.ParseMode.HTML)
    context.user_data['text_init'] = text_init
    return INPUT_NUMBER

# Reinicio del Bot y Reinicio de caché
def restart(update, context:CallbackContext):
    bot = telegram.Bot(token=TOKEN)
    chat_id = update.effective_user['id']
    name = update.effective_user['first_name']  
    clear_cahe(context)
    bot.send_message(chat_id=chat_id, text=context.user_data['text_init'], parse_mode=telegram.ParseMode.HTML) 
    return INPUT_NUMBER

# Pregunta Inicial
def ready_command_handler(update, context:CallbackContext):
    clear_cahe(context)
    update.message.reply_text('Tenemos un video fraccionado en <strong>61696 imágenes</strong>, \nDime el número de la imagen que quieres tomar <ins><b>del 0 al 61696</b></ins> para poder calcular en cuál está despegando el cohete', parse_mode=telegram.ParseMode.HTML)

    return INPUT_NUMBER

# Si la respuesta es /no acortamos la muestra desde momento inicial a momento sugerido por usuario
# Guardamos en memoria el dato recibido
def ready_command_handler_before(update, context:CallbackContext): 
    number_before = context.user_data.get('numero')
    context.user_data['number_before'] = number_before
    if 'number_after' in context.user_data:
        number_after = context.user_data.get('number_after')
    else:
        number_after = '61696'
    update.message.reply_text('De acuerdo, intentemos con otro número entre ' + number_before + ' y ' + number_after+'\n Puedes reiniciar el juego con el comando /restart')
    return INPUT_NUMBER

# Si la respuesta es /si acortamos la muestra desde momento final a momento sugerido por usuario
# Guardamos en memoria el dato recibido
def ready_command_handler_after(update, context:CallbackContext):
    number_after = context.user_data.get('numero')
    context.user_data['number_after'] = number_after
    if 'number_before' in context.user_data:
        number_before = context.user_data.get('number_before')
    else:
        number_before = '0'

    update.message.reply_text('De acuerdo, intentemos con otro número entre ' + number_before + ' y ' + number_after +'\n Puedes reiniciar el juego con el comando /restart')
    return INPUT_NUMBER

# Si la respuesta es /calcular con la muestra reducida un promedio y pintamos el frame resultante 
# Actualizamos caché
def calcular(update, context:CallbackContext):
    resultado = round((int(context.user_data.get('number_before')) + int(context.user_data.get('number_after')))/2)
    response = requests.get('http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/' + str(resultado), stream=True)
    with open(str(resultado)+'.png', 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                    
    chat = update.message.chat
    send_img(f, chat)
    update.message.reply_text(f'<b>Lo más probable es que la imagen donde se encuentra despegando el cohete sea la {resultado}</b>\nSi lo deseas, escribe /start para volver a empezar', parse_mode=telegram.ParseMode.HTML)
    clear_cahe(context)
    return ConversationHandler.END


# Empezamos la orden 
def input_number(update, context:CallbackContext):
    number = update.message.text
    # Verificamos si el ingreso es un número válido y tomamos una decisión
    test = isNumeric(number)
    if number == '/ready':
            ready_command_handler(update, context)
            return INPUT_NUMBER
    elif number == '/restart':
            restart(update, context)
            return INPUT_NUMBER
    elif 'number_before' in context.user_data and context.user_data.get('number_before') >= number:
            update.message.reply_text(f'Debes ingresar un número menor a {number}.\n/calcular,<ins><b> No tengo más rango para elegir, pero estoy seguro que he capturado la imagen.</b></ins>\nPuedes reiniciar el juego con el comando /restart')
            return INPUT_NUMBER
    elif 'number_after' in context.user_data and context.user_data.get('number_after') <= number:
            update.message.reply_text(f'Debes ingresar un número mayor a {number}.\n/calcular,<ins><b> No tengo más rango para elegir, pero estoy seguro que he capturado la imagen.</b></ins> Puedes reiniciar el juego con el comando /restart')
            return INPUT_NUMBER
    else:
        # Si los campos son correctos empezamos la validación
        if test:
            global message_count
            message_count += 1
            print(message_count)
            if message_count == 17:
                calcular(update, context)
                message_count = 0
                return ConversationHandler.END
            context.user_data['numero'] = number
            response = requests.get('http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/' + number, stream=True)
            with open(number+'.png', 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
                
            chat = update.message.chat
            send_img(f, chat)
            update.message.reply_text('<ins><b>¿El cohete ya despegó o aún no ha despegado?</b></ins>\n/si, <b>Ya despegó</b>,\n /no, <b>Aun no ha despegado</b>,\n/calcular,<ins><b> No tengo más rango para elegir, pero estoy seguro que he capturado la imagen.</b></ins>\n Puedes reiniciar el juego con el comando /restart', parse_mode=telegram.ParseMode.HTML)
            
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
        entry_points=[CommandHandler('ready', ready_command_handler),
                    CommandHandler('no', ready_command_handler_before),
                    CommandHandler('si', ready_command_handler_after),
                    CommandHandler('restart', restart),
                    CommandHandler('calcular', calcular),
                    ],
        states={
            INPUT_NUMBER: [MessageHandler(Filters.text, input_number)]
        },
        fallbacks=[]
    ))

    # Escucha activa del chat
    updater.start_polling()
    updater.idle()