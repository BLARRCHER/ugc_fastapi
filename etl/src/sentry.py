import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from config import settings


def init_sentry():
    if settings.enable_sentry:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            debug=settings.debug,
            release=settings.release_version,
            request_bodies="medium",
            sample_rate=1.0,
            traces_sample_rate=0.0,
            integrations=[LoggingIntegration(event_level=None)],
        )
