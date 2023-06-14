import bpy
import cv2
import numpy as np
import math

def calculate_iou(image_path, mesh_object):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Get the object's mesh vertices
    mesh_vertices = np.array(mesh_object.data.vertices)

    # Calculate the bounding box of the object
    min_x = min(mesh_vertices[:, 0])
    max_x = max(mesh_vertices[:, 0])
    min_y = min(mesh_vertices[:, 1])
    max_y = max(mesh_vertices[:, 1])

    # Resize the image to match the bounding box size
    resized_image = cv2.resize(image, (max_x - min_x + 1, max_y - min_y + 1))

    # Calculate the intersection over union (IoU)
    intersection = np.sum(np.logical_and(resized_image, mesh_object))
    union = np.sum(np.logical_or(resized_image, mesh_object))
    iou = intersection / union

    return iou

def rotate_object(mesh_object, angle):
    # Convert the angle to radians
    angle_rad = math.radians(angle)

    # Set the rotation axis (Z-axis in this case)
    rotation_axis = (0, 0, 1)

    # Set the rotation center to the object's origin
    rotation_center = mesh_object.location

    # Apply the rotation
    bpy.context.view_layer.objects.active = mesh_object
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    bpy.ops.transform.rotate(value=angle_rad, orient_axis=rotation_axis, center_override=rotation_center)
    bpy.context.view_layer.update()

def find_max_iou_rotation(image_path, mesh_object):
    max_iou = -1
    max_angle = 0

    for angle in range(0, 360, 45):
        rotate_object(mesh_object, angle)
        iou = calculate_iou(image_path, mesh_object)

        if iou > max_iou:
            max_iou = iou
            max_angle = angle

        # Reset the object's rotation
        rotate_object(mesh_object, -angle)

    return max_angle

# Example usage
image_path = "/path/to/your/image.png"  # Replace with the path to your image
mesh_object = bpy.context.object  # Assuming the desired mesh object is currently selected

iou = calculate_iou(image_path, mesh_object)
print("Intersection over Union (IoU):", iou)

max_angle = find_max_iou_rotation(image_path, mesh_object)
print("Maximum IoU rotation angle:", max_angle)