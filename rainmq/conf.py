import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    env: str
    SERVICE_NAME: str = 'Rain_MQ'
    DEBUG: bool = 'true' == os.getenv('DEBUG', 'true').lower()
    TESTING: bool = False
    HOST: str = os.getenv('APP_HOST', '127.0.0.1')
    PORT: int = int(os.getenv('APP_PORT', 8080))
    # db_host


@dataclass(frozen=True)
class Development(Config):
    DEBUG: bool = False


@dataclass(frozen=True)
class Testing(Config):
    TESTING: bool = True
    # db_host


@dataclass(frozen=True)
class Production(Config):
    DEBUG: bool = False

