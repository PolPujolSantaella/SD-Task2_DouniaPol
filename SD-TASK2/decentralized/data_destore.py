class KeyValueStore:

    def __init__(self):
        self.keys_set = set()
        self.keys_dict = dict()

    def put(self, key, value):
        print(f'Received: {key}')
        self.keys_set.add(key)
        self.keys_dict[key] = value
        return True

    def get(self, key):
        if key not in self.keys_set:
            return "failed", False
        return self.keys_dict[key],True

    def doCommit(self, key, value):
        self.keys_set.add(key)
        self.keys_dict[key] = value
        return True

    def askVote(self, key):
        if key not in self.keys_set:
            return "failed"
        return self.keys_dict[key]

    def discover(self, port):
        print("Discovering: "+str(port))
        return self.keys_set

data_destore = KeyValueStore()
