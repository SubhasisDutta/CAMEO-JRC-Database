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
This package contains all the scripts to :
1. Extract information from CAMEO dataset and load it into MongoDB.
2. Extract information from JRC Entity dataset and load it into MongoDB.
3. Find all the relation between the CAMEO and JRC Actors and store it in a relation table.
Details to Run the Scripts are present in [ir-scripts/ReadMe](ir-scripts/ReadMe.md) 

## mr-script
This package will contain the Map reduce implementation of the join operation between CAMEO and JRC data.


## spark-script
This package will contain the Spark join implementation for the join operation between CAMEO and JRC data.

## jrc-classification
This package will contain the Machine Learning based classifier to identify the unidentified language for the different political Actors in JRC entity data set.



