from enum import Enum


class AppEnvEnum(str, Enum):
    dev = "dev"
    staging = "staging"
    production = "production"
