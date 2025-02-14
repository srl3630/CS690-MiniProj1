import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('lyons_Night.rou.xml')
root = tree.getroot()

# Find all 'trip' elements
trips = root.findall('trip')

# Sort the trips by the 'depart' attribute (convert to float for proper sorting)
sorted_trips = sorted(trips, key=lambda trip: float(trip.get('depart')))

# Clear the original trips and add the sorted trips
root.clear()  # Clear the root to remove all children
for trip in sorted_trips:
    root.append(trip)

# Write the sorted XML back to a new file
tree.write('sorted_lyons_Night.rou.xml', encoding='utf-8', xml_declaration=True)

print("XML file sorted and saved as 'sorted_lyons_Night.rou.xml'.")