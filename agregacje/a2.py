from pymongo import MongoClient
db = MongoClient().zadanie

result = db.getglue.aggregate(
            [
                { "$group": { "_id": "$userId", "count": {"$sum": 1} } },
                { "$sort": { "count": -1 } },
                { "$limit": 10 }
            ]
            )

print(result)
