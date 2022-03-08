from setuptools import setup, find_packages

setup(
    name="Core",
    version="0.1",
    packages=find_packages(),
    install_requires=['Django>=2.1', 'jsonpickle', 'jinja2'],

    package_data={'Core': ['static/*.css', 'static/*.js', 'static/*.html', 'static/images/*.png', 'templates/*.html']},
    zip_safe=False
)
