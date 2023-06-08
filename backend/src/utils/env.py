import os
from pydantic import BaseSettings, Field

# Pydantic BaseSetting, permet de declarer un mapping du `.env` .
# En donnant le chemin d'acces au fichier .env, pydantic gère l'import des variables.

class Settings(BaseSettings):
    database_url: str
    database_log_url: str
    meilisearch_masterkey: str = Field(default=None)

    class Config:
        environment = os.environ['ENVIRONMENT']
        env_file = f"../.env/{environment}.env"

settings = Settings()