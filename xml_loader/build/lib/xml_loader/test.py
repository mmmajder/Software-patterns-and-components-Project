from xml_loader.xml_loader.XML_Loader import XML_Loader

if __name__ == '__main__':
    x = XML_Loader()
    g = x.load("../dataset/data.xml")
    print(g)