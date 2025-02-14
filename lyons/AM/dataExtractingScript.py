import xml.etree.ElementTree as ET
import os
import csv

# Define the lanes for each direction
LANE_GROUPS = {
    "Northbound": ["-14026336#4_0", "-14026336#3_0"],
    "Southbound": ["14026336#3_0", "14026336#4_0"],
    "Eastbound": ["683047946#5_0", "683047946#6_0"],
    "Westbound": ["-683047946#6_0", "-683047946#5_0"]
}

# Lane lengths (to calculate density properly)
LANE_LENGTHS = {
    "-14026336#4_0": 40, "-14026336#3_0": 40,
    "14026336#3_0": 40, "14026336#4_0": 40,
    "683047946#5_0": 109, "683047946#6_0": 109,
    "-683047946#6_0": 109, "-683047946#5_0": 109
}

def parse_detector_output(file):
    """Extract flow rate and density from detector_output.xml per lane"""
    tree = ET.parse(file)
    root = tree.getroot()

    # Store results by direction
    data = {direction: {"flow_rate": [], "density": []} for direction in LANE_GROUPS}

    for interval in root.findall("interval"):
        for lane in LANE_GROUPS:
            for lane_id in LANE_GROUPS[lane]:
                loop_data = interval.find(f".//*[@id='{lane_id}']")
                if loop_data is not None:
                    flow = float(loop_data.get("flow", 0))
                    occupancy = float(loop_data.get("occupancy", 0))
                    
                    # Convert occupancy (%) to vehicle density (vehicles/km)
                    lane_length = LANE_LENGTHS[lane_id]
                    density = (occupancy / 100) * (1000 / lane_length)

                    data[lane]["flow_rate"].append(flow)
                    data[lane]["density"].append(density)

    # Compute averages per direction
    results = {}
    for direction, values in data.items():
        avg_flow = sum(values["flow_rate"]) / len(values["flow_rate"]) if values["flow_rate"] else 0
        avg_density = sum(values["density"]) / len(values["density"]) if values["density"] else 0
        results[direction] = {"avg_flow": avg_flow, "avg_density": avg_density}

    return results

def parse_tripinfo(file):
    """Extract average inter-vehicular distance per direction"""
    tree = ET.parse(file)
    root = tree.getroot()

    # Store results by direction
    distance_data = {direction: [] for direction in LANE_GROUPS}

    for trip in root.findall("tripinfo"):
        if "routeLength" in trip.attrib:
            route_length = float(trip.get("routeLength", 0))
            assigned_direction = None

            # Assign trip to a direction based on its route
            for direction, lanes in LANE_GROUPS.items():
                if any(lane in trip.get("id", "") for lane in lanes):
                    assigned_direction = direction
                    break

            if assigned_direction:
                distance_data[assigned_direction].append(route_length)

    # Compute averages
    results = {}
    for direction, distances in distance_data.items():
        avg_distance = sum(distances) / len(distances) if distances else 0
        results[direction] = avg_distance

    return results

def extract_and_save_traffic_data():
    detector_file = "detector_output.xml"
    tripinfo_file = "tripinfo.xml"
    output_csv = "traffic_data.csv"

    if not os.path.exists(detector_file) or not os.path.exists(tripinfo_file):
        print("Error: Required output files not found. Run the SUMO simulation first.")
        return

    # Extract data
    detector_results = parse_detector_output(detector_file)
    tripinfo_results = parse_tripinfo(tripinfo_file)

    # Write to CSV
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Direction", "Average Flow Rate (veh/hr)", "Average Density (veh/km)", "Average Inter-Vehicular Distance (m)"])

        for direction in LANE_GROUPS:
            avg_flow = detector_results.get(direction, {}).get("avg_flow", 0)
            avg_density = detector_results.get(direction, {}).get("avg_density", 0)
            avg_distance = tripinfo_results.get(direction, 0)

            writer.writerow([direction, avg_flow, avg_density, avg_distance])

    print(f"Traffic data saved to {output_csv}")

if __name__ == "__main__":
    extract_and_save_traffic_data()
