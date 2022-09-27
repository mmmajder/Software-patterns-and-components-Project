import xml.etree.ElementTree as ElemTree

from Core.models import Graph
from Core.services.interfaces import ILoader


class XML_Loader(ILoader):
    def __init__(self):
        pass

    def name(self):
        return 'XML Loader'

    def identifier(self):
        return 'xml-loader'

    def load(self, path):
        XMLtree = ElemTree.parse(path)

        # check if empty file
        if len(XMLtree.getroot().getchildren()) == 0:
            return Graph()

        graph = Graph()
        self.parse_XMLtree_to_graph_recursion(XMLtree.getroot(), None, graph, True)
        self.add_references_to_grapf(graph)
        return graph

    def parse_XMLtree_to_graph_recursion(self, root, child, graph, first):
        if first:
            parent = graph.insert_node("Root", root.attrib)
        else:
            parent = child
        for c in root.getchildren():
            id = self.has_id(c)
            if not id:
                if c.text.strip():
                    parent.add_attribute(c.tag, c.text)
            else:
                child_element = graph.insert_node(id, c.attrib)
                graph.insert_edge(parent, child_element)
                self.parse_XMLtree_to_graph_recursion(c, child_element, graph, False)

    def has_id(self, c):
        if "id" in c.attrib.keys():
            return c.attrib["id"]
        for t in c.getchildren():
            if t.tag == 'id':
                return t.text
        return None

    def add_references_to_grapf(self, graph):
        for node in graph.get_nodes():
            if "reference" in node.attributes.keys():
                for neighbor_id in node.attributes["reference"].split(" "):
                    if neighbor_id != '':
                        node2 = graph.get_node_by_id(neighbor_id)
                        graph.insert_edge(node, node2)
                del node.attributes["reference"]
