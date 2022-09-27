import os
from Core.services.interfaces import IVisuliser
from jinja2 import Template

class ComplexVisualiser(IVisuliser):
    def __init__(self):
        pass

    def name(self) -> str:
        return "Complex visualiser"

    def identifier(self) -> str:
        return "cv"

    def visualise(self, graph) -> str:
        template_path = os.path.abspath("../complex_visualiser/complex_visualiser/templates/complex_visualiser.html")
        template_string = open(template_path).read()
        temp = Template(template_string)
        return temp.render(graph=graph)

