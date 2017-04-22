# About this Project

This project is built to code events about political conflict and cooperation among different political actors in multiple languages(primarily Engilsh, Arabic and Spanish).
It is part of "Modernizing Political Event Data for Big Data Social Science Research".

Implemented under the guidance of: 
1. Prof. Patrick Brandt
2. Prof. Latifur Khan
3. Prof. Vincent Ng
4. Prof. Jennifer Holmes

Built at University of Texas at Dallas, funded by U.S National Science Foundation. 
Details here: https://www.nsf.gov/awardsearch/showAward?AWD_ID=1539302&HistoricalAwards=false 



# Political Name Parser for JRC and CAMEO dataset
This repo contains script to parse the entity file of JRC names, CAMEO actoe data and puts organizes it in a structured format in database.

## CAMEO Data Set
Conflict and Mediation Event Observations dataset obtained from https://github.com/openeventdata/Dictionaries

Details about CAMEO: 
 http://phoenixdata.org/description 
 http://eventdata.parusanalytics.com/papers.dir/Gerner.APSA.02.pdf

## JRC Dataset
JRC-Names is a highly multilingual named entity resource for person and organisation names (called 'entities'). It consists of large lists of names and their many spelling variants (up to hundreds for a single person), including across scripts (Latin, Greek, Arabic, Cyrillic, Japanese, Chinese, etc.).

https://ec.europa.eu/jrc/en/language-technologies/jrc-names

## BableNet
BabelNet is both a multilingual encyclopedic dictionary, with lexicographic and encyclopedic coverage of terms, 
and a semantic network which connects concepts and named entities in a very large network of semantic relations, 
made up of about 14 million entries, called Babel synsets. Each Babel synset represents a given meaning and contains
all the synonyms which express that meaning in a range of different languages.
http://babelnet.org/about 

# Project Modules

## ir-scripts
Contains all the scripts to :
1. Extract information from CAMEO dataset and load it into MongoDB.
2. Extract information from JRC Entity dataset and load it into MongoDB.
3. Find all the relation between the CAMEO and JRC Actors and store it in a relation table.

Details to Run the Scripts are present in [ir-scripts/ReadME](ir-scripts/)

## mr-script
This package will contain the Map reduce implementation of the join operation between CAMEO and JRC data.
<br/>
Details present in [mr-script/ReadME](mr-script/)

## spark-script
This package will contain the Spark join implementation for the join operation between CAMEO and JRC data.
<br/>
Details present in [spark-script/ReadME](spark-script/)

## jrc-classification
This package will contain the Machine Learning based classifier to identify the unidentified language for the different political Actors in JRC entity data set.
<br/>
Details present in [jrc-classification/ReadME](jrc-classification/)

## rest-server
Contains a web-server to allow different client systems to access the data from different client systems.
<br/>
Demo Server : http://35.160.238.107:2121/ 

Available API:
1. Check Status :<br/>
    ```<Server IP:port>/``` -  Should give a response<br/>
    Response:<br/>
    {"Status": "Server Running", "multilangAPI": "Welcome"}<br/>
    Ex - http://35.160.238.107:2121/
2. Full Raw Output :<br/>
    ```<Server IP:port>/search?query=<Person Name>``` - Returns all combined search resuls from CAMEO, JRC, BableNET and dbPedia.<br/>
    Ex:
    [http://35.160.238.107:2121/search?query=barrak+obama](http://35.160.238.107:2121/search?query=barrak+obama)<br/>
3. Filtered Output:<br/>
    a. ```<Server IP:port>/filter?query=<Person Name>``` - Returns all the translation found for the Person in default<br/>
    (Arabic, Spanish). The derault is setup in config/config.cnf.
    Eg:
    [http://35.160.238.107:2121/filter?query=donald+trump](http://35.160.238.107:2121/filter?query=donald+trump) 
    b. ```<Server IP:port>/filter?query=<Person Name>&source=bablenet``` - Returns all person name in default language for 
    only one data source. (By default it returns from all data source. Currently support: jrc, bablenet)<br/>
    Eg: 
    [http://35.160.238.107:2121/filter?query=hillary+clinton&source=jrc](http://35.160.238.107:2121/filter?query=hillary+clinton&source=jrc)<br/>
    [http://35.160.238.107:2121/filter?query=hillary+clinton&source=bablenet](http://35.160.238.107:2121/filter?query=hillary+clinton&source=bablenet)<br/>
    c.  ```<Server IP:port>/filter?query=<Person Name>&lang=<Language Code>``` - Returns all person name in a particular language.<br/>  
    Eg:     
    [http://35.160.238.107:2121/filter?query=donald+trump&lang=de](http://35.160.238.107:2121/filter?query=donald+trump&lang=de) (Names in German) <br/>
    [http://35.160.238.107:2121/filter?query=donald+trump&lang=ja](http://35.160.238.107:2121/filter?query=donald+trump&lang=ja) (Names in Japanese)<br/>
    [http://35.160.238.107:2121/filter?query=donald+trump&lang=hi](http://35.160.238.107:2121/filter?query=donald+trump&lang=hi) (Name in Hindi)<br/>
    [http://35.160.238.107:2121/filter?query=narendra+modi&lang=bn](http://35.160.238.107:2121/filter?query=narendra+modi&lang=bn) (Name in Bengali)<br/>
      
Details to setup and run is present in [rest-server/ReadME](rest-server/)

## webapp
This package contains a User Interface Client to visualize the data that can be accessed by the API.
<br/>
Details present in [webappn/ReadME](webapp/)


## Dependency
The scripts have dependency on PyMongo(For database connection), Python Tornado(for API server), editdistance

To install all dependency run
```
pip install -r requirements.txt
```

