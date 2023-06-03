from pymongo import MongoClient
import json
with open('db_client.json') as f:
    client2 = json.load(f)

client = MongoClient(client2['client'])
db = client.pythondb

def adding_money(name,val):
    if( repeat_register(name) == 1 ): # not register yet
        return
    
    now_money = query_money(name)

    if( now_money == None ):
        now_money = 0

    query_data = { 'discord_id': name }
    new_data = {'$set': { 'money': now_money+val }  }

    db["discord_user_data"].update_one(query_data,new_data)


def query_money(name):
    if( repeat_register(name) == 1 ):
        return -1 # not register yet

    for i in db["discord_user_data"].find():
        if( i["discord_id"] == name ):
            return i["money"]

def repeat_register(id):

    ok = 1

    for i in db["discord_user_data"].find():
        if( i["discord_id"] == id ):
            ok = 0
    print(id)
    return ok

def registered(name): 

    if( repeat_register(name) == 0 ):
        return -1 # already registered
    
    user_data = {
        "discord_id": "-1",
        "money": 0,
        "last_time": -1,
        "vocabulary": "None Start",
        "vocabulary_times": 0,
    }
    
    user_data["discord_id"] = name
    db["discord_user_data"].insert_one(user_data)
    return 1 # registered completed!

def query_account_vocabulary(name):
    for i in db["discord_user_data"].find():
        if( i["discord_id"] == name ):
            return i["vocabulary"]

def vocabulary_insert(name,val):
    
    now_vocabulary = query_account_vocabulary(name)

    query_data = { 'discord_id': name }
    new_data = {'$set': { 'vocabulary': val }  }

    db["discord_user_data"].update_one(query_data,new_data)
def vocabulary_time_update(name,val):
    
    query_data = { 'discord_id': name }
    new_data = {'$set': { 'vocabulary_times': val }  }

    db["discord_user_data"].update_one(query_data,new_data)
def query_times(name):
    for i in db["discord_user_data"].find():
        if( i["discord_id"] == name ):
            return i["vocabulary_times"]