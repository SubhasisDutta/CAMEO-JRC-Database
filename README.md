# JRC-Name-Parser
This repo contains script to parse the entity file of JRC names and put it in database.


## Installation
The scripts have dependency on PyMongo 

To install all dependency run
```
pip install -r requirements.txt
```

## To Execute the scripts

Setup the config.cnf file inside config.cnf with required details
```
#Configuration for Access Attributes
[MongoDBConnection]
db.host=localhost
db.port=27017
db.username=
db.password=
db.batch_limit=1000
db.schema=Political_Actors

[JRCNames]
JRCNames.entityfile=../data/jrc/entities
db.JRCNames=JRC_Names

[Cameo]
Cameo.Phoenix.agents=../data/cameo/Phoenix.agents.txt
Cameo.Phoenix.Countries.actors=../data/cameo/Phoenix.Countries.actors.txt
Cameo.Phoenix.International.actors=../data/cameo/Phoenix.International.actors.txt
Cameo.Phoenix.MilNonState.actors=../data/cameo/Phoenix.MilNonState.actors.txt
```


### Scripts to Run

### Rebuild JRC Names Collection

1. Setup the file location of config.cnf in JRCNames.entityfile attribute 
2. Run
```
python src/loadJRCData.py
```

Options:
```
usage: loadJRCData.py [-h] [--config CONFIG]

Script to process JRC data and push it into MongoDB collection.

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Location of Config File (default: ../config/config.cnf)
```

### Rebuild CAMEO Data Collection

1. Setup the Cameo file locations in config.cnf
2. Run
```
python src/loadCAMEOData.py
```

Options:
```
usage: loadCAMEOData.py [-h] [--config CONFIG]

Script to process CAMEO data and push it into MongoDB collection.

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Location of Config File (default: ../config/config.cnf)
```