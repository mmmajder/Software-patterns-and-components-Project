from abc import abstractmethod, ABCMeta


class ServiceBase(metaclass=ABCMeta):
    @abstractmethod
    def identifier(self):
        pass

    @abstractmethod
    def name(self):
        pass


class ILoader(ServiceBase):

    @abstractmethod
    def load(self, path):
        pass


class IVisuliser(ServiceBase):

    @abstractmethod
    def visualise(self, graph):
        pass
