from setuptools import setup, find_packages

setup(
    name="json-loader",
    version="0.1",
    packages=find_packages(),
    namespace_packages=["json_loader"],
    entry_points={
        'loader':
            ['json_loader=json_loader.JSON_loader:JSONLoader'],
    },
    zip_safe=True
)
