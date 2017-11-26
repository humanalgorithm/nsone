# NSOne Asynchronous DNS Zone and Record Loading Tool using Twisted
![ScreenShot](https://raw.githubusercontent.com/humanalgorithm/nsone/master/nsone_screenshot.png)

## What is it? 
This tool uses the NSOne Python SDK to create DNS records with the help of Python's Twisted asynchronous library

## How does it work? 
The script will loop through every line in the provided CSV file(located in /data). For each line it will use the NSOne SDK to see if an associated zone already exists, if so it can use the preexisting zone to add record to the zone, if not it will create a new zone. 

Each request for zone is made asynchronously using Twisted and returns a deferred object. Call backs are used to capture flow of the program when the asynchronous requests return.  

Most of the asynchronous DSN processing logic takes place in record_processing.py and zone_processing.py located within nsone/dns_processing directory

## How to run?
Once repo is cloned and requirements are installed:
From the /nsone folder:
```
python -m run.import_zones
```

## Turning on and off logging:
The logger class within nsone/shared/logger.py is configurable to turn off logging throughout the tool. If you wish to turn off any of the logging for a specific part of the program just change the corresponding value False. 
```
class Logger(object):
        ...
        log_config = {
            "record_update":  True,
            "record_create":  True,
            "record_load": True,
            "zone_update": True,
            "zone_create":  True,
            "zone_load": True,
            "record_request_create": True,
            "record_request_update": True,
            "record_request_load": True,
            "zone_request_load": True,
            "zone_request_create": True,
            "existing_answers": True
        }
```


## How to setup? 

1) Setup a virtualenv:
```
virtualenv <your_env_folder_name> --no-site-packages
```
2) cd into the folder you just created
```
cd <your_env_folder_name>
```
3) Activate the virtual env
On Windows:
```
cd Scripts
activate.bat
```
On Linux:
```
source bin/activate
```

4) git clone this repo
From within your_env_folder_name
```
git clone <clone link for this repo>
```

5) Install requriements
cd into cloned folder
```
cd nsone
```
install requirements
```
pip install -r requirements.txt
```

6) Run script using -m switch
From the /nsone directory
```
python -m run.import_zones
```
