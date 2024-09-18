from src.app import create_app
from src.mongodb.mongo_setup import connect_to_mongodb, disconnect_from_mongodb
from utils.custom_library_errors import *
from env_utils import MainSettings
import uvicorn


def main():
    try:
        settings=MainSettings()
        connect_to_mongodb()
        app = create_app(library_name=settings.library_name)
        uvicorn.run(app, host=settings.host, port=settings.port)
    except LibraryError:
        raise
    except Exception:
        raise
    finally:
        disconnect_from_mongodb()


if __name__ == "__main__":
    main()
