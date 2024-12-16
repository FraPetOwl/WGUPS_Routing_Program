# main.py student ID:004928444
# Author: Peter Fraser
# Title: WGUPS Routing Program
# Submission 1:

import csv
import datetime
import package
import hash
import truck

# create instance of Hashmap
h = hash.HashMap()


# Loads the package data from the CSV into the hash map
def package_data_to_hashmap():
    print("Loading package data")
    with open("WGUPS Package File.csv") as packageCSV:
        read_package_csv = csv.reader(packageCSV, delimiter=',')
        next(read_package_csv)  # skips the header rows

        for row in read_package_csv:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            delivery_deadline = row[5]
            weight = int(row[6])
            special_notes = row[7]

            # Creates a package info object
            package_info = package.PackageInfo(package_id, address, city, state, zip_code, delivery_deadline, weight,
                                               special_notes)
            # Inserts into the hash map
            h.insert(package_id, package_info)
    print("Package data loaded\n")


# Load package object data to hash map
package_data_to_hashmap()


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


# Returns address of the closest package found - comparing to current address truck is at
# nearest neighbor algo

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


# Manually load trucks 1 and 2 based on WGUPS project requirements

truck1 = truck.Truck(truck_id=1,
                     speed=18,
                     current_location=hub,
                     time=datetime.timedelta(hours=8),
                     time_left_hub=datetime.timedelta(hours=8),
                     mileage=0.0,
                     packages=[1, 2, 13, 14, 15, 16, 19, 20, 23, 24, 29, 30, 31, 34, 37, 40])

truck2 = truck.Truck(truck_id=2,
                     speed=18,
                     current_location=hub,
                     time=datetime.timedelta(hours=9, minutes=5),
                     time_left_hub=datetime.timedelta(hours=9, minutes=5),
                     mileage=0.0,
                     packages=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 18, 25, 28, 32, 36, 38])


# Function to deliver packages, passing in specific truck with it's assigned list of packages

def truck_deliver_packages(delivery_truck):
    print(f"Truck #{delivery_truck.truck_id} starting delivery")
    # While there are packages in the truck, deliver until there are no more packages left in truck
    while delivery_truck.packages:

        # Find the package with the closest address in the list of truck packages
        closest_address = min_distance_from(delivery_truck.current_location, delivery_truck.packages)

        # Get the package info for this address stored in the hash map
        for package_id in delivery_truck.packages:
            package_info = h.get(package_id)
            package_info.delivery_status = "On Route"

            if delivery_truck.time >= datetime.timedelta(hours=10, minutes=20):
                if package_id == 9:
                    package_info.address, zip_code = "410 S State St", "84111"
                    h.insert(package_id, package_info)

            if package_info.address == closest_address:
                # Calculate the distance between current location and the closest address, then update mileage
                delivery_distance = distance_between(delivery_truck.current_location, closest_address)
                delivery_truck.mileage += delivery_distance

                # Calculate the time it takes to deliver the package and add it to total truck time
                time_to_deliver = datetime.timedelta(hours=delivery_distance / delivery_truck.speed)
                delivery_truck.time += time_to_deliver

                # Assign package to time it left the hub, it's delivery time, and update delivery status
                package_info.time_left_hub = delivery_truck.time_left_hub
                package_info.delivery_time = delivery_truck.time
                package_info.delivery_status = f"Delivered at {package_info.delivery_time}"

                h.insert(package_id, package_info)  # Update in hash table

                # Print delivery details
                print(f"Delivered package {package_id} to {closest_address} at {package_info.delivery_time}\n")

                # Remove the delivered package from the truck's package list
                delivery_truck.packages.remove(package_id)

                # Update truck's current location
                delivery_truck.current_location = closest_address

                # Break the loop after delivering one package (then find the next package)
                break
    else:
        print(f"Truck {delivery_truck.truck_id} out of packages to deliver.\n")


# Call trucks 1 and 2 to execute their delivery

truck_deliver_packages(truck1)
truck_deliver_packages(truck2)


# Returns trucks from its current location back to the hub and updates mileage/time/location.

def return_trucks_to_hub(delivery_truck):
    print(f"Returning truck {delivery_truck.truck_id} to the hub\n")

    return_distance = distance_between(delivery_truck.current_location, hub)
    delivery_truck.current_location = hub
    delivery_truck.mileage += return_distance

    time_to_return = datetime.timedelta(hours=return_distance / delivery_truck.speed)
    delivery_truck.time += time_to_return


return_trucks_to_hub(truck1)
return_trucks_to_hub(truck2)

# Check mileage after trucks deliver their first run

