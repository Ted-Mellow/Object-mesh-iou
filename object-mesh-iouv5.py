import bpy
import cv2
import numpy as np
import os

def calculate_iou(image, rendered_image):
    # Convert the images to float32 for accurate calculations
    image = image.astype(np.float32)
    rendered_image = rendered_image.astype(np.float32)

    # Calculate the intersection and union
    intersection = np.minimum(image, rendered_image)
    union = np.maximum(image, rendered_image)

    # Calculate the IOU
    iou = np.sum(intersection) / np.sum(union)

    return iou

def rotate_object(object_mesh, angle):
    # Select the object and make it active
    bpy.context.view_layer.objects.active = object_mesh
    object_mesh.select_set(True)

    # Set the object mode to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Rotate the object mesh
    object_mesh.rotation_euler[1] = np.radians(angle)

# Set the paths to the image and the object mesh
image_path = "/Users/ted/Desktop/Kaedim/Object-mesh-iou/cubetest.png"
mesh_path = "/Users/ted/Desktop/Kaedim/Object-mesh-iou/object-shape-iou.obj"

# Load the image
image = cv2.imread(image_path)

# Import the object mesh
bpy.ops.import_scene.obj(filepath=mesh_path)
object_mesh = bpy.context.selected_objects[0]

# Remove the default cube from the scene
bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)

max_iou = -1.0
max_angle = 0

for angle in range(0, 360, 45):
    # Reset the object's rotation
    object_mesh.rotation_euler[1] = 0

    # Rotate the object mesh
    rotate_object(object_mesh, angle)

    # Render the scene and obtain the rendered image
    bpy.ops.render.render(write_still=True)
    rendered_image_path = f"/Users/ted/Desktop/Kaedim/Object-mesh-iou/renders/rendered_image_{angle}.png"
    bpy.data.images["Render Result"].save_render(rendered_image_path)

    # Read the rendered image and check if it has non-zero pixels
    rendered_image = cv2.imread(rendered_image_path)
    if rendered_image is None or np.sum(rendered_image) == 0:
        print(f"Skipping angle {angle} - Empty rendered image")
        continue

    iou = calculate_iou(image, rendered_image)

    if iou > max_iou:
        max_iou = iou
        max_angle = angle

    print(f"Angle: {angle}, IoU: {iou}")

print("Maximum IoU:", max_iou)
print("Angle with Maximum IoU:", max_angle)
