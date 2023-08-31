from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR.parent / ".env.local"


class Settings(BaseSettings):
    project_name: str = Field("UGC Movies", env="UGC_PROJECT_NAME")
    debug: bool = Field(True, env="UGC_DEBUG")
    jwt_secret_key: str = Field("secret_jwt_key", env="UGC_JWT_KEY")
    mock_auth_token: bool = Field(
        False, env="UGC_MOCK_AUTH_TOKEN"
    )  # для отладки - можно отключить проверку токена в заголовках
    jaeger_host_name: str = Field("localhost", env="JAEGER_HOST_NAME")
    jaeger_port: int = Field(6831, env="JAEGER_PORT")
    enable_tracer: bool = Field(False, env="ENABLE_TRACER")

    kafka_instance: str = Field("localhost:39092", env="UGC_KAFKA_INSTANCE")

    mongo_url: str = Field(
        "mongodb://user_name:user_password@localhost:27017/prod-db?authSource=admin", env="UGC_MONGO_URL"
    )
    mongo_db: str = Field("prod-db", ENV="MONGO_DB")

    enable_sentry: bool = Field(False, env="ENABLE_SENTRY")
    sentry_dsn: str = Field("<sentry dsn>", env="SENTRY_DSN")
    release_version: str = Field("ugc-service@1.0.0", env="RELEASE_VERSION")


settings = Settings(_env_file=ENV_FILE)
