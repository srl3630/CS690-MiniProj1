import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
df = pd.read_csv("final_data.csv")

# Convert categorical columns
df["Time of Day"] = df["Time of Day"].astype("category")
df["Signal Actuation"] = df["Signal Actuation"].astype("category")
df["Direction"] = df["Direction"].astype("category")

# Summary statistics
def summarize_data(df):
    summary = df.groupby(["Time of Day", "Traffic Light Cycle Time", "Signal Actuation"]).agg(
        avg_flow_rate=("Average Flow Rate (veh/hr)", "mean"),
        avg_density=("Average Density (veh/km)", "mean"),
        avg_inter_distance=("Average Inter-Vehicular Distance (m)", "mean")
    ).reset_index()
    return summary

summary_df = summarize_data(df)
summary_df.to_csv("sumo_analysis_summary.csv", index=False)
print(summary_df)

# Visualizing the effect of traffic light cycle time and actuation
metrics = ["avg_flow_rate", "avg_density", "avg_inter_distance"]
metric_titles = ["Flow Rate (veh/hr)", "Density (veh/km)", "Inter-Vehicular Distance (m)"]

for metric, title in zip(metrics, metric_titles):
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Traffic Light Cycle Time", y=metric, hue="Signal Actuation", data=summary_df)
    plt.title(f"Effect of Traffic Light Cycle Time and Signal Actuation on {title}")
    plt.xlabel("Traffic Light Cycle Time (s)")
    plt.ylabel(title)
    plt.legend(title="Signal Actuation")
    plt.savefig(f"sumo_{metric}_analysis.png")
    plt.show()

# Exploring AM vs PM vs Night traffic for different TLS timings
for metric, title in zip(metrics, metric_titles):
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Traffic Light Cycle Time", y=metric, hue="Time of Day", data=summary_df)
    plt.title(f"Comparison of AM, PM, and Night Traffic for {title}")
    plt.xlabel("Traffic Light Cycle Time (s)")
    plt.ylabel(title)
    plt.legend(title="Time of Day")
    plt.savefig(f"sumo_{metric}_time_comparison.png")
    plt.show()

# Save separate summary files
for time_of_day in df["Time of Day"].unique():
    filtered_df = summary_df[summary_df["Time of Day"] == time_of_day]
    filtered_df.to_csv(f"sumo_analysis_{time_of_day}.csv", index=False)
