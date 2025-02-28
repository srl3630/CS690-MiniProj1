import os
import pandas as pd

def parse_filename(filename):
    """Extracts time of day, traffic light cycle time, and signal actuation from the filename."""
    parts = filename.split("_")
    time_of_day = parts[0]  # AM, PM, LT
    cycle_time = parts[1]  # 70, 90, 110
    signal_actuation = "On" if "SAtrue" in parts[2] else "Off"
    return time_of_day, cycle_time, signal_actuation

def process_csv_files(directory, output_file):
    """Reads all CSV files in the directory, extracts data, adds parameters, and writes to a final file."""
    all_data = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv") and filename != output_file:
            file_path = os.path.join(directory, filename)
            
            time_of_day, cycle_time, signal_actuation = parse_filename(filename)
            
            df = pd.read_csv(file_path)
            df["Time of Day"] = time_of_day
            df["Traffic Light Cycle Time"] = cycle_time
            df["Signal Actuation"] = signal_actuation
            
            all_data.append(df)
    
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv(os.path.join(directory, output_file), index=False)
    print(f"Final dataset saved as {output_file}")

# Run the script
directory_path = "./"  # Change this if needed
output_filename = "final_data.csv"
process_csv_files(directory_path, output_filename)