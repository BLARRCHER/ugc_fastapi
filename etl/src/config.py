import socket

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = "localhost:39092,localhost:39093,localhost:39094"
    clickhouse_host: str = "localhost"
    debug: bool = Field(False, env="ETL_KAFKA_DEBUG")
    max_batch_size: int = Field(1000, env="ETL_KAFKA_RECORDS_PER_BATCH")
    topic_names: list[str] = ["user.views"]
    group_id: str = "etl_kafka"
    auto_offset_reset: str = "smallest"

    enable_sentry: bool = Field(False, env="ENABLE_SENTRY")
    sentry_dsn: str = Field("<sentry dsn>", env="SENTRY_DSN")
    release_version: str = Field("ugc-service@1.0.0", env="RELEASE_VERSION")


settings = Settings()

consumer_config = {
    "bootstrap.servers": settings.kafka_bootstrap_servers,
    "group.id": settings.group_id,
    "auto.offset.reset": settings.auto_offset_reset,
    "enable.auto.offset.store": False,
}
producer_config = {
    "bootstrap.servers": settings.kafka_bootstrap_servers,
    "client.id": socket.gethostname(),
}
admin_config = {
    "bootstrap.servers": settings.kafka_bootstrap_servers,
}
