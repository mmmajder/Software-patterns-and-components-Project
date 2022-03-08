import os

from Core.services.interfaces import IVisuliser
from django.shortcuts import render, redirect
from django.template import Template, Context

class SimpleVisualiser(IVisuliser):

    def __init__(self):
        pass

    def name(self):
        return "SimpleVisualiser"

    def identifier(self):
        return "sv"

    def visualise(self, graph):
        template_path = os.path.abspath("../simple_visualiser/implementation/templates/simple_visualiser.html")
        template_string = open(template_path).read() #file kao string
        context = Context({'graph':graph})
        temp = Template(template_string) #kreiranje template
        
        html = temp.render(context)

        return html

      