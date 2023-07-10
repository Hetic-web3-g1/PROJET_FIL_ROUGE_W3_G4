import os
from typing import Literal

from pydantic import BaseSettings

# Pydantic BaseSetting, permet de declarer un mapping du `.env` .
# En donnant le chemin d'acces au fichier .env, pydantic gère l'import des variables.


class Settings(BaseSettings):
    environment: Literal["development", "production"] = os.getenv("CONFIG_NAME")
    postgres_url: str

    # hash keys
    reset_token_key: str
    jwt_private_key: str

    # external keys
    meilisearch_masterkey: str | None = None
    sendgrid_api_key: str

    class Config:
        config = os.getenv("CONFIG_NAME")
        env_file = f"./{config}.env"
        if config is None:
            raise ValueError("No 'CONFIG_NAME' env variable set")
        elif os.path.isfile(env_file) is False:
            raise ValueError(f"No {config}.env file found")


settings = Settings()
