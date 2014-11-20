from pymongo import MongoClient
db = MongoClient().zadanie

result = db.getglue.aggregate(
            [
                { "$match": { "action": "Disliked" }},
                { "$group": { "_id": "$title", "count": {"$sum": 1} } },
                { "$sort": { "count": -1 } },
                { "$limit": 10 }
                ]
            )

print(result)
