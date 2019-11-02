import settings
from apes_search import app

if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)
