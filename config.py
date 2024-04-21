from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    token: SecretStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config_sets = Settings()

# pydantic==2.5.3
# pydantic-settings==2.2.1
