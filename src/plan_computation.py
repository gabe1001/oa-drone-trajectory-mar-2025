import typing as T
import math

import numpy as np

from src.data_model import Camera, DatasetSpec, Waypoint
from src.camera_utils import compute_image_footprint_on_surface, compute_ground_sampling_distance


def compute_distance_between_images(camera: Camera, dataset_spec: DatasetSpec) -> np.ndarray:
    """Compute the distance between images in the horizontal and vertical directions for specified overlap and sidelap.

    Args:
        camera (Camera): Camera model used for image capture.
        dataset_spec (DatasetSpec): user specification for the dataset.

    Returns:
        float: The distance between images in the horizontal direction.
        float: The distance between images in the vertical direction.
    """
    footprint_x = compute_image_footprint_on_surface(camera, dataset_spec.height)[0]
    footprint_y = compute_image_footprint_on_surface(camera, dataset_spec.height)[1]

    overlap = dataset_spec.overlap
    sidelap = dataset_spec.sidelap

    distance_x = footprint_x * (1 - overlap)
    distance_y = footprint_y * (1 - sidelap)

    return np.array([distance_x, distance_y])


def compute_speed_during_photo_capture(camera: Camera, dataset_spec: DatasetSpec, allowed_movement_px: float = 1) -> float:
    """Compute the speed of drone during an active photo capture to prevent more than 1px of motion blur.

    Args:
        camera (Camera): Camera model used for image capture.
        dataset_spec (DatasetSpec): user specification for the dataset.
        allowed_movement_px (float, optional): The maximum allowed movement in pixels. Defaults to 1 px.

    Returns:
        float: The speed at which the drone should move during photo capture.
    """
    gsd = compute_ground_sampling_distance(camera, dataset_spec.height)
    max_distance_meters = gsd * allowed_movement_px
    # Get exposure time in seconds
    exposure_time_s = dataset_spec.exposure_time_ms / 1000.0

    # Calculate max speed
    max_speed_mps = max_distance_meters / exposure_time_s

    return max_speed_mps # meters per second

def generate_photo_plan_on_grid(camera: Camera, dataset_spec: DatasetSpec) -> T.List[Waypoint]:
    """Generate the complete photo plan as a list of waypoints in a lawn-mower pattern.

    Args:
        camera (Camera): Camera model used for image capture.
        dataset_spec (DatasetSpec): user specification for the dataset.

    Returns:
        List[Waypoint]: scan plan as a list of waypoints.

    """
    photo_plan: T.List[Waypoint] = []
    scan_dim_x = dataset_spec.scan_dimension_x
    scan_dim_y = dataset_spec.scan_dimension_y
    height = dataset_spec.height

    ideal_distance_x, ideal_distance_y = compute_distance_between_images(camera, dataset_spec)
    capture_speed = compute_speed_during_photo_capture(camera, dataset_spec)

    #Determine Number of Rows and Columns
    # If dimension is zero, we need 1 photo in that dimension
    num_cols = 1 if scan_dim_x == 0 else math.ceil(scan_dim_x / ideal_distance_x) + 1
    num_rows = 1 if scan_dim_y == 0 else math.ceil(scan_dim_y / ideal_distance_y) + 1

    # Handle cases where scan dimension is smaller than ideal distance -> still need 2 points minimum usually
    num_intervals_x = 0 if scan_dim_x == 0 else math.ceil(scan_dim_x / ideal_distance_x)
    num_cols = num_intervals_x + 1

    num_intervals_y = 0 if scan_dim_y == 0 else math.ceil(scan_dim_y / ideal_distance_y)
    num_rows = num_intervals_y + 1

    actual_distance_x = 0.0
    if num_cols > 1:
        actual_distance_x = scan_dim_x / (num_cols - 1)

    actual_distance_y = 0.0
    if num_rows > 1:
        actual_distance_y = scan_dim_y / (num_rows - 1)

    # Generate Waypoints with Lawn Mower Pattern
    for r in range(num_rows):
        y_coord = r * actual_distance_y

        # Determine direction based on row index
        if r % 2 == 0:
            # Even row: Left-to-Right
            x_coords = [c * actual_distance_x for c in range(num_cols)]
        else:
            # Odd row: Right-to-Left
            x_coords = [scan_dim_x - (c * actual_distance_x) for c in range(num_cols)]

        # Create waypoints for the current row
        for x_coord in x_coords:
            z_coord = height # Constant height for all waypoints
            waypoint = Waypoint(x=x_coord, y=y_coord, z=z_coord, speed=capture_speed)
            photo_plan.append(waypoint)

    return photo_plan