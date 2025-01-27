import logging
from payagram.bot import *
from payagram.containers import *
from payagram.keyboards import *
from payagram.tools import *
from decouple import config
from models.user import UserStates, Channel
from tools import manuwriter
from typing import Union
from tools.exceptions import *


# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# read .env configs
# You bot data
BOT_TOKEN = config('BOT_TOKEN')
HOST_URL = config('HOST_URL')
BOT_USERNAME = config('BOT_USERNAME')

# Read the text resource containing the multilanguage data for the bot texts, messages, commands and etc.
# Also you can write your texts by hard coding but it will be hard implementing multilanguage texts that way,
text_resources = manuwriter.load_json('texts', 'resources')

async def some_message_handler(bot: TelegramBot, message: GenericMessage) -> Union[GenericMessage, Keyboard|InlineKeyboard]:
    '''TODO: Write your handler'''

async def some_state_handler(bot: TelegramBot, message: GenericMessage) -> Union[GenericMessage, Keyboard|InlineKeyboard]:
    '''TODO: Write your state handler. For each state of the user defined in UserStates enum, you must define a handler.'''

async def some_inline_query_handler(bot: TelegramBot, callback_query: TelegramCallbackQuery)-> Union[GenericMessage, Keyboard|InlineKeyboard]:
    '''TODO: Write your inline query handler. handlers are categorized by action values of the query (inline keyboards must be grouped by special action values)
    You must write a handler for each single action value used in the bot.'''


# Parallel Jovbs:
def some_parallel_job(bot: TelegramBot)-> Union[GenericMessage, Keyboard|InlineKeyboard]:
    '''Parallel jobs are optional methods that will run by an special interval simultaniouesly with users requests.'''

main_keyboard = {
    'en': Keyboard(text_resources["keywords"]["some_message"]["en"]),
    'fa': Keyboard(text_resources["keywords"]["some_message"]["fa"])
}

bot = TelegramBot(token=BOT_TOKEN, username=BOT_USERNAME, host_url=HOST_URL, text_resources=text_resources, _main_keyboard=main_keyboard)

bot.add_state_handler(state=UserStates.SELECT_CHANNEL, handler=some_state_handler)
bot.add_message_handler(message=bot.keyword('some_message_handler'), handler=some_message_handler)
bot.add_callback_query_handler(action="int", handler=some_inline_query_handler)
bot.add_command_handler(command='uptime', handler=lambda bot, message: (GenericMessage.Text(message.by.chat_id, bot.get_uptime()), None))

bot.start_clock()  # optional, but mandatory if you defined at least one parallel job. also if you want to calculate bot uptime.
bot.config_webhook()  # automatically writes the webhook path route handler, so that users messages(requests), all be passed to bot.handle method

@bot.app.route('/other_routes', methods=['POST'])
def something():
    '''Special route handler. optional. used for some special purposes, for example if your bot uses payment gateways, you must define payment callback route this way.'''
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    bot.go(debug=False)  # Run the Flask app
