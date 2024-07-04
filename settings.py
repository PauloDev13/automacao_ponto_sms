from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf8'
    )

    USER_LOGIN: str
    USER_PASSWORD: str
    PATH_EXCEL: str
