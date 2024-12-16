class PackageInfo:
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight, special_notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline  # EOD or specific time
        self.weight = weight  # in Kilos
        self.special_notes = special_notes  # assignment to truck #, package delay, address correction, package grouping
        self.delivery_status = "At Hub"
        self.delivery_time = None
        self.time_left_hub = None

    def __str__(self):
        return (f"ID: {self.package_id}, Address: {self.address}, {self.city}, {self.state}, {self.zip_code}, "
                f"Deadline: {self.delivery_deadline}, Weight: {self.weight}, Notes: {self.special_notes},"
                f"Delivery Status: {self.delivery_status}, Delivery Time: {self.delivery_time}")
