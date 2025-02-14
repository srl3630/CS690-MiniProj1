import xml.etree.ElementTree as ET
import math

# Define the lanes for each direction
LANE_GROUPS = {
    "Northbound": ["nb_1", "nb_2"],
    "Southbound": ["sb_1", "sb_2"],
    "Eastbound": ["eb_1", "eb_2"],
    "Westbound": ["wb_1", "wb_2"]
}

# Lane lengths (to calculate density properly)
LANE_LENGTHS = {
    "nb_1": 40, "nb_2": 40,
    "sb_1": 40, "sb_2": 40,
    "eb_1": 109, "eb_2": 109,
    "wb_1": 109, "wb_2": 109
}

LANE_IDS = {
    "nb_1": "-14026336#4_0", "nb_2": "-14026336#3_0",
    "sb_1": "14026336#3_0", "sb_2": "14026336#4_0",
    "eb_1": "683047946#5_0", "eb_2": "683047946#6_0",
    "wb_1": "-683047946#6_0", "wb_2": "-683047946#5_0"
}

def calculate_distance(x1, y1, x2, y2):
    """Compute Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def detect_lane_orientation(vehicle_positions):
    """Determine if a lane is horizontal, vertical, or diagonal based on vehicle positions."""
    x_values = [pos[0] for pos in vehicle_positions]
    y_values = [pos[1] for pos in vehicle_positions]

    x_range = max(x_values) - min(x_values) if len(x_values) > 1 else 0
    y_range = max(y_values) - min(y_values) if len(y_values) > 1 else 0

    if x_range > y_range:
        return "horizontal"
    elif y_range > x_range:
        return "vertical"
    else:
        return "diagonal"

# Load FCD XML file
tree = ET.parse('fcd.xml')
root = tree.getroot()

# Dictionary to store vehicle data per timestep
time_data = {}

# Parse XML data
for timestep in root.findall('timestep'):
    time = float(timestep.get('time'))
    lane_vehicles = {}

    # For all vehicles in the timestep
    for vehicle in timestep.findall('vehicle'):
        # Get the vehicle's ID, position, and lane
        veh_id = vehicle.get('id')
        x, y = float(vehicle.get('x')), float(vehicle.get('y'))
        length = float(vehicle.get('length'))  
        lane = vehicle.get('lane')  

        # Store vehicle data by lane
        if lane not in lane_vehicles:
            lane_vehicles[lane] = []
        lane_vehicles[lane].append((veh_id, x, y, length))

    # Store lane data by timestep
    time_data[time] = lane_vehicles
    
# Compute inter-vehicular distance per lane
for time, lane_vehicles in time_data.items():
    # For each lane, compute inter-vehicular distance at the current timestep
    for lane, vehicles in lane_vehicles.items():
        if len(vehicles) < 2:
            continue  # Skip if there are no vehicle pairs to compare
        
        # Determine vehicle comparison order based on lane orientation
        lane_orientation = detect_lane_orientation([(x, y) for _, x, y, _ in vehicles])
        