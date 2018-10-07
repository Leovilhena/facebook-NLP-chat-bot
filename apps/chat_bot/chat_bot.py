from sanic import Blueprint
from sanic.response import text

chat_bot_blueprint = Blueprint('chat_bot')


@chat_bot_blueprint.get('/')
async def facebook_auth_handler(request):
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == '12345678unit9':
            return text('Verification token mismatch', 403)
        else:
            return text(request.args['hub.challenge'], 200)
    else:
        return text('Ok!', 200)

