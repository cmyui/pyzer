#!/usr/bin/env python3.9
import asyncio

import uvicorn


async def main() -> int:
    uvicorn.run(
        "pyzer.api.init_api:app",
        host="127.0.0.1",
        port=443,
        ssl_keyfile="/home/cmyui/programming/certgen/key.pem",
        ssl_certfile="/home/cmyui/programming/certgen/cert.pem",
        reload=True,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
