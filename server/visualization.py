"""visualization.py - Visualization of sensor data."""

import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px

from constants import TIMESTAMP, TEMPERATURE, HUMIDITY, AQI, CO2, TVOC

COLORS = px.colors.qualitative.Plotly


def plot_data(data: list[dict]) -> str:
    """
    Plot sensor data using Plotly.

    Args:
        data (list[dict]): List of dictionaries containing sensor data.

    Returns:
        str: HTML code for the graph.

    Raises:
        KeyError: If a required key is missing from the data.
    """
    try:
        # Extract data by key
        times = [entry[TIMESTAMP] for entry in data]
        temperature = [entry[TEMPERATURE] for entry in data]
        humidity = [entry[HUMIDITY] for entry in data]
        aqi = [entry[AQI] for entry in data]
        co2 = [entry[CO2] for entry in data]
        tvoc = [entry[TVOC] for entry in data]
        # Create Plotly graphs
        temp_graph = generate_html(temperature, times, color=COLORS[1], label="Temperature (°C)")
        humidity_graph = generate_html(humidity, times, color=COLORS[0], label="Humidity (%)")
        aqi_graph = generate_html(aqi, times, color=COLORS[4], label="AQI (1-5)")
        co2_graph = generate_html(co2, times, color=COLORS[2], label="CO₂ (ppm)")
        tvoc_graph = generate_html(tvoc, times, color=COLORS[3], label="TVOC (mg/m³)")
        # Return graph HTML
        return f"{temp_graph}\n{humidity_graph}\n{co2_graph}\n{tvoc_graph}\n{aqi_graph}"
    # Handle errors in visualization
    except Exception as error: #pylint: disable=broad-except
        raise RuntimeError("Error occurred in generating visualization") from error


def generate_html(values: list, timestamps: list, label: str, color: str) -> str:
    """
    Generate a Plotly graph given a list of values, timestamps, title, and label.

    Args:
        values (list): List of values to plot.
        timestamps (list): List of timestamps to plot.
        title (str): Title of the graph.
        label (str): Label for the y-axis.

    Returns:
        str: HTML code for the graph.
    """
    # Create Plotly traces
    trace = go.Scatter(
        x=timestamps,
        y=values,
        mode='lines+markers',
        name=label,
        line=dict(color=color),
        marker=dict(color=color),
    )
    # Create subplots layout
    fig = go.Figure()
    fig.add_trace(trace)
    # Update layout
    fig.update_layout(
        title=f"📊 {label.split(' ')[0]} Data Overview",
        xaxis_title="Time",
        yaxis_title=label,
        template="plotly_white",
        hovermode="x unified"
    )
    # Generate graph HTML
    graph_html = pyo.plot(fig, output_type='div', include_plotlyjs='cdn')
    # Return graph HTML
    return graph_html
