class Truck:
    def __init__(self, speed, current_location, time, time_left_hub, mileage, packages):
        self.speed = speed
        self.current_location = current_location
        self.time = time
        self.time_left_hub = time_left_hub
        self.mileage = mileage
        self.packages = packages

    # list of integers which rep the packages from hash table, have all delayed packages go out first
    def __str__(self):
        return (f"Speed: {self.speed} mph, Current Location: {self.current_location}, Time: {self.time}, "
                f"Time Left Hub: {self.time_left_hub}, Total Miles: {self.mileage}, Packages: {self.packages}")
