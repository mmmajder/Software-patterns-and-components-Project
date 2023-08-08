# Graph representation app

Parsing json and xml data. Displaying graph data with Python D3 library.

App is divided in components:
- JSON loader
- XML loader
- Simple visualiser
- Complex visualiser

## Display
- Main screen
- Tree view - left side
- Bird view - right bottom corner

## Installation steps:

1. command to install Django
```bash
pip install Django
```

2. other requirements
```bash
pip install setuptools 

pip install jsonpickle #required for JSON Loader

pip install jinja2 # required for Visualisers
```
3. server parameters
```bash
python manage.py makemigrations

python manage.py migrate
```
4. command to install Core
```bash
python setup.py install
```
5. command to run server
```bash
python manage.py runserver
```
6. install plugins

 I) you can simply run script.ps1 by choosing 'Run with PowerShell' on right click;
	by doing this, you will run the app along with all 4 plugins 
	
II) you can position in file of plugin you want to install and run this command:
	python setup.py install

## Contributors
- Katarina Komad SW28/2019
- Aleksa Stanivuk SW29/2019
- Milan Ajder SW31/2019
- Andjela Miskovic SW33/2019
