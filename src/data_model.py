"""Data models for the camera and user specification."""
from dataclasses import dataclass

@dataclass
class Camera:
    """
    Data model for a simple pinhole camera.
    
    Attributes:
        focal length along x axis (in pixels)
        focal length along y axis (in pixels)
        optical center of the image along the x axis (in pixels)
        optical center of the image along the y axis (in pixels)
        Size of the sensor along the x axis (in mm)
        Size of the sensor along the y axis (in mm)
        Number of pixels in the image along the x axis
        Number of pixels in the image along the y axis
        
    References: 
    - https://github.com/colmap/colmap/blob/3f75f71310fdec803ab06be84a16cee5032d8e0d/src/colmap/sensor/models.h#L220
    - https://en.wikipedia.org/wiki/Pinhole_camera_model
    """
    fx: float
    fy: float
    cx: float
    cy: float
    sensor_size_x_mm: float
    sensor_size_y_mm: float
    image_size_x: int
    image_size_y: int


@dataclass
class DatasetSpec:
    """
    Data model for specifications of an image dataset.
    Attributes:
        Overlap: the ratio (in 0 to 1) of scene shared between two consecutive images (Unitless).
        Sidelap: ratio (in 0 to 1) of scene shared between two images in adjacent rows (Unitless).
        Height: above the ground (in meters).
        Scan dimension X: the horizontal size of the rectangle to be scanned (in meters).
        Scan dimension Y: the vertical size of the rectangle to be scanned (in meters).
        Exposure Time: for each image (in milliseconds).

    """
    overlap: float
    sidelap: float
    height: float
    scan_dimension_x: int
    scan_dimension_y: int
    exposure_time_ms: int
    def __str__(self):
        return f"Overlap {self.overlap}, Sidelap {self.sidelap}, Height {self.height}, Scan dimension X {self.scan_dimension_x}, Scan dimension Y {self.scan_dimension_y}, Exposure Time {self.exposure_time_ms}"


@dataclass
class Waypoint:
    """
    Waypoints are positions where the drone should fly to and capture a photo.
    For Nadir scans (looking straight down), this position defines the
    camera's location in the world coordinate system.

    Attributes:
        x: The x-coordinate of the waypoint (in meters).
        y: The y-coordinate of the waypoint (in meters).
        z: The z-coordinate (height) of the waypoint (in meters).
        speed: Maximum allowed drone speed (meters/second) 
               during photo capture at this waypoint to prevent motion blur.
    """
    x: float
    y: float
    z: float
    speed: float