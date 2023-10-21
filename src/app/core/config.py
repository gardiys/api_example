from zoneinfo import ZoneInfo

from dynaconf import Dynaconf
from pydantic import AnyUrl
from pydantic_settings import BaseSettings

_settings = Dynaconf(settings_files=["config.yaml"])
_project_timezone = "Europe/Moscow"

_db_dsn = AnyUrl.build(
    scheme="postgresql+asyncpg",
    username=_settings.database.user,
    password=_settings.database.password,
    host=_settings.database.host,
    port=_settings.database.port,
    path=_settings.database.db,
)


class Settings(BaseSettings):
    app_name: str
    timezone: str
    tz: ZoneInfo
    app_env: str
    db_dsn: str
    first_external_host: str
    second_external_host: str


settings = Settings(
    app_name="example_api",
    timezone=_project_timezone,
    tz=ZoneInfo(_project_timezone),
    app_env=_settings.app_env,
    db_dsn=str(_db_dsn),
    first_external_host=_settings.first_external_host,
    second_external_host=_settings.second_external_host,
)
