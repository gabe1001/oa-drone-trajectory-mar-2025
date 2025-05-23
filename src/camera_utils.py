"""Utility functions for the camera model.
"""
import numpy as np

from src.data_model import Camera

def compute_focal_length_in_mm(camera: Camera) -> np.ndarray:
    """Computes the focal length in mm for the given camera

    Args:
        camera (Camera): the camera model.

    Returns:
        np.ndarray: [fx, fy] in mm.
    """

    # Note(Ayush): Solution provided by project leader.
    pixel_to_mm_x = camera.sensor_size_x_mm / camera.image_size_x
    pixel_to_mm_y = camera.sensor_size_y_mm / camera.image_size_y

    return np.array([camera.fx * pixel_to_mm_x, camera.fy * pixel_to_mm_y])

def project_world_point_to_image(camera: Camera, point: np.ndarray) -> np.ndarray:
    """Project a 3D world point into the image coordinates.

    Args:
        camera (Camera): the camera model
        point (np.ndarray): the 3D world point

    Returns:
        np.ndarray: [u, v] pixel coordinates corresponding to the point.
    """
    fx = camera.fx
    fy = camera.fy
    cx = camera.cx
    cy = camera.cy

    X = point[0]
    Y = point[1]
    Z = point[2]

    x = fx * (X / Z)
    y = fy * (Y / Z)
    u = x + cx
    v = y + cy


    return np.array([u,v])


def compute_image_footprint_on_surface(camera: Camera, distance_from_surface: float) -> np.ndarray:
    """Compute the footprint of the image captured by the camera at a given distance from the surface.

    Args:
        camera (Camera): the camera model.
        distance_from_surface (float): distance from the surface (in m).

    Returns:
        np.ndarray: [footprint_x, footprint_y] in meters.
    """

    # Convert distance to mm
    distance_mm = distance_from_surface * 1000

    #Small Triangle: Base: sensor_size_x_mm Height: focal length
    #Big Triangle: Base: footprint_x_mm Height: distance_mm
    # triangles are similar, the ratios of their corresponding sides are equal
    # (sensor_size_x_mm) / focal length = (footprint_x_mm) / (distance_mm)
    focal_length_x = compute_focal_length_in_mm(camera)[0]  #convert focal length into mm
    focal_length_y = compute_focal_length_in_mm(camera)[1]

    # Compute the image footprint in mm
    footprint_x = (camera.sensor_size_x_mm * distance_mm) / focal_length_x
    footprint_y = (camera.sensor_size_y_mm * distance_mm) / focal_length_y


    return np.array([footprint_x/1000, footprint_y/1000]) # convert from millimeters to meters

def compute_ground_sampling_distance(camera: Camera, distance_from_surface: float) -> float:
    """Compute the ground sampling distance (GSD) at a given distance from the surface.

    Args:
        camera (Camera): the camera model.
        distance_from_surface (float): distance from the surface (in m).
    
    Returns:
        float: the GSD in meters (smaller among x and y directions).
    """

    smallest_gsd = distance_from_surface/ min(camera.fx, camera.fy)
    return smallest_gsd
