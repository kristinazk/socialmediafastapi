from pydantic_settings import BaseSettings

# validation for all the environment variables
class Settings(BaseSettings):
    pg_user: str
    pg_password: str
    pg_db: str
    secret_key: str
    algorithm : str
    access_token_expire_minutes : int

    class Config:
        env_file = '.env'

settings = Settings()
