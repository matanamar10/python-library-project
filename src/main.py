from src.app import create_app
from src.mongodb.mongo_setup import MongoDBConnectionManager
from utils.custom_library_errors import *
from env_utils import MainSettings
import uvicorn
import asyncio


async def main():
    mongo_manager = None
    try:
        mongo_manager = MongoDBConnectionManager()
        settings = MainSettings()

        await mongo_manager.connect()
        app = create_app(library_name=settings.library_name)
        uvicorn.run(app, host=settings.host, port=settings.port)

    except LibraryError:
        raise
    except Exception:
        raise
    finally:
        if mongo_manager:
            await mongo_manager.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
