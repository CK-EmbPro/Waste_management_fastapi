from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    algorithm: str
    access_token_expire_minute: str
    refresh_token_expire_minute: str
    jwt_access_secret_key: str
    jwt_refresh_secret_key: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8")
    
settings = Settings()