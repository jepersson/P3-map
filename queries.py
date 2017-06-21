from pymongo import MongoClient

client = MongoClient()
db = client.p3
collection = db.maps

print("Number of documents:")
print("> collection.find().count()")
print(collection.find().count())

print("Number of nodes:")
print('> db.maps.find({"type": "node"}).count()')
print(db.maps.find({'type': 'node'}).count())

print("Number of ways:")
print('> db.maps.find({"type": "way"}).count()')
print(db.maps.find({"type": "way"}).count())

print("Unique users:")
print('> len(db.maps.distinct("created.user"))')
print(len(db.maps.distinct("created.user")))

print("Top #10 contributors:")
print('''> db.maps.aggregate([
    {"$group":{"_id": "$created.user", "count": {"$sum": 1}}},
    {"$sort":{ "count": -1}},
    {"$limit": 10}
])''')
agg_results = db.maps.aggregate([
    {"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
])
print("\n".join(map(str, [x for x in agg_results])))


print("Most common amenity:")
print('''> db.maps.aggregate([
    {"$match": {"amenity": {"$exists": 1}}},
    {"$group": {"_id": "$amenity", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
])''')
agg_results = db.maps.aggregate([
    {"$match": {"amenity": {"$exists": 1}}},
    {"$group": {"_id": "$amenity", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
])
print("\n".join(map(str, [x for x in agg_results])))
