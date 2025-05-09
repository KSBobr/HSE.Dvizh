from datetime import datetime
import config
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]
def init_db():
    db.users.create_index([("email", 1)], unique=True)
    db.events.create_index([("title", "text")])
    db.achievements.create_index(["achievement_name"])
    db.categories.create_index(["category_name"])

class User:
    @staticmethod
    def create(name: str, email: str, password: str, role: str):
        return db.users.insert_one({
            "name": name,
            "email": email,
            "password": password,
            "role": role,
            "registration_date": datetime.now(),
            "friends": [],
            "events":[],
            "favorite_events": [],
            "achievements": [],
            "number_of_event": 0,
            "number_of-org_event": 0
            # pictures
        })

    @staticmethod
    def get_by_id(user_id: str):
        return db.users.find_one({"_id": ObjectId(user_id)})
    @staticmethod
    def add_event(user_id: str, event_id: str):
        return db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"events": ObjectId(event_id)},
             "$inc": {"number_of_event":1}}
        )

    @staticmethod
    def add_f_event(user_id: str, event_id: str):
        return db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"favorite_events": ObjectId(event_id)}}
        )
    @staticmethod
    def add_friend(user_id1: str, user_id2: str):
        return db.users.update_one(
            {"_id": ObjectId(user_id1)},
            {"$addToSet": {"favorite_events": ObjectId(user_id2)}}
        )
    @staticmethod
    def add_achievement(user_id: str, achievement_id: str):
        return db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"favorite_events": ObjectId(achievement_id)}}
        )

class Event:
    @staticmethod
    def create(title: str, date: datetime, location: str, category: ObjectId):
        return db.events.insert_one({
            "title": title,
            "date": date,
            "location": location,
            "category": category,
            "users": [],
            "organizers": [],
            "status": "planned"
            #"pictures":[???]
        })
    
    @staticmethod
    def add_user(event_id: str, user_id: str):
        return db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$addToSet": {"users": ObjectId(user_id)}}
        )
    def add_organizers(event_id: str, user_id: str):
        return db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$addToSet": {"users": ObjectId(user_id)}}
        )
class Category:
    @staticmethod
    def create(name: str):
        return db.categories.insert_one({
            "category_name": name
        })
class Achievement:
    @staticmethod
    def create(name: str):
        return db.achievements.insert_one({
            "achievement_name": name
            #picture
        })