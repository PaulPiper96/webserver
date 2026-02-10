import os
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    app_name: str = "ScalableFastAPIProject"
    debug: bool = False

    # kommt aus docker-compose:
    # DATABASE_URL="mysql+pymysql://user:pass@db:3306/fastapi_db"
    database_url: str = ""

    @property
    def db_url(self) -> str:
        url = self.database_url or os.getenv("DATABASE_URL")
        if not url:
            raise RuntimeError("DATABASE_URL / database_url is not set")
        return url

config = Config()