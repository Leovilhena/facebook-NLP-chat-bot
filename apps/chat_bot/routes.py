import ujson
import aiohttp
import datetime
from sanic import Blueprint
from sanic.response import text, json
from sanic.exceptions import ServerError, Forbidden, InvalidUsage
from apps.chat_bot.config import access_token
from apps.chat_bot.classes import Bot

chat_bot_blueprint = Blueprint('chat_bot')
bots_connections = {}  # This should be on a NoSQL database, ex.: Redis

@chat_bot_blueprint.get('/')
async def facebook_auth_handler(request):
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == '12345678unit9':
            raise Forbidden('Verification token mismatch')
        else:
            return text(request.args['hub.challenge'], 200)
    else:
        return text('Ok!', 200)

@chat_bot_blueprint.post('/')
async def facebook_message_handler(request):
    try:
        payload = request.json
        sender_id = payload['sender']['id']
        message = payload['message']['text']
    except (ValueError, KeyError, TypeError):
        raise InvalidUsage('Invalid payload')

    if not sender_id or not message:
        raise ServerError('Missing sender ID or message')

    bot = bots_connections.get(sender_id, Bot(sender_id))
    bot_reply = bot(message)
    data = prepare_data(sender_id, bot_reply)

    async with aiohttp.ClientSession(headers={'Content-type': 'application/json'}) as session:
        result, status_code = await send_message(session, data)

    if 'error' in result or status_code != 200:
        raise ServerError("Error while connecting to Facebook's API")

    return json({
        'sender': sender_id,
        'message': message,
        'reply': bot_reply,
        'mood': bot.mood,
        'timestamp': datetime.datetime.now()
    }, 200)

def prepare_data(sender_id, reply_message):
    return ujson.dumps({
        'recipient': {'id': sender_id},
        'message': {'text': reply_message}
    })

async def send_message(session, data):
    api_endpoint = f'https://graph.facebook.com/v3.1/me/messages?access_token={access_token}'

    try:
        async with session.post(api_endpoint, json=data) as result:
            return await result.json(), 200
    except aiohttp.client_exceptions.ClientError:
        raise ServerError({}, status_code=500)
