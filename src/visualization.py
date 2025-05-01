"""Utility to visualize photo plans.
"""

import typing as T

import plotly.graph_objects as go

from src.data_model import Waypoint


def plot_photo_plan(photo_plans: T.List[Waypoint]) -> go.Figure:
    """Plot the photo plan on a 2D grid.

    Args:
        photo_plans (T.List[Waypoint]): List of waypoints for the photo plan.

    Returns:
        T.Any: Plotly figure object.
    """
    # Extract X and Y coordinates from the list of Waypoint objects
    x_coords = [wp.x for wp in photo_plans]
    y_coords = [wp.y for wp in photo_plans]
    # Z (height) and speed remain constant
    z_coord = photo_plans[0].z
    capture_speed = photo_plans[0].speed

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='lines+markers', # Show lines connecting points and markers at points
        marker=dict(symbol='arrow', size=10, angleref='previous', color='MediumPurple'), # Customize marker style
        line=dict(width=2, color='LightSkyBlue'),
        name='Flight Path'
    ))

    plot_title = (
        f"Drone Flight Plan<br>"
        f"<sup>Height (Z): {z_coord:.2f}m | Capture Speed: {capture_speed:.2f} m/s</sup>"
    )

    fig.update_layout(
        title=plot_title, 
        xaxis_title='X-coordinate (m)',
        yaxis_title='Y-coordinate (m)',
        yaxis_scaleanchor='x',
        yaxis_scaleratio=1,
        hovermode='closest',
    )

    return fig
