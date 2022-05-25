#!/usr/bin/env bash
set -euxo pipefail

# wait for services we depend on to be ready
./scripts/await_port.sh $DB_HOST $DB_PORT
./scripts/await_port.sh $REDIS_HOST $REDIS_PORT

exec uvicorn pyzer.api.init_api:app \
    --host 0.0.0.0 \
    --port 443 \
    --ssl-keyfile /certs/key.pem \
    --ssl-certfile /certs/cert.pem \
    --reload
