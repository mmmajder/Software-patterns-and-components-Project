import json

from Core.models import Graph
from Core.services.interfaces import ILoader


class JSONLoader(ILoader):
    def __init__(self):
        self._nodes = {}  # id : attributes{}
        self._graph = Graph()
        self._id_counter = 0

    def name(self):
        return "JSON Loader"

    def identifier(self):
        return "json-basic-loader"

    def load(self, path):
        with open(path, "r") as f:
            root = json.load(f)
            root = self.configure_root(root)

            self._create_all_nodes(root)
            self._create_edges()

            return self._graph

    def _create_all_nodes(self, parent):
        self.add_references_attribute(parent)
        attributes_for_removal = []
        for attribute_key, attribute_value in parent.items():

            if isinstance(attribute_value, dict) and attribute_key != "references":
                attributes_for_removal.append(attribute_key)
                child = attribute_value
                self._set_references(child, parent)
                self._create_all_nodes(child)

            elif isinstance(attribute_value, list) and attribute_key != "references":
                attributes_for_removal.append(attribute_key)
                children = attribute_value
                for child in children:
                    self._create_all_nodes(child)

            elif isinstance(attribute_value, bool):
                    parent[attribute_key] = "bool=" + str(attribute_value)
            elif attribute_value is None:
                    parent[attribute_key] = "undefined"

        for attribute_key_for_removal in attributes_for_removal:
            del parent[attribute_key_for_removal]
        self._create_node(parent)

    def _create_node(self, attributes):
        if "id" not in attributes.keys():
            attributes["id"] = "id" + str(self._id_counter)
            self._id_counter += 1

        node_id = str(attributes["id"])
        node = self._graph.insert_node(node_id, attributes)
        if node is not None:
            self._nodes[node_id] = node


    def _create_edges(self):
        for node_id, node in self._nodes.items():
            if "references" in node.attributes.keys():
                for child_id in node.attributes["references"]:
                    child_node = self._nodes[child_id]
                    self._graph.insert_edge(node, child_node)
                del node.attributes["references"]

    def _set_references(self, child, parent):
        if "id" not in child.keys():
            child["id"] = "id" + str(self._id_counter)
            self._id_counter += 1

        if "references" in parent.keys():
            parent["references"].append(str(child["id"]))
        else:
            parent["references"] = [str(child["id"])]

    @staticmethod
    def add_references_attribute(child_attributes):
        if "references" not in child_attributes.keys():
            child_attributes["references"] = []

    # ROOT
    def configure_root(self, root):
        root["id"] = "root"
        roots_children = list(root.values())[0]
        self._set_all_references(root, roots_children)
        return root

    def _set_all_references(self, child_attributes, attribute_value):
        for child in attribute_value:
            self._set_references(child, child_attributes)


if __name__ == '__main__':
    loader = JSONLoader()
    graph = loader.load("test.json")

    print(len(graph.get_nodes()))
