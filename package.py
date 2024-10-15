class PackageInfo:
    def __init__(self, id, address, city, state, zip_code, delivery_deadline, weight, special_notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes

    def __str__(self):
        return f"ID: {self.id}, Address: {self.address}, {self.city}, {self.state}, {self.zip_code}, Deadline: {self.delivery_deadline}, Weight: {self.weight}, Notes: {self.special_notes}"