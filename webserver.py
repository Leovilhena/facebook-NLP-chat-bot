import os
from sanic import Sanic
from apps.chat_bot import routes

app = Sanic(__name__)
app.blueprint(routes.chat_bot_blueprint)

host = os.environ.get('HOST', 'localhost')
port = os.environ.get('PORT', 8080)


if __name__ == '__main__':
    app.run(host=host, port=port)