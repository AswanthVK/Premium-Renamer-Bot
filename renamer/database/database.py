import datetime
import os
import motor.motor_asyncio

# Required For Database

MANGODB_URL = os.environ.get("MANGODB_URL", "mongodb+srv://dkbotz:786@cluster0.pczec.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
SESSION_NAME = os.environ.get("SESSION_NAME", "PAID")

class Singleton(type):
    __instances__ = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances__:
            cls.__instances__[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.__instances__[cls]


class Database(metaclass=Singleton):
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.col = self.db.users
        self.cache = {}

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            last_used_on=datetime.date.today().isoformat(),
            settings={
                'permanent_thumb': '',
                'upload_as_file': True,
                'bot_updates': True,
                'screen_shot': 0,
                'sample_video': 0,
                'custom_caption': '**{filename}**'},
            paid_status={
                'is_paid': False,
                'paid_duration': 0,
                'paid_on': datetime.datetime.now(),
                'paid_username': "",
                'paid_reason': ""},
            ban_status={
                'is_banned': False,
                'ban_duration': 0,
                'banned_on': datetime.date.max.isoformat(),
                'ban_reason': ''
            }
        )



################## Paid Function ##################
    async def remove_paid(self, id):
        await self.get_user(id)
        paid_status = dict(
            is_paid=False,
            paid_duration=0,
            paid_on=datetime.datetime.now(),
            paid_username="",
            paid_reason="",
        )
        self.cache[id]["paid_status"] = paid_status
        await self.col.update_one({"id": id}, {"$set": {"paid_status": paid_status}})

    async def paid_user(self, user_id, paid_username, paid_duration, paid_reason):
        await self.get_user(user_id)
        paid_status = dict(
            is_paid=True,
            paid_duration=paid_duration,
            paid_on=datetime.datetime.now(),
            paid_username=paid_username,
            paid_reason=paid_reason,
        )
        self.cache[user_id]["paid_status"] = paid_status
        await self.col.update_one(
            {"id": user_id}, {"$set": {"paid_status": paid_status}}
        )

    async def get_paid_status(self, id):
        default = dict(
            is_paid=False,
            paid_duration=0,
            paid_on=datetime.datetime.now(),
            paid_username="",
            paid_reason="",
        )
        user = await self.get_user(id)
        return user.get("paid_status", default)

    async def get_all_paid_users(self):
        paid_users = self.col.find({"paid_status.is_paid": True})
        return paid_users

################## Checking & Adding New User 👤 ##################

    async def get_user(self, id):
        user = self.cache.get(id)
        if user is not None:
            return user

        user = await self.col.find_one({"id": int(id)})
        self.cache[id] = user
        return user

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.get_user(id)
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def update_last_used_on(self, id):
        self.cache[id]["last_used_on"] = datetime.date.today().isoformat()
        await self.col.update_one(
            {"id": id}, {"$set": {"last_used_on": datetime.date.today().isoformat()}}
        )


    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        user_id = int(user_id)
        if self.cache.get(user_id):
            self.cache.pop(user_id)
        await self.col.delete_many({"id": user_id})

    async def get_last_used_on(self, id):
        user = await self.get_user(id)
        return user.get("last_used_on", datetime.date.today().isoformat())

    async def get_user_update(self):
         user = self.col.find({'settings.bot_updates': True})
         return user

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

################## Settings ⚙ ##################

    async def get_settings_status(self, id, key):
        user = await self.col.find_one({'id':id})
        settings = user.get('settings')
        return settings.get(str(key), True)

    async def get_all_settings(self, id):
        user = await self.col.find_one({'id':id})
        settings = user.get('settings')
        return settings

    async def update_settings_status(self, id, key, value):
        user = await self.col.find_one({'id':id})
        settings = user.get('settings')
        settings[key] = value
        await self.col.update_one({'id': id}, {'$set': {'settings': settings}})   


################## Ban Status 🚫 ##################


    async def remove_ban(self, id):
        await self.get_user(id)
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason="",
        )
        self.cache[id]["ban_status"] = ban_status
        await self.col.update_one({"id": id}, {"$set": {"ban_status": ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        await self.get_user(user_id)
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason,
        )
        self.cache[user_id]["ban_status"] = ban_status
        await self.col.update_one({"id": user_id}, {"$set": {"ban_status": ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason="",
        )
        user = await self.get_user(id)
        return user.get("ban_status", default)

    async def get_all_banned_users(self):
        banned_users = self.col.find({"ban_status.is_banned": True})
        return banned_users