print(f"Truck 1 mileage:{truck1.mileage}\nTruck 2 mileage: {truck2.mileage}")
print(f"Total truck mileage after first run: {truck1.mileage + truck2.mileage}\n")

# Manually load remainder of packages into Truck 1 for a second delivery run

truck1.packages = [17, 21, 22, 26, 27, 33, 35, 39]
truck1.time_left_hub = truck1.time

truck_deliver_packages(truck1)
return_trucks_to_hub(truck1)

print("     Welcome to WGUPS Routing Program!\n")

def display_menu():
    print("*"*45)
    print((" " * 18) + "Menu")
    print("*********************************************\n"
          "1. Print All Package Status and Total Mileage\n"
          "2. Get a Single Package Status with a Time\n"
          "3. Get All Package Status with a Time\n"
          "4. Exit the Program\n"
          "*********************************************\n")


# Prints all packages and their final status with total mileage of trucks below

def print_all_package_status_and_mileage():
    for package_id in range(1, 41):
        print(h.get(package_id))
    print()

    print(f"Truck 1 mileage:{truck1.mileage:.2f}\nTruck 2 mileage: {truck2.mileage:.2f}")
    print(f"Total truck mileage: {truck1.mileage + truck2.mileage:.2f}\n")


# Prints a single package status for a package ID and a time given by the user

def get_single_package_status():
    try:
        package_id = int(input("\nEnter Package ID (1-40): "))

        time_input_str = input("Enter a time in HH:MM format: ")
        user_time = datetime.datetime.strptime(time_input_str, "%H:%M").time()
        user_timedelta = datetime.timedelta(hours=user_time.hour, minutes=user_time.minute)

        package_info = h.get(package_id)
        if package_info:
            # Compare the delivery time with the user input time
            if user_timedelta < package_info.time_left_hub:
                print(f"Package {package_id} status at {time_input_str}: At Hub")
                return
            elif package_info.time_left_hub <= user_timedelta < package_info.delivery_time:
                print(f"Package {package_id} status at {time_input_str}: On Route")
                return
            elif user_timedelta >= package_info.delivery_time:
                print(
                    f"Package {package_id} status at {time_input_str}: Delivered at {package_info.delivery_time}")
                return
            # If no status is determined, assume "At Hub"
            print(f"Package {package_id} status at {time_input_str}: At Hub")
        else:
            print("Invalid Package ID.")
    except Exception as e:
        print("Error:", e)


# Prints all package status for a specific time given by the user

def get_all_package_status():
    try:
        # Prompt user for a specific time
        time_input_str = input("Enter a time in HH:MM format: ")
        user_time = datetime.datetime.strptime(time_input_str, "%H:%M").time()
        user_timedelta = datetime.timedelta(hours=user_time.hour, minutes=user_time.minute)

        # Print header for output
        print("\nPackage Statuses at", time_input_str)
        print("-" * 30)
        print(f"{'Package ID':<12}{'Status':<15}")
        print("-" * 30)

        # Iterate through all package IDs in the hash table
        for package_id in range(1, 41):  # Assuming IDs range from 1 to 40
            package_info = h.get(package_id)
            if package_info:
                # Compare user time with package's times
                if user_timedelta < package_info.time_left_hub:
                    print(f"Package {package_id}: At Hub")
                elif package_info.time_left_hub <= user_timedelta < package_info.delivery_time:
                    print(f"Package {package_id}: On Route")
                elif user_timedelta >= package_info.delivery_time:
                    print(f"Package {package_id}: Delivered at {package_info.delivery_time}")
                else:
                    print(f"Package {package_id}: At Hub")  # Default case
            else:
                print(f"Package {package_id}: Not Found")

    except Exception as e:
        print("Error:", e)


def main():
    while True:
        display_menu()
        choice = input("Please make a selection (1-4): ")

        if choice == "1":
            print_all_package_status_and_mileage()
        elif choice == "2":
            get_single_package_status()
        elif choice == "3":
            get_all_package_status()
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


# Run the program
if __name__ == "__main__":
    main()

# Resources:
# Overall structure idea for classes / functions: Getting Started with the C950 code
# https://wgu.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=58db0088-cbce-469e-817c-ac9601692338
# For hashmap: https://www.youtube.com/watch?v=9HFbhPscPU0 as noted in email / helpful links
# 2d array/matrix for Distance data https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
# Nearest Neighbor Greedy Algorithm / Implementation
# https://srm--c.vf.force.com/apex/coursearticle?Id=kA03x000001DbBGCA0#
# Assistance for Prof. Khatri and Prof. Ferdinand
