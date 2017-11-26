# NSOne Asynchronous DNS Zone and Record Loading Tool using Twisted
![ScreenShot](https://raw.githubusercontent.com/humanalgorithm/nsone/master/nsone_screenshot.png)

## What is it? 
This tool uses the NSOne Python SDK to create DNS records with the help of Python's Twisted asynchronous library

## How does it work? 



## How to run?

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
