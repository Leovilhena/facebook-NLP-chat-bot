from sanic import Blueprint
from sanic.response import text, json
from sanic.exceptions import ServerError, Forbidden, InvalidUsage

chat_bot_blueprint = Blueprint('chat_bot')


@chat_bot_blueprint.get('/')
async def facebook_auth_handler(request):
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == '12345678unit9':
            raise Forbidden('Verification token mismatch', 403)
        else:
            return text(request.args['hub.challenge'], 200)
    else:
        return text('Ok!', 200)

@chat_bot_blueprint.post('/')
async def facebook_message_handler(request):
    try:
        payload = request.json
        sender = payload['sender']['id']
        message = payload['message']['text']
    except (ValueError, KeyError, TypeError):
        raise InvalidUsage('Invalid payload')

    if not sender or not message:
        raise ServerError('Missing sender ID or message')

    return json({'sender': sender, 'message': message}, 200)