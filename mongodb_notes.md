# Notes for the mongodb json import.

Import the created json data file with the following line:
```
mongoimport --db p3 --collection maps --file openStreetMapData.osm.json
```

Output:
```
2017-06-12T08:11:00.187+0900    connected to: localhost
2017-06-12T08:11:01.593+0900    imported 44856 documents
```
