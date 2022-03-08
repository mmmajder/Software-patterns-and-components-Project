class Graph(object):
    def __init__(self):
        self._outgoing = {}  # {node1 : [edge1, ...], ...}
        self._incoming = {}
        self._node_by_id = {}

    def get_root(self):
        return list(self.get_nodes())[0]

    def get_node_by_id(self, id):
        try:
            return self._node_by_id[id]
        except:
            return None

    def get_nodes(self):
        return self._node_by_id.values()

    def get_edge(self, source_node, destination_node):
        for edge in self._outgoing[source_node]:
            if edge.destination == destination_node:
                return edge
        return None

    def insert_existing_node(self, node):
        self._outgoing[node] = []
        self._incoming[node] = []
        self._node_by_id[node.id] = node
        return node

    def insert_node(self, node_id, attributes):
        node = Node(node_id, attributes)
        self._outgoing[node] = []
        self._incoming[node] = []
        self._node_by_id[node_id] = node
        return node

    def insert_edge(self, source, destination):
        if self.get_edge(source, destination) is not None:
            raise ValueError('source and destination are already adjacent')
        e = Edge(source, destination)
        self._outgoing[source].append(e)
        self._incoming[destination].append(e)
        source.children.append(destination)

    def __str__(self):
        ret = ""
        for node in self._outgoing.keys():
            ret += str(node)
            for edge in self._outgoing[node]:
                ret += "\t" + str(edge) + "\n"
            ret += "\n"
        return ret

    def remove_node(self, node_id):
        v = self.get_node_by_id(node_id)
        if not v:
            return
        del (self._outgoing[v])
        del (self._incoming[v])
        for node, edges in self._outgoing.items():
            deleting = []
            i = 0
            for edge in edges:
                if edge.destination.id == node_id:
                    deleting.append(i)
                i += 1
            for d in deleting:
                del (self._outgoing[node][d])
        self.clear_children(node_id)
        self._node_by_id[node_id].children.clear()
        del (self._node_by_id[node_id])

    def clear_children(self, node_id):
        n = self.get_node_by_id(node_id)
        if not n:
            return
        for node in self.get_nodes():
            if n in node.children:
                node.children.remove(n)

    def remove_nodes_by_id(self, node_ids):
        for node_id in node_ids:
            self.remove_node(node_id)
        return self

    def get_root_nodes(self):
        roots = []

        for id in self.get_root_node_ids():
            roots.append(self.get_node_by_id(id))

        return roots

    def get_root_node_ids(self):
        # gets ids of all nodes
        nodeIds = self.get_node_ids()
        # iterates through all nodes
        # if the node is someone's child
        # it can not be considered 
        # one of the roots
        for node in self.get_nodes():
            for child in node.children:
                print(child.id)
                if child.id in nodeIds:
                    print("obisao child id " + child.id)
                    nodeIds.remove(child.id)
                    print(nodeIds)

        return nodeIds

    def get_node_ids(self):
        nodeIds = []

        for node in self.get_nodes():
            nodeIds.append(node.id)

        return set(nodeIds)

    def get_path_to_node_from_roots(self, id):
        for rootId in self.get_root_node_ids():
            path = self.get_path_to_node(rootId, id)

            if path != None and id in path:
                return path

        return None

    def get_path_to_node(self, startId, endId, path=[]):
        path = path + [startId]
        print(path)
        if startId == endId:
            return path

        node = self.get_node_by_id(startId)
        if len(node.children) == 0:
            return None

        for child in node.children:
            if child.id not in path:  # fights infinite recursion
                new_path = self.get_path_to_node(child.id, endId, path)
                if new_path:
                    return new_path

        return None

class Edge(object):
    __slots__ = '_source', '_destination'

    def __init__(self, source, destination):
        self._source = source
        self._destination = destination

    @property
    def source(self):
        return self._source

    @property
    def destination(self):
        return self._destination

    def endpoints(self):
        return self._source, self._destination

    def opposite(self, v):
        if not isinstance(v, Node):
            raise TypeError('v must be a Node')

        if v is self._source:
            return self._destination

        elif v is self._destination:
            return self._source
        else:
            raise ValueError('v not incident to edge')

    def __hash__(self):  # will allow edge to be a map/set key
        return hash((self._source, self._destination))

    def __eq__(self, other):
        if self._source.id == other.source.id and self._destination == other.destination.id:
            return True
        return False

    def __str__(self):
        return '({0}-{1})'.format(self._source.id, self._destination.id)


class Node(object):
    def __init__(self, id, attributes=None):
        if attributes is None:
            attributes = {}
        self._attributes = attributes
        self._children = []
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def children(self):
        return self._children

    @property
    def attributes(self):
        return self._attributes

    def add_attribute(self, key, value):
        self._attributes[key] = value

    def add_child(self, child):
        self._children.append(child)

    def __hash__(self):  # will allow vertex to be a map/set key
        return hash(self.id)

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def __str__(self):
        retVal = ""
        if not self._attributes:
            return retVal
        for key in self._attributes.keys():
            retVal += str(key) + ":" + str(self._attributes.get(str(key))) + "\n"
        return retVal
