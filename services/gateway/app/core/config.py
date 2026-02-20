from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'Compliance Gateway'
    secret_key: str = 'change-me'
    access_token_expire_minutes: int = 60
    database_url: str = 'postgresql://fintech:fintech@postgres:5432/fintech'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
