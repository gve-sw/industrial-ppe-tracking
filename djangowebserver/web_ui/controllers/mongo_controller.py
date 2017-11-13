from pymongo import MongoClient
from .. import envs
from bson.objectid import ObjectId


def get_db():
    """
    :return: A Mongo database to be used for the app
    """
    client = MongoClient(envs.get_mongo_host(), int(envs.get_mongo_port()))
    db = client[envs.get_mongo_db()]
    return db


def translate_ids(items):
    """
    Given a list of Mongo objects, translate Object('') to a serializable string
    :return:
    """
    for item in items:
        item["_id"] = str(item["_id"])
    return items


def get_policies_table():
    """
    Return the table where policies are stored
    :return:
    """
    return get_db().policies


def insert_policy(policy):
    """
    Create or update a policy
    :return: The policy document
    """
    if "id" in policy.keys():
        # Means that is an update, to make it simpler we are going to just delete and add a new one.
        get_policies_table().delete_one({"_id": ObjectId(policy["id"])})
        # Remove ID from policy object
        policy.pop('id')
    # Add new policy
    return get_policies_table().insert_one(policy)


def get_policy_by_id(policy_id):
    """
    Get document policy by id
    :param policy_id:
    :return:
    """
    return get_policies_table().find_one({"_id": ObjectId(policy_id)})


def get_policy(json_filter):
    """
    Return policy according to the JSON filter
    :param json_filter:
    :return:
    """
    return list(get_policies_table().find_one(json_filter))


def get_all_policies():
    """
    Return all policies
    :return:
    """
    result = []
    for item in get_policies_table().find():
        item["id"] = str(item["_id"])
        item.pop("_id")
        result.append(item)
    return result


def delete_policy(policy_id):
    """
    Remove a policy from database
    :param policy:
    :return:
    """
    get_policies_table().delete_one({"_id": ObjectId(policy_id)})
