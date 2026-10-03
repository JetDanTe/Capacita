from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Capacita API"
    max_page_size: int = 50
    model_config = {"env_file": ".env"}



settings = Settings()