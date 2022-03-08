from setuptools import setup, find_packages

setup(
    name="xml-loader",
    version="0.1",
    packages=find_packages(),
    namespace_packages=["xml_loader"],
    entry_points={
        'loader':
            ['xml_loader=xml_loader.XML_Loader:XML_Loader'],
    },
    zip_safe=True
)
