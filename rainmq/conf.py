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
    DATABASE_HOST: str = 'mongodb://localhost:27017'
    DATABASE_NAME: str = 'mq_logs'


@dataclass(frozen=True)
class Development(Config):
    env: str
    DEBUG: bool = True
    DATABASE_HOST = 'mongodb://localhost:27017'
    DATABASE_NAME = 'mq_logs'


@dataclass(frozen=True)
class Testing(Config):
    TESTING: bool = True
    # db_host


@dataclass(frozen=True)
class Production(Config):
    DEBUG: bool = False

