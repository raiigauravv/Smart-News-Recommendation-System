from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://snr-web.azurestaticapps.net",  # Azure Static Web Apps
        "https://*.azurestaticapps.net",  # Allow all Azure SWA subdomains
    ]  # Vite dev + Azure SWA


settings = Settings()
