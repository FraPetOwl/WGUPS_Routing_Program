# Author: Peter Fraser
# Student ID:004928444
# Title: WGUPS Routing Program
# Submission 1:

import csv
import datetime
from package import PackageInfo
from hash import HashMap
from truck import Truck

# create instance of Hashmap
h = HashMap()


# Loads the package data from the CSV into the hash map
def packageDataToHashMap():
    print("Loading package data")
    with open("WGUPS Package File.csv") as packageCSV:
        readPackageCSV = csv.reader(packageCSV, delimiter=',')
        next(readPackageCSV)  # skips the header rows

        for row in readPackageCSV:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            delivery_deadline = row[5]
            weight = int(row[6])
            special_notes = row[7]

            # Creates a package info object
            package_info = PackageInfo(package_id, address, city, state, zip_code, delivery_deadline, weight,
                                       special_notes)
            # Inserts into the hash map
            h.insert(package_id, package_info)
    print("Package data loaded\n")


# Call the function to load data
packageDataToHashMap()


def load_address_data():
    address_data_list = []
    # Read and append addresses to address_data list
    with open("addressCSV.csv") as address_file:
        reader = csv.reader(address_file)
        #       next(reader)  # Skip the header if needed
        for row in reader:
            address_data_list.append(row[2].strip())
    return address_data_list


address_data = load_address_data()
hub = address_data[0]
print(f"Address data:\n", address_data)
print()


def load_distance_data():
    # Initialize an empty matrix of 27x27 for all addresses
    rows, cols = 27, 27
    distance_data_list = [[0.0 for _ in range(cols)] for _ in range(rows)]

    with open("WGUPS Distance Table.csv") as distanceTable:
        read_distance_table = csv.reader(distanceTable, delimiter=',')
        next(read_distance_table)  # Skip the header row

        # Keeps track of which row (location within 2d list) we are processing
        for i, row in enumerate(read_distance_table):
            numeric_row = row[2:]  # Skip first two columns (address info)

            for j, miles in enumerate(numeric_row):
                if miles:  # Only if the entry has a value
                    distance_data_list[i][j] = float(miles)
                    distance_data_list[j][i] = float(miles)  # Mirror the distance value
    return distance_data_list


distance_data = load_distance_data()
print(f"Distance data:\n", distance_data)
print()


# Given two address strings, returns the distance between them

def distance_between(address1, address2):
    # Find the indices of the two addresses
    index1 = address_data.index(address1)
    index2 = address_data.index(address2)
    # Access the distance between the two addresses using distance_data
    return distance_data[index1][index2]


# Returns string of the closest package address found from the current address (for nearest neighbor)


def min_distance_from(from_address, truck_packages):
    # Initialize variables
    min_distance = float('inf')
    closest_address = None
    # Loop through each package in the truck's package list
    for package_id in truck_packages:
        # Get the address associated with the current package
        package_address = h.get(package_id).address

        # Calculate distance between the current address and package address
        calculated_distance = distance_between(from_address, package_address)

        # If this distance is smaller than the current minimum, update min_distance and closest_address
        if calculated_distance < min_distance:
            min_distance = calculated_distance
            closest_address = package_address
            print(f"New closest address: {closest_address}, Distance: {min_distance}")
    return closest_address


# Manually load trucks 1 and 2 based on requirements
truck1 = Truck(speed=18,
               current_location=hub,
               time=datetime.timedelta(hours=8),
               time_left_hub=datetime.timedelta(hours=8),
               mileage=0.0,
               packages=[1, 2, 13, 14, 15, 16, 19, 20, 23, 24, 29, 30, 31, 34, 37, 40])

truck2 = Truck(speed=18,
               current_location=hub,
               time=datetime.timedelta(hours=9, minutes=5),
               time_left_hub=datetime.timedelta(hours=9, minutes=5),
               mileage=0.0,
               packages=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 18, 25, 28, 32, 36, 38])


def truck_deliver_packages(truck):
    # While there are packages in the truck, deliver until there are no more packages left in truck
    while truck.packages:
        # Find the package with the closest package in the list of truck packages
        closest_address = min_distance_from(truck.current_location, truck.packages)

        # Get the package info for this address
        for package_id in truck.packages:
            package_info = h.get(package_id)
            if package_info.address == closest_address:
                # Calculate the distance between current location and the closest address
                delivery_distance = distance_between(truck.current_location, closest_address)

                # Update mileage
                truck.mileage += delivery_distance

                # Calculate the time it takes to deliver package
                time_to_deliver = datetime.timedelta(hours=delivery_distance / truck.speed)
                truck.time += time_to_deliver

                # Update package status to "Delivered" in the HashMap FIX after I give packages their delivery status
                package_info.delivery_deadline = f"Delivered at {truck.time}"
                h.insert(package_id, package_info)  # Update in hash table

                # Print delivery details (optional)
                print(f"Delivered package {package_id} to {closest_address} at {truck.time}\n")

                # Remove the delivered package from the truck's package list
                truck.packages.remove(package_id)

                # Update truck's current location
                truck.current_location = closest_address

                # Break the loop after delivering one package (to find the next closest)
                break


# Call trucks 1 and 2 to execute their delivery

truck_deliver_packages(truck1)
truck_deliver_packages(truck2)

# Check mileage after trucks deliver

print(f"Truck 1 mileage:{truck1.mileage}\nTruck 2 mileage: {truck2.mileage}")
print(f"Total truck mileage: {truck1.mileage + truck2.mileage}\n")


# Manually return trucks from its current location back to the hub.
# And update mileage/time/location.
def return_trucks_to_hub(truck):
    print("Returning truck to the hub")

    return_distance = distance_between(truck.current_location, hub)
    truck.mileage += return_distance
    time_to_return = datetime.timedelta(hours=return_distance / truck.speed)
    truck.time += time_to_return
    truck.current_location = hub


return_trucks_to_hub(truck1)
return_trucks_to_hub(truck2)

# Manually load remainder of packages.

truck1 = Truck(speed=18,
               current_location=truck1.current_location,
               time=truck1.time,
               time_left_hub=truck1.time,
               mileage=truck1.mileage,
               packages=[17, 21, 22, 26, 27, 33, 35, 39])

truck_deliver_packages(truck1)
return_trucks_to_hub(truck1)
# call return to hub for truck 1 to update and get final tally

print(f"Truck 1 mileage:{truck1.mileage}\nTruck 2 mileage: {truck2.mileage}")
print(f"Total truck mileage: {truck1.mileage + truck2.mileage}\n")

# Resources:
# Overall structure idea for classes / functions: Getting Started with the C950 code - https://wgu.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=58db0088-cbce-469e-817c-ac9601692338
# For hashmap: https://www.youtube.com/watch?v=9HFbhPscPU0 as noted in email / helpful links
# 2d array/matrix for Distance data https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
# Nearest Neighbor Greedy Algorithm / Implementation https://srm--c.vf.force.com/apex/coursearticle?Id=kA03x000001DbBGCA0#
# Assistance for Prof. Khatri and Prof. Ferdinand
