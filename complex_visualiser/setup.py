from setuptools import setup, find_packages
setup(
    name="complex_visualiser",
    version="0.1",
    packages=find_packages(),
    namespace_packages=["complex_visualiser"],
    entry_points = {
        'visualiser':
            ['complex_visualiser=complex_visualiser.complex_visualiser:ComplexVisualiser'],
    },
    zip_safe=True,
    install_requires=['Jinja2']
)