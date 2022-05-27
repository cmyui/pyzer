from starlette.config import Config

config = Config(".env")

DB_HOST = config.get("DB_HOST")
DB_PORT = config.get("DB_PORT")
DB_NAME = config.get("DB_NAME")
DB_USER = config.get("DB_USER")
DB_PASS = config.get("DB_PASS")

DB_DSN = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

REDIS_HOST = config.get("REDIS_HOST")
REDIS_PORT = config.get("REDIS_PORT")
REDIS_DB = config.get("REDIS_DB")
# TODO: REDIS_PASS?

# TODO: make these required

ACCESS_TOKEN_EXPIRATION_SECONDS = config.get(
    "ACCESS_TOKEN_EXPIRATION_SECONDS",
    default=86400,
)

DOMAIN = config.get("DOMAIN", default="ppy.sh")

VERSION = "0.0.0"
