from datetime import datetime
import time

class Transaction:
    
    def __init__(self, initdata={}):
        if initdata:
            assert type(initdata) is dict
        self.timestamp = initdata.get('timestamp')
        self.description = initdata.get('description')
        self.modified = initdata.get('modified')
        self.tags = initdata.get('tags', [])
        self.ledger = initdata.get('ledger')
        self.errors = []

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = self._create_timestamp(value, "timestamp")

    @property
    def modified(self):
        return self._modified

    @modified.setter
    def modified(self, value):
        self._modified = self._create_timestamp(value, "modified")
    
    def is_valid(self):
        """
        Validate a transaction
        """
        try:
            assert all(k in self.__dict__.keys() for k in ['_timestamp'])
            assert type(self.timestamp) is int and self.timestamp >= 0
            assert self.description is None or type(self.description) is str
            assert type(self.modified) is int and self.modified >= 0
            assert type(self.tags) is list
        except AssertionError as err:
            self.error = err
            return False

        return True

    @staticmethod
    def _create_timestamp(value, variable):
        if type(value) == int:
            return value
        elif type(value) == datetime:
            return int(value.timestamp())
        elif type(value) == float:
            return int(value)
        elif value == None:
            return None
        else:
            raise TypeError("{} should be a datetime, float, or int".format(variable))

    def asdict(self):
        return {
            "timestamp": self.timestamp,
            "modified": self.modified,
            "ledger": self.ledger,
            "description": self.description,
            "tags": self.tags
        }
