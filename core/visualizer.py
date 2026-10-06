"""
core/visualizer.py
==================
TOPIC USED:
- Array Computing (NumPy):
    * 1D Arrays: Vectorized Mean, Median, Standard Deviation (np.std), Min, Max
    * 2D Arrays & Matrices: 2D column stacking (np.column_stack) for multi-dimensional speed/duration efficiency index
- Curve Plotting (Matplotlib):
    * Bar charts comparing actual dispatch duration vs. benchmark target
    * Polynomial fitting (np.polyfit, np.polyval) to plot continuous response trend curves
    * Figure styling, axes labels, legends, and saving to disk

WHERE IT CONNECTS:
- Connected to 'run.py' (Option 4) to output terminal analytics and generate 'data/performance_curve.png'.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def compute_fleet_statistics(response_intervals: list) -> dict:
    """
    TOPIC: NumPy 1D & 2D Vector/Matrix Computing
    Calculates key statistical metrics across response intervals.
    """
    if not response_intervals:
        response_intervals = [7.5, 9.2, 5.8, 12.1, 8.4, 6.6, 10.5]

    # NumPy 1D Array
    num_array = np.array(response_intervals, dtype=np.float64)

    mean_duration = float(np.mean(num_array))
    median_duration = float(np.median(num_array))
    std_deviation = float(np.std(num_array))
    fastest_time = float(np.min(num_array))
    longest_time = float(np.max(num_array))

    # NumPy 2D Matrix Computing: Combine duration with computed speed factor
    speed_vector = 60.0 / (num_array / 60.0 + 0.1)
    stats_matrix = np.column_stack((num_array, speed_vector))
    efficiency_index = float(np.mean(stats_matrix[:, 1]) / mean_duration)

    return {
        "count": len(response_intervals),
        "mean_min": round(mean_duration, 2),
        "median_min": round(median_duration, 2),
        "std_dev": round(std_deviation, 2),
        "min_min": round(fastest_time, 2),
        "max_min": round(longest_time, 2),
        "efficiency": round(efficiency_index, 2)
    }


def render_trend_curve(response_times: list, save_file: str = "data/performance_curve.png") -> str:
    """
    TOPIC: Matplotlib Curve Plotting & Polynomial Regression
    Generates a response time chart and saves to PNG file.
    """
    os.makedirs(os.path.dirname(save_file), exist_ok=True)
    if not response_times or len(response_times) < 2:
        response_times = [7.2, 11.5, 5.8, 9.4, 14.1, 6.3, 10.2, 8.0]

    labels = [f"Case-{i+1}" for i in range(len(response_times))]
    actual_values = np.array(response_times)
    standard_target = np.full(len(response_times), 8.0)

    plt.figure(figsize=(8.5, 4.4), facecolor="#0f172a")
    ax = plt.subplot(1, 1, 1)
    ax.set_facecolor("#1e293b")

    x_indices = np.arange(len(labels))
    bar_width = 0.35

    ax.bar(x_indices - bar_width/2, actual_values, bar_width, label='Actual Time (min)', color='#38bdf8', alpha=0.9)
    ax.bar(x_indices + bar_width/2, standard_target, bar_width, label='Target Benchmark (8 min)', color='#f43f5e', alpha=0.7)

    # Polynomial Curve Fitting
    smooth_x = np.linspace(0, len(labels)-1, 50)
    polynomial_weights = np.polyfit(x_indices, actual_values, 2)
    smooth_y = np.polyval(polynomial_weights, smooth_x)
    ax.plot(smooth_x, smooth_y, color='#fbbf24', linestyle='--', linewidth=2, label='Polynomial Response Curve')

    ax.set_title("Fleet Dispatch Response Benchmark & Trend", color="#f8fafc", fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel("Incident Sequence", color="#94a3b8", fontsize=10)
    ax.set_ylabel("Response Time (Minutes)", color="#94a3b8", fontsize=10)
    ax.set_xticks(x_indices)
    ax.set_xticklabels(labels, color="#cbd5e1", fontsize=9)
    ax.tick_params(colors="#cbd5e1")
    ax.grid(color="#334155", linestyle=":", alpha=0.6)

    legend = ax.legend(facecolor="#1e293b", edgecolor="#334155")
    for text_elem in legend.get_texts():
        text_elem.set_color("#f8fafc")

    plt.tight_layout()
    plt.savefig(save_file, dpi=120, bbox_inches='tight')
    plt.close()
    return save_file
