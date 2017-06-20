from pymongo import MongoClient

client = MongoClient()
db = client.p3
collection = db.maps

print("Number of documents:")
print("> collection.find().count()")
print(collection.find().count())

print("Number of nodes:")
print('> db.maps.find({"type":"node"}).count()')
print(db.maps.find({'type': 'node'}).count())

print("Number of ways:")
print('> db.maps.find({"type":"way"}).count()')
print(db.maps.find({"type":"way"}).count())

print("Unique users:")
print('> len(db.maps.distinct("created.user"))')
print(len(db.maps.distinct("created.user")))

print("Top #10 contributors:")
pr

> db.maps.aggregate([
                     {"$group":{"_id":"$created.user", "count":{"$sum":1}}}, 
                     {"$sort":{ "count":-1}}, 
                     {"$limit":10}
                    ]) 

{ "_id" : "Agatefilm", "count" : 27216 }
{ "_id" : "leojth", "count" : 5652 }
{ "_id" : "tothod", "count" : 2717 }
{ "_id" : "Fringillus", "count" : 1680 }
{ "_id" : "KLARSK", "count" : 1333 }
{ "_id" : "riiga", "count" : 965 }
{ "_id" : "Essin", "count" : 794 }
{ "_id" : "Gujo", "count" : 638 }
{ "_id" : "clobar", "count" : 463 }
{ "_id" : "FvGordon", "count" : 447 }
```

Most common amenities:
```
> db.maps.aggregate([ 
                     {"$match": {"amenity": {"$exists": 1}}}, 
                     {"$group": {"_id": "$amenity", "count": {"$sum": 1}}},  
                     {"$sort": {"count": -1}}, 
                     {"$limit": 10} 
                    ])

{ "_id" : "parking", "count" : 306 }
{ "_id" : "place_of_worship", "count" : 51 }
{ "_id" : "bicycle_parking", "count" : 43 }
{ "_id" : "shelter", "count" : 33 }
{ "_id" : "grave_yard", "count" : 27 }
{ "_id" : "restaurant", "count" : 24 }
{ "_id" : "school", "count" : 22 }
{ "_id" : "post_box", "count" : 21 }
{ "_id" : "fuel", "count" : 20 }
{ "_id" : "recycling", "count" : 17 }
```

