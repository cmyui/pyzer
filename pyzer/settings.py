import os

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]

DB_DSN = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_DB = os.environ["REDIS_DB"]
# TODO: REDIS_PASS?

# TODO: make these required

ACCESS_TOKEN_EXPIRATION_SECONDS = os.environ.get(
    "ACCESS_TOKEN_EXPIRATION_SECONDS",
    86400,
)

DOMAIN = os.environ.get("DOMAIN", "ppy.sh")

VERSION = "0.0.0"
