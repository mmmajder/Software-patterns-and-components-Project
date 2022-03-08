cd "tim4Core"
python setup.py install
cd ..

cd "json_loader"
python setup.py install
cd ..

cd "xml_loader"
python setup.py install
cd ..

cd "simple_visualiser"
python setup.py install
cd ..

cd "complex_visualiser"
python setup.py install
cd ..

cd "tim4project"
python manage.py runserver

