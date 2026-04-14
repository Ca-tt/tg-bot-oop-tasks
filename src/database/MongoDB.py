#
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Union
from json import dump

from src.data import BotConfig

from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.results import DeleteResult

from src.data.BotConfig import SportHomeBotConfig

@dataclass
class ConfigDocument:
    _id: str = "_id"
    parse_time: str = "parse_time"


@dataclass
class ProductDocument:
    _id: str = "_id"
    id: str = "id"


@dataclass
class StatisticsDocument:
    _id: str = "_id"
    products_tracked: str = "products_tracked"


@dataclass
class Collections:
    config: str = "config"
    stats: str = "stats"
    products: str = "products"
    csv_products: str = "csv_products"


CONFIG_DOCUMENT = ConfigDocument()
PRODUCT_DOCUMENT = ProductDocument()
STATS_DOCUMENT = StatisticsDocument()
DB_COLLECTIONS = Collections()  
    
class Database:
    """MongoDB database"""

    def __init__(self, bot_config: SportHomeBotConfig) -> None:
        self.bot_config = bot_config
        
        self.client = MongoClient(bot_config.database_token)
        self.db = self.client[bot_config.database_name]
        self.users_collection = self.db[bot_config.users_collection]
        self.products_collection = self.db[bot_config.products_collection]
        self.test_products_collection = self.db[bot_config.test_products_collection]

        """ collections """
        self.config_collection = self.db[DB_COLLECTIONS.config]
        self.stats_collection = self.db[DB_COLLECTIONS.stats]
        self.csv_products_collection = self.db[DB_COLLECTIONS.csv_products]
        self.test_csv_products_collection = self.db[bot_config.test_csv_products_collection]


    def get(self, collection_name: str = DB_COLLECTIONS.config) -> list[dict]:
        """returns list of documents from given collection"""
        return list(self.db[collection_name].find({}))
    
    def add_to_collection(self, collection_name: str, document: dict) -> None:
        try:
            self.db[collection_name].insert_one(document)
            print(f"Document added to {collection_name} collection")
        except Exception as e:
            print(f"An error occurred while adding document to {collection_name} collection: {e}")


    def save_products_to_json(self):
        def convert_objectid(obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            if isinstance(obj, dict):
                return {k: convert_objectid(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [convert_objectid(item) for item in obj]
            return obj

        products = self.get(collection_name=DB_COLLECTIONS.products)
        products_serializable = convert_objectid(products)

        with open("products.json", "w", encoding="utf-8") as file:
            dump(products_serializable, file, ensure_ascii=False, indent=4)


    def insert_product(self, product: Dict[str, Any]) -> None:
        try:
            status = self.products_collection.find_one({"id": product["id"]})
            if status:
                print("Product already exists in the database")
                return
            else:
                self.products_collection.insert_one(product)
                print("Product inserted into database")
        except Exception as e:
            print(f"An error occurred: {e}")


    def get_products(self) -> List[dict]:
        try:
            products = list(self.products_collection.find({}))
            return products
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    
    
    def get_test_products(self) -> List[dict]:
        try:
            products = list(self.test_products_collection.find({}))
            return products
        except Exception as e:
            print(f"An error occurred: {e}")
            return []


    def insert_user(self, user: Dict[str, Any]) -> None:
        try:
            status = self.users_collection.find_one({"chat_id": user["chat_id"]})
            if status:
                print("User already exists in the database")
                return
            else:
                self.users_collection.insert_one(user)
                print("User inserted into database")
        except Exception as e:
            print(f"An error occurred: {e}")


    def get_user_by_id(self, user_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        try:
            return self.users_collection.find_one({"chat_id": user_id})
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def get_users(self) -> List[Dict[str, Any]]:
        try:
            users = list(self.users_collection.find())
            return users
        except Exception as e:
            print(f"An error occurred: {e}")
            return []


    def find(
        self, key: str, value: Union[str, int, bool, list]
    ) -> Optional[Dict[str, Any]]:
        return self.products_collection.find_one({key: value})
    
    def find_document(
        self, collection_name: str, key: str, value: Union[str, int, bool, list]
    ) -> Optional[Dict[str, Any]]:
        return self.db[collection_name].find_one({key: value})


    def update(self, key: str, value: Any, field_name: str, new_value: Any) -> None:
        try:
            self.products_collection.update_one(
                {key: value}, {"$set": {field_name: new_value}}
            )
            print(f"Updated {field_name} to {new_value} for {key}: {value}")
        except Exception as e:
            print(f"An error occurred: {e}")


    def update_one_document(
        self,
        collection_name: str = "config",
        key: str = "",
        value: Union[str, int, bool] = "",
    ) -> None:
        """updates one document in collection"""

        document: dict = self.db[collection_name].find_one({})

        if document:
            document_id = document[CONFIG_DOCUMENT._id]
        else:
            print(f"🔴 No config document found!")
            return

        update_data = {"$set": {key: value}}
        result = self.db[collection_name].update_one(
            {"_id": ObjectId(document_id)}, update_data
        )

        if result.modified_count > 0:
            print(f"🟢 Config updated: {key}:{value}")

        elif result.matched_count > 0:
            print("🟡 Nothing new in config")

        else:
            print("🔴 Error: no such _id or document in config collection")


    def get_parse_time(self) -> List[int]:
        document = self.config_collection.find_one({})

        parse_time = [19, 0]

        if document is None:
            # ? set default time
            document = {CONFIG_DOCUMENT.parse_time: parse_time}
            self.config_collection.insert_one(document)

        else:
            parse_time = document[CONFIG_DOCUMENT.parse_time]

            # ? set default time
            for time in parse_time:
                if time is None:
                    parse_time = [19, 0]

        return parse_time


    # ? REMOVALS
    
    def remove_from_collection(self, collection_name: str, key: str, value: Any) -> bool:
        """removes document from collection by key and value"""
        result = self.db[collection_name].delete_one({key: value})
        if result.deleted_count > 0:
            print(f"🟢 Document with {key}:{value} deleted from {collection_name} collection!")
        else:
            print(f"🟡 Document with {key}:{value} not found in {collection_name} collection!")
            
        return result.deleted_count > 0
    
    def remove_product(self, id: int) -> None:
        document = self.products_collection.delete_one({PRODUCT_DOCUMENT.id: id})

        if document:
            print(f"🟢 product {id} deleted from DB!")
        else:
            print(f"🟡 Product with {id} not found in DB!")

    def remove_product_by_url(self, url: str) -> None | DeleteResult:
        result = None

        if url:
            result = self.db[DB_COLLECTIONS.products].delete_one(filter={"url": url})

        return result


    # ? STATS
    def count_documents(self, collection_name: str) -> int:
        return self.db[collection_name].count_documents({})
    
    def get_products_count(self) -> int:
        """ returns number of products in product collection """
        return len(self.get_products())

    def get_products_tracked_stats(self) -> int:
        document = self.stats_collection.find_one({})
        return document[STATS_DOCUMENT.products_tracked]
