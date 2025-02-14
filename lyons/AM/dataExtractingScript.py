import os
import traci
import xml.etree.ElementTree as ET


def parse_detector_data(detector_file):
    """Extracts flow rate and density from detector XML output."""
    tree = ET.parse(detector_file)
    root = tree.getroot()
    total_flow = 0
    total_occupancy = 0
    count = 0
    
    for interval in root.findall('interval'):
        total_flow += float(interval.get('flow', 0))
        total_occupancy += float(interval.get('occupancy', 0))
        count += 1
    
    avg_flow_rate = total_flow / count if count > 0 else 0
    avg_density = total_occupancy / count if count > 0 else 0
    
    return avg_flow_rate, avg_density

def parse_trip_data(trip_file):
    """Extracts average inter-vehicular distance from trip XML output."""
    tree = ET.parse(trip_file)
    root = tree.getroot()
    total_distance = 0
    vehicle_count = 0
    
    for trip in root.findall('tripinfo'):
        total_distance += float(trip.get('routeLength', 0))
        vehicle_count += 1
    
    avg_distance = total_distance / vehicle_count if vehicle_count > 0 else 0
    return avg_distance

def extract_metrics(detector_file='detector_output.xml', trip_file='tripinfo.xml'):
    if not os.path.exists(detector_file) or not os.path.exists(trip_file):
        print("Error: Missing detector or trip output files.")
        return
    
    avg_flow_rate, avg_density = parse_detector_data(detector_file)
    avg_inter_vehicle_distance = parse_trip_data(trip_file)
    
    print(f"Average Flow Rate: {avg_flow_rate} vehicles/hour")
    print(f"Average Vehicular Density: {avg_density} %")
    print(f"Average Inter-Vehicular Distance: {avg_inter_vehicle_distance} meters")
    
    return avg_flow_rate, avg_density, avg_inter_vehicle_distance

if __name__ == "__main__":
    extract_metrics()
