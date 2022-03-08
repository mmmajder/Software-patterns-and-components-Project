from json_loader.json_loader.JSON_loader import JSONLoader

if __name__ == '__main__':
    loader = JSONLoader()
    graph = loader.load("../dataset/data.json")
    print(graph)
