import os
from sanic import Sanic
from apps.chat_bot import routes
from multiprocessing import cpu_count

app = Sanic(__name__)

# chat_bot app register
app.blueprint(routes.chat_bot_blueprint)

# Host configurations
host = os.environ.get('HOST', 'localhost')
port = os.environ.get('PORT', 8080)
workers = os.environ.get('WORKERS', cpu_count())


if __name__ == '__main__':
    app.run(host=host, port=int(port), workers=workers)