from setuptools import setup, find_packages
setup(
    name="simple_visualiser",
    version="0.1",
    packages=find_packages(),
    namespace_packages=["implementation"],
    entry_points = {
        'visualiser':
            ['simple_visualiser=implementation.simple_visualiser:SimpleVisualiser'],
    },
    zip_safe=True, 
    install_requires=['Jinja2']
)