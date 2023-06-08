import os
from typing import Literal

from pydantic import BaseSettings

# Pydantic BaseSetting, permet de declarer un mapping du `.env` .
# En donnant le chemin d'acces au fichier .env, pydantic gère l'import des variables.


class Settings(BaseSettings):
    environment: Literal["dev", "prod"]
    database_url: str

    # keys
    reset_token_key: str
    jwt_private_key: str

    # external keys
    meilisearch_masterkey: str
    sendgrid_api_key: str

    class Config:
        environment = os.environ["ENVIRONMENT"]
        env_file = f"./.env/{environment}.env"


settings = Settings()
