class HashMap:
    # initializes hash map to a list of 10 with the value none
    def __init__(self):
        self.size = 10
        self.map = [None] * self.size

    # Generates a hash value for a given key using the sum of ASCII values of the key's characters
    def get_hash(self, key):
        hashed_index = 0
        for char in str(key):
            hashed_index += ord(char)
        return hashed_index % self.size

    # Adds a key-value pair to the hash map
    def insert(self, key, value):
        key_hash = self.get_hash(key)
        key_value_pair = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value_pair])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(key_value_pair)
            return True

    # Retrieves a value from the hash map based on the key
    def get(self, key):
        key_hash = self.get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    # Deletes a key-value pair from the hash map
    def delete(self, key):
        key_hash = self.get_hash(key)

        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    # Prints the contents of the hash map
    def print(self):
        print('---Hashmap---')
        for item in self.map:
            if item is not None:
                for pair in item:  # Handling the list of key-value pairs
                    print(f"Package ID: {pair[0]}, Package Info: {pair[1]}")
            else:
                print("Empty slot")  # To see empty hash slots