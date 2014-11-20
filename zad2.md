# Zadanie 2

Import danych (~19M rekordow):
```
mongoimport --file e:/getglue_sample.json --type json --headerline -d zadanie -c getglue
```
Python od wersji 3.4 ma wbudowany menedzer pakietow pip. Biblioteke **pymongo** instaluje sie poprzez
```
pip install pymongo
```
(w systemie Windows potrzebna jest modyfikacja zmiennej PATH aby móc korzystac z pipa w cmd)

# 1
10 pozycji, które dostały najwiecej akcji 'dislike':

mongo:
```js
db.getglue.aggregate(
    { $match: { "action": "Disliked" }},
    { $group: { _id: "$title", count: {$sum: 1} } },
    { $sort: { count: -1 } }, { $limit: 10 } );
```

python:
```py
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
```

Wynik
```js
{  
   'ok':1.0,
   'result':[  
      {  
         'count':1452,
         '_id':'Two and a Half Men'
      },
      {  
         'count':1392,
         '_id':'Twilight'
      },
      {  
         'count':1315,
         '_id':'Sex and the City'
      },
      {  
         'count':1223,
         '_id':'Glee'
      },
      {  
         'count':1151,
         '_id':'Jersey Shore'
      },
      {  
         'count':1066,
         '_id':'Titanic'
      },
      {  
         'count':1060,
         '_id':'American Idol'
      },
      {  
         'count':985,
         '_id':'CSI: Miami'
      },
      {  
         'count':979,
         '_id':"Grey's Anatomy"
      },
      {  
         'count':976,
         '_id':'Gossip Girl'
      }
   ]
}
```
# 2
10 najaktywniejszych użytkownikow:

mongo
```js
db.getglue.aggregate(
      { $group: { _id: "$userId", count: {$sum: 1} } },
      { $sort: { count: -1 } },
      { $limit: 10 }
    )
```

python
```py
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
```

Wynik
```js
{ "_id" : "LukeWilliamss", "count" : 696782 }
{ "_id" : "demi_konti", "count" : 68137 }
{ "_id" : "bangwid", "count" : 59261 }
{ "_id" : "zenofmac", "count" : 56233 }
{ "_id" : "agentdunham", "count" : 55740 }
{ "_id" : "cillax", "count" : 43161 }
{ "_id" : "tamtomo", "count" : 42378 }
{ "_id" : "hblackwood", "count" : 32832 }
{ "_id" : "ellen_turner", "count" : 32239 }
{ "_id" : "husainholic", "count" : 32135 }
```

# 3
5 najbardziej lubianych filmów Woody'ego Allena:

mongo:
```js
db.getglue.aggregate(
      { $match: {director: "woody allen"  } },
      { $match: {action: "Liked"} },
      { $group: {_id: "$title", count: {$sum: 1}} },
      { $sort: {count: -1} },
      { $limit : 5}
    )
```

python:
```py
from pymongo import MongoClient
db = MongoClient().zadanie

result = db.getglue.aggregate(
            [
              { $match: {director: "woody allen"  } },
              { $match: {action: "Liked"} },
              { $group: {_id: "$title", count: {$sum: 1}} },
              { $sort: {count: -1} },
              { $limit : 5}
            ]
          )
print(result)
```

Wynik
```js
{ "_id" : "Midnight in Paris", "count" : 2024 }
{ "_id" : "Vicky Cristina Barcelona", "count" : 1876 }
{ "_id" : "Annie Hall", "count" : 1629 }
{ "_id" : "Manhattan", "count" : 956 }
{ "_id" : "Sleeper", "count" : 924 }
```

# 4
10 najpopularniejszych filmów/seriali

mongo:
```js
db.getglue.aggregate(
      { $match: { "modelName": "movies" || "tv_shows"  } },
      { $group: {_id: "$title", count: {$sum: 1} } },
      { $sort: {count: -1} },
      { $limit: 10}
    )
```

python:
```py
from pymongo import MongoClient
db = MongoClient().zadanie

result = db.getglue.aggregate(
            [
              { "$match": { "modelName": "movies" || "tv_shows"  } },
              { "$group": {"_id": "$title", "count": {"$sum": 1} } },
              { "$sort": {"count": -1} },
              { "$limit": 10}
            ]
          )
print(result)
```

Wynik
```
{ "_id" : "The Twilight Saga: Breaking Dawn Part 1", "count" : 87521 }
{ "_id" : "The Hunger Games", "count" : 79340 }
{ "_id" : "Marvel's The Avengers", "count" : 64356 }
{ "_id" : "Harry Potter and the Deathly Hallows: Part II", "count" : 33680 }
{ "_id" : "The Muppets", "count" : 29002 }
{ "_id" : "Captain America: The First Avenger", "count" : 28406 }
{ "_id" : "Avatar", "count" : 23238 }
{ "_id" : "Thor", "count" : 23207 }
{ "_id" : "The Hangover", "count" : 22709 }
{ "_id" : "Titanic", "count" : 20791 }
```
