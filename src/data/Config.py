from dataclasses import dataclass, field
from typing import Optional, List


#? bot engine
from bot_engine.utils.Dotenv import Dotenv

dotenv = Dotenv()


@dataclass
class Environment:
    development: str = "development"
    production: str = "production"

@dataclass
class BotConfig:
    """ sets bot-level config (local level) """
    #? bot
    active_bot: str
    bot_token: str

    #? configs
    environment: str
    port: int
    default_language: str

    #? DB
    database_name: str
    database_token: str
    super_admin_id: int
    admin_ids: List[int]
    user_ids: Optional[List[int]] = field(init=False)
    
    #? settings
    database_connections_limit: Optional[int] = 1
    replica_name: Optional[str] = ""
    users_collection: Optional[str] = "users"
    products_collection: Optional[str] = "products"
    versions_collection: Optional[str] = "versions"

    #? telegram API
    user_id: str = "user_id"
    chat_id: str = "chat_id"
    
    
