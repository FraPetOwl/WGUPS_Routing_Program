class PackageInfo:
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight, special_notes, assigned_truck):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline  # EOD or specific time
        self.weight = weight  # in Kilos
        self.special_notes = special_notes  # package delay / address correction / package grouping
        self.assigned_truck = assigned_truck
        self.delivery_status = "At Hub"
        self.delivery_time = None
        self.time_left_hub = None

    def __str__(self):
        return (f"ID: {self.package_id}, Assigned Truck: {self.assigned_truck}, Address: {self.address}, {self.city}, "
                f"{self.state}, {self.zip_code}, Deadline: {self.delivery_deadline}, Weight: {self.weight}, "
                f"Notes: {self.special_notes}, Delivery Status: {self.delivery_status}, Delivery Time: {self.delivery_time}")
