import xml.etree.ElementTree as ET
import random

# Define the edges for AM (east/north) and PM (south/west) traffic flow
AM_EDGES = {
    "14027172#0", "-14026336#0", "-14026336#1", "14027172#1", "-14026336#1",  # Northbound
    "683044783#6", "683043808#0", "683044783#5", "683044783#4", "683044783#3", "683044783#2"  # Eastbound
}

PM_EDGES = {
    "-14027172#1", "-14027172#0", "14026336#0", "14026336#1",  # Southbound
    "-683043808#0", "-683044783#6", "-683044783#5", "-683044783#4", "-683044783#3", "-683044783#2"  # Westbound
}


# Function to filter trips while keeping 50% of the trips going in the wrong direction
def filter_trips_with_reduction(input_file, output_file, allowed_edges, reduction_percentage=50):
    tree = ET.parse(input_file)
    root = tree.getroot()

    trips = root.findall("trip")
    wrong_direction_trips = [trip for trip in trips if trip.get("to") not in allowed_edges]

    # Retain 50% of wrong-direction trips
    keep_wrong_direction_trips = random.sample(wrong_direction_trips,
                                               int(len(wrong_direction_trips) * (reduction_percentage / 100)))

    # Remove only the remaining 50% of wrong-direction trips
    for trip in wrong_direction_trips:
        if trip not in keep_wrong_direction_trips:
            root.remove(trip)

    tree.write(output_file)


# Apply filtering for AM and PM while retaining 50% of wrong-direction trips
filter_trips_with_reduction("lyons_AM.rou.xml", "lyons_AM.rou.xml", AM_EDGES, reduction_percentage=50)
filter_trips_with_reduction("lyons_PM.rou.xml", "lyons_PM.rou.xml", PM_EDGES, reduction_percentage=50)

print("✅ AM and PM traffic files updated: 50% of wrong-direction traffic retained.")


# Function to reduce traffic volume for night simulation
def reduce_traffic(input_file, output_file, percentage=20):
    tree = ET.parse(input_file)
    root = tree.getroot()

    trips = root.findall("trip")
    keep_trips = random.sample(trips, int(len(trips) * (percentage / 100)))

    # Remove all trips and add back only the selected ones
    for trip in trips:
        root.remove(trip)

    for trip in keep_trips:
        root.append(trip)

    tree.write(output_file)


# Reduce the number of trips to 20% for night traffic
reduce_traffic("lyons_Night.rou.xml", "lyons_Night.rou.xml", percentage=20)

print("✅ Night traffic file created successfully.")


# Function to count the number of trips in a .rou.xml file
def count_trips(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        num_trips = len(root.findall("trip"))
        return num_trips
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found.")
        return None
    except ET.ParseError:
        print(f"❌ Error: Could not parse {file_path}. Ensure it is a valid XML file.")
        return None


# Count trips in each file and print the results
trip_files = ["lyons_AM.rou.xml", "lyons_PM.rou.xml", "lyons_Night.rou.xml"]
trip_counts = {file: count_trips(file) for file in trip_files}

print("\n🚦 Traffic Statistics:")
for file, count in trip_counts.items():
    if count is not None:
        print(f"✅ {file}: {count} trips remaining.")
