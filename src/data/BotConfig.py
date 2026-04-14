from dataclasses import dataclass

#? engine
from bot_engine.utils.Dotenv import dotenv

#? data
from bot_engine.config.BotConfig import BotConfig, Environment


@dataclass
class SportHomeBotConfig(BotConfig):
    login: str = dotenv.get("LOGIN") or ""
    password: str = dotenv.get("PASSWORD") or ""
    test_products_collection: str = "products_backup"
    test_csv_products_collection: str = "csv_products_backup"
    


BOT_CONFIG = SportHomeBotConfig(
    active_bot = dotenv.get("ACTIVE_BOT") or "",
    bot_token = dotenv.get("BOT_TOKEN") or "",
    environment = dotenv.get("ENVIRONMENT") or Environment.development,
    port = dotenv.get_int("PORT") or 8000,
    default_language = dotenv.get("DEFAULT_LANGUAGE") or "ru",
    database_name = dotenv.get("DATABASE_NAME") or "",
    database_token = dotenv.get("DATABASE_TOKEN") or "",
    super_admin_id = dotenv.get_int("SUPER_ADMIN_ID"),
    admin_ids = dotenv.get_list_of_ints("ADMIN_IDS"),
    test_products_collection = "products_backup",
    test_csv_products_collection = "csv_products_backup",
)


FALLBACK_CHAT_ID = 486360237
# FALLBACK_CHAT_ID = 331697498 #? for producion testing

if BOT_CONFIG.environment == Environment.development:
    FALLBACK_CHAT_ID = 331697498



