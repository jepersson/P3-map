# Repository for Udacity's Data analyst nanodegree, P3 Wrangle OpenStreetMap
data.

This is my notes for the above mentioned project. To find my writing about the
nanodegree's different projects visit my [blog](http://jepersson.github.io)
instead.

## Notes

Info about the data for the project can be found on:
[link](https://wiki.openstreetmap.org/wiki/OSM_XML)

An example report of the project can also be found here:
[link](https://docs.google.com/document/d/1F0Vs14oNEs2idFJR3C_OPxwS6L0HPliOii-QpbmrMo4/pub)

### Having a look at the contents of our xml file

* What are the different data present?
* How is the osm data defined?
  * Ways
  * Nodes
  * Relations
* What kind of structure should work best for our json file?
* Can we see any potential trouble with the data inputted?

### Reading in the xml data file

* Reading in the data line by line. Why?
* Write auditing scripts for each potential trouble found. Start with street
  names and post numbers.

### Outline for the data cleaning and conversion process

* Create a json conversion script that uses the auditing files to clean and
  convert the data to json.

### Conclusion and some data exploration

* Find out some fun things about the data inputted into the database, i.e.
  * size of the file
  * number of unique users
  * number of nodes and ways
  * number of chosen types, cafes/bakeries.

