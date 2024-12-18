class Truck:
    def __init__(self, truck_id, speed, current_location, time, time_left_hub, mileage, packages):
        self.truck_id = truck_id
        self.speed = speed
        self.current_location = current_location
        self.time = time
        self.time_left_hub = time_left_hub
        self.mileage = mileage
        self.packages = packages

    def __str__(self):
        return (f"Truck ID: {self.truck_id}, Speed: {self.speed} mph, Current Location: {self.current_location}, "
                f"Time: {self.time}, "
                f"Time Left Hub: {self.time_left_hub}, Total Miles: {self.mileage}, Packages: {self.packages}")
