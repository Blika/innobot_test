from decouple import config
from playhouse.db_url import connect

TOKEN = config("TOKEN")
DB = connect(config("DATABASE_URL", default="sqlite:///botttt.db"))
PORT = config("PORT", default=8443, cast=int)
HEROKU_APP_NAME = config("HEROKU_APP_NAME", default=None)
