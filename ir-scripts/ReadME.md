
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
cd ir-scripts
python loadJRCData.py
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
cd ir-scripts
python loadCAMEOData.py
```

Options:
```
usage: loadCAMEOData.py [-h] [--config CONFIG]

Script to process CAMEO data and push it into MongoDB collection.

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Location of Config File (default: ../config/config.cnf)
```

### Create relationship table of CAMEO and JRC

1. Setup the Cameo file locations in config.cnf
2. Run 
```
cd ir-scripts
python createCameoJRCRelation.py
```

```
usage: createCameoJRCRelation.py [-h] [--config CONFIG]

Script to load CAMEO and JRC data and find their relation and store them in a
table.

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Location of Config File (default: ../config/config.cnf)
```

### Build the JRC and Bablenet Name Translation dataset 

1. Setup the Cameo file locations in config.cnf
2. Run 

```
cd ir-scripts
python buildCameo_Jrc_Bablenet_NameDataset.py
```
* If we need to build only the JRC data :
Edit Line 49 : to 
```angular2html
processComplete = processor.process(True,False)
```
* If we need to select a different CAMEO data set to build data
Edit Line 49 : to 
```angular2html
processComplete = processor.process(False,True)
```
change nameTranslatorService.py
```angular2html
Line 49:
cameo_data = cameo.find({"record_type": "Cameo.Phoenix.Countries.actors",
                                     "cameo_title": "PRESIDENT_OF_THE_UNITED_STATES_"},
                                    no_cursor_timeout=True)
```


```
usage: buildCameo_Jrc_Bablenet_NameDataset.py [-h] [--config CONFIG]

Script to load CAMEO and JRC data and find their relation and store them in a
table.

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Location of Config File (default: ../config/config.cnf)

```