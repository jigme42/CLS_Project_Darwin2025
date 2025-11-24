import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.image as mpimg
from matplotlib.axes import Axes 

# --- Configuration --- #
output_plots_dir = 'plotty'
output_grouped_plots_dir = 'grouped_plotts'
data_dir = 'c'

os.makedirs(output_plots_dir, exist_ok=True)
os.makedirs(output_grouped_plots_dir, exist_ok=True)

# --- Data Loading --- #
print("Loading data...")
monthly_df = pd.read_csv(os.path.join(data_dir, 'Monthly_AllMetrics_WithWaterExtent.csv'))
seasonal_all_df = pd.read_csv(os.path.join(data_dir, 'Seasonal_AllMetrics_AllSeasons.csv'))
seasonal_anomalies_df = pd.read_csv(os.path.join(data_dir, 'Seasonal_AllMetrics_WithAnomalies.csv'))

# --- Data Preparation and Merging --- #
print("Performing data preparation and merging...")
monthly_df['date'] = pd.to_datetime(monthly_df['date'])
monthly_df['year'] = monthly_df['date'].dt.year

def get_season(month):
    if month in [12, 1, 2]:
        return 'Summer'
    elif month in [3, 4, 5]:
        return 'Autumn'
    elif month in [6, 7, 8]:
        return 'Winter'
    else:
        return 'Spring'

monthly_df['season'] = monthly_df['date'].dt.month.apply(get_season)

# Aggregate monthly water extent to seasonal
seasonal_water_extent = monthly_df.groupby(['year', 'season'])['annual_water_extent_km2'].mean().reset_index()

# Merge data
seasonal_all_df = pd.merge(seasonal_all_df, seasonal_water_extent, on=['year', 'season'], how='left')
seasonal_all_df.to_csv(os.path.join(data_dir, 'Seasonal_AllMetrics_Merged.csv'), index=False)

# Add anomalies
seasonal_anomalies_df = pd.merge(seasonal_anomalies_df, seasonal_water_extent, on=['year', 'season'], how='left')
seasonal_anomalies_df = seasonal_anomalies_df.sort_values(by=['year', 'season']).reset_index(drop=True)
seasonal_anomalies_df['annual_water_extent_km2_trend'] = seasonal_anomalies_df.groupby('season')['annual_water_extent_km2_y'].transform(
    lambda x: x.rolling(window=3, center=True, min_periods=1).mean()
)
seasonal_anomalies_df['annual_water_extent_km2_anomaly'] = (
    seasonal_anomalies_df['annual_water_extent_km2_y'] - seasonal_anomalies_df['annual_water_extent_km2_trend']
)

seasonal_anomalies_df.to_csv(os.path.join(data_dir, 'Seasonal_AllMetrics_WithAnomalies.csv'), index=False)

print("Data preparation and merging complete.")

# --- Plotting Functions --- #
print("Generating individual plots...")

def plot_monthly_timeseries(df, metric, title, filename):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y=metric, data=df, errorbar=None)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(metric.replace('_', ' ').title())
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_plots_dir, filename))
    plt.close()

def plot_seasonal_trends(df, metric, title, filename):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='year', y=metric, hue='season', data=df, marker='o', errorbar=None)
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(metric.replace('_', ' ').title())
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_plots_dir, filename))
    plt.close()

def plot_correlation(df, x_metric, y_metric, title, filename):
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=x_metric, y=y_metric, data=df)
    sns.regplot(x=x_metric, y=y_metric, data=df, scatter=False, color='red')
    plt.title(title)
    plt.xlabel(x_metric.replace('_', ' ').title())
    plt.ylabel(y_metric.replace('_', ' ').title())
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_plots_dir, filename))
    plt.close()

# Generate plots
plot_monthly_timeseries(monthly_df, 'mean_evi', 'Monthly EVI Time Series', 'monthly_evi_timeseries.png')
plot_monthly_timeseries(monthly_df, 'mean_precip', 'Monthly Precipitation Time Series', 'monthly_precip_timeseries.png')
plot_monthly_timeseries(monthly_df, 'annual_water_extent_km2', 'Monthly Water Extent Area Time Series', 'monthly_water_extent_timeseries.png')

