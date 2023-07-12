import os
from typing import Literal
from sqlalchemy.engine.url import URL

from pydantic import BaseSettings

# Pydantic BaseSetting, permet de declarer un mapping du `.env` .
# En donnant le chemin d'acces au fichier .env, pydantic gère l'import des variables.


class Settings(BaseSettings):
    environment: Literal["development", "production"] = os.getenv("CONFIG_NAME")
    postgres_user: str
    postgres_password: str
    postgres_hostname: str
    postgres_port: int
    postgres_db: str

    # hash keys
    reset_token_key: str
    jwt_private_key: str

    # s3 keys
    scality_access_key_id: str
    scality_secret_access_key: str

    # external keys
    meilisearch_masterkey: str | None = None
    sendgrid_api_key: str

    @property
    def postgres_url(self):
        url = URL.create(
        drivername="postgresql+psycopg2",
        username=self.postgres_user,
        password=self.postgres_password,
        host=self.postgres_hostname,
        port=self.postgres_port,
        database=self.postgres_db,
        )
        return url.render_as_string(hide_password=False)

        
    class Config:
        config = os.getenv("CONFIG_NAME")
        env_file = f"./{config}.env"
        if config is None:
            raise ValueError("No 'CONFIG_NAME' env variable set")
        elif os.path.isfile(env_file) is False:
            raise ValueError(f"No {config}.env file found")


settings = Settings()