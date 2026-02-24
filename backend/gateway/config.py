from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    # Upstream service URLs
    AUTH_SERVICE_URL: str = "http://auth:8001"
    RBAC_SERVICE_URL: str = "http://rbac:8002"
    QUOTATION_SERVICE_URL: str = "http://quotation:8003"
    INVOICE_SERVICE_URL: str = "http://invoice:8004"
    INVENTORY_SERVICE_URL: str = "http://inventory:8005"
    HRIS_SERVICE_URL: str = "http://hris:8006"
    NOTIFICATION_SERVICE_URL: str = "http://notification:8007"

    class Config:
        env_file = ".env"

settings = Settings()