plot_seasonal_trends(seasonal_all_df, 'mean_evi', 'Seasonal EVI Trends', 'seasonal_evi_lines.png')
plot_seasonal_trends(seasonal_all_df, 'mean_precip', 'Seasonal Precipitation Trends', 'seasonal_precip_lines.png')
plot_seasonal_trends(seasonal_all_df, 'mean_groundwater', 'Seasonal Groundwater Trends', 'seasonal_groundwater_lines.png')
plot_seasonal_trends(seasonal_all_df, 'annual_water_extent_km2', 'Annual Water Extent Trends', 'seasonal_water_extent_lines.png')

plot_correlation(seasonal_anomalies_df, 'evi_anomaly', 'gw_anomaly', 'EVI Anomaly vs. Groundwater Anomaly Scatter Plot', 'corr_monthly_evi_gw_anomaly.png')
plot_correlation(seasonal_anomalies_df, 'evi_anomaly', 'annual_water_extent_km2_anomaly', 'EVI Anomaly vs Water Extent Anomaly', 'corr_monthly_evi_water_extent_anomaly.png')

print("Individual plots generated successfully.")

# --- Grouped Plotting --- #
print("Generating grouped plots...")

def create_grouped_plot(image_paths, output_filename, title, layout=(1, 1), figsize=(15, 10)):
    fig, axes = plt.subplots(layout[0], layout[1], figsize=figsize)

    # Ensure axes is iterable
    if isinstance(axes, Axes):
        axes = [axes]
    else:
        axes = axes.ravel()

    for i, img_path in enumerate(image_paths):
        img = mpimg.imread(img_path)
        axes[i].imshow(img)
        axes[i].axis("off")

    for j in range(len(image_paths), len(axes)):
        fig.delaxes(axes[j])

    fig.suptitle(title, fontsize=16)
    plt.tight_layout(rect=(0, 0.03, 1, 0.95))
    plt.savefig(output_filename)
    plt.close()

# Group plots
monthly_timeseries_plots = [
    os.path.join(output_plots_dir, "monthly_evi_timeseries.png"),
    os.path.join(output_plots_dir, "monthly_precip_timeseries.png"),
    os.path.join(output_plots_dir, "monthly_water_extent_timeseries.png")
]
create_grouped_plot(
    monthly_timeseries_plots,
    os.path.join(output_grouped_plots_dir, "grouped_monthly_timeseries.png"),
    "Monthly Time Series: EVI, Precipitation, and Water Extent",
    layout=(3, 1),
    figsize=(10, 18)
)

seasonal_trends_plots = [
    os.path.join(output_plots_dir, "seasonal_evi_lines.png"),
    os.path.join(output_plots_dir, "seasonal_precip_lines.png"),
    os.path.join(output_plots_dir, "seasonal_groundwater_lines.png"),
    os.path.join(output_plots_dir, "seasonal_water_extent_lines.png")
]
create_grouped_plot(
    seasonal_trends_plots,
    os.path.join(output_grouped_plots_dir, "grouped_seasonal_trends.png"),
    "Seasonal Trends: EVI, Precipitation, Groundwater, and Water Extent",
    layout=(2, 2),
    figsize=(18, 12)
)

correlation_plots = [
    os.path.join(output_plots_dir, "corr_monthly_evi_gw_anomaly.png"),
    os.path.join(output_plots_dir, "corr_monthly_evi_water_extent_anomaly.png")
]
create_grouped_plot(
    correlation_plots,
    os.path.join(output_grouped_plots_dir, "grouped_correlation_plots.png"),
    "Correlation Plots: EVI Anomaly vs. Groundwater and Water Extent Anomalies",
    layout=(1, 2),
    figsize=(20, 8)
)

print("All analysis and plotting complete. Check the 'plotty' and 'grouped_plotts' directories.")
