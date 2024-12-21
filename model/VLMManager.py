import base64
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection, AutoImageProcessor
import io
from PIL import Image
import torch
from typing import List
from torchvision.ops import box_convert
import cv2
import numpy as np
import threading


class VLMManager:    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        checkpoint = "owlv2-p16-ensemble"
        self.processor = AutoProcessor.from_pretrained(checkpoint)

        # Load the model and tokenizer
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(
            checkpoint,
            ignore_mismatched_sizes=True,
            device_map=self.device,
        )
        self.processor = AutoProcessor.from_pretrained(
            checkpoint,
            device_map=self.device,
        )

    def identify(self, image: bytes, caption: str, sector_bbox: list) -> List[int]:
        im = Image.open(io.BytesIO(image))

        # text prompts
        inputs = self.processor(text=[caption], images=im, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            target_sizes = torch.tensor([im.size[::-1]])
            results = self.processor.post_process_object_detection(
                outputs, threshold=0.3, target_sizes=target_sizes
            )[0]
        print(results)
        bboxes = results["boxes"].tolist()
        scores = results["scores"].tolist()
        labels = results["labels"].tolist()
        labels_replaced = []
        for label in labels:
            labels_replaced.append(caption[label])
        max_score_box = []
        max_score = 0.0
        for i, score in enumerate(scores):
            if score > max_score:
                max_score = score
                max_score_box = bboxes[i]
                

        
        try:
            # Draw bboxes and save image
            iou_threshold = 0.3
            clean_bbox, clean_labels = non_maximum_suppression_with_labels(bboxes, list(map(str, labels_replaced)), iou_threshold)

            result = draw_bbox_with_labels(
                image_path="pleasework.jpg",
                bboxes=clean_bbox,
                labels=clean_labels,
                output_path="output_image.jpg"
            )
            
            def show_image(image):
                cv2.imshow("Output Image", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            threading.Thread(target=show_image, args=(result,)).start()

            
        except Exception as e:
            print(f"Error: {e}")
        # Post Processing 
        count_valid_empty_seats = 0 
        # if clean_bbox is in sector_bbox, increase the count
        for bbox in clean_bbox:
            if bbox[0] >= sector_bbox[0] and bbox[1] >= sector_bbox[1] and bbox[2] <= sector_bbox[2] and bbox[3] <= sector_bbox[3]:
                count_valid_empty_seats += 1
        
        return count_valid_empty_seats
def draw_bbox(image_path, bboxes, output_path, color=(0, 255, 0), thickness=2):
    """
    Draw bounding boxes on an image and save it
    
    Parameters:
    - image_path: str, path to input image
    - bboxes: list of [x1, y1, x2, y2] coordinates
    - output_path: str, path to save output image
    - color: tuple, BGR color for bbox (default: green)
    - thickness: int, line thickness of bbox
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read the image")
    
    # Make a copy to draw on
    output_image = image.copy()
    
    # Draw each bounding box
    for bbox in bboxes:
        x1, y1, x2, y2 = map(int, bbox)  # Convert coordinates to integers
        
        # Draw rectangle
        cv2.rectangle(output_image, (x1, y1), (x2, y2), color, thickness)
    
    # Save the output image
    cv2.imwrite(output_path, output_image)
    return output_image


import numpy as np

def non_maximum_suppression_with_labels(bboxes, labels, iou_threshold=0.1):
    print("labels" ,labels)
    """
    Filters overlapping bounding boxes using Non-Maximum Suppression (NMS) and adjusts labels to match.

    Parameters:
        bboxes (list of lists or np.ndarray): Array of bounding boxes in the format [x1, y1, x2, y2].
        labels (list or np.ndarray): Array of labels corresponding to the bounding boxes.
        iou_threshold (float): IoU threshold for filtering overlapping boxes. Default is 0.1.

    Returns:
        tuple: Filtered list of bounding boxes and their corresponding labels.
    """
    if len(bboxes) == 0:
        return [], []

    # Ensure bboxes and labels are numpy arrays
    bboxes = np.array(bboxes, dtype=float)
    labels = np.array(labels)

    # Extract coordinates
    x1 = bboxes[:, 0]
    y1 = bboxes[:, 1]
    x2 = bboxes[:, 2]
    y2 = bboxes[:, 3]

    # Calculate areas of the bounding boxes
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)

    # Sort boxes by their top-left x-coordinate (arbitrary sorting criterion)
    order = np.argsort(x1)

    # Lists to hold the filtered boxes and labels
    filtered_bboxes = []
    filtered_labels = []

    while order.size > 0:
        # Index of the current box
        i = order[0]
        filtered_bboxes.append(bboxes[i])
        filtered_labels.append(labels[i])

        # Compute IoU of the current box with the rest
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        # Calculate width and height of the intersection
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # Calculate Intersection over Union (IoU)
        intersection = w * h
        iou = intersection / (areas[i] + areas[order[1:]] - intersection)

        # Retain boxes with IoU less than the threshold
        remaining = np.where(iou < iou_threshold)[0]
        order = order[remaining + 1]

    return np.array(filtered_bboxes), np.array(filtered_labels)

def draw_bbox_with_labels(image_path, bboxes, labels, output_path, color=(0, 255, 0), thickness=2):
    """
    Draw bounding boxes with labels on an image and save it
    
    Parameters:
    - image_path: str, path to input image
    - bboxes: list of [x1, y1, x2, y2] coordinates
    - labels: list of strings, labels for each bbox
    - output_path: str, path to save output image
    - color: tuple, BGR color for bbox (default: green)
    - thickness: int, line thickness of bbox
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read the image")
    
    # Make a copy to draw on
    output_image = image.copy()
    
    # Font settings
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    
    # Draw each bounding box with label
    for bbox, label in zip(bboxes, labels):
        x1, y1, x2, y2 = map(int, bbox)
        
        # Draw rectangle
        cv2.rectangle(output_image, (x1, y1), (x2, y2), color, thickness)
        
        # Get label size
        (label_width, label_height), baseline = cv2.getTextSize(
            label, font, font_scale, font_thickness
        )
        
        # Draw label background
        cv2.rectangle(
            output_image,
            (x1, y1 - label_height - baseline),
            (x1 + label_width, y1),
            color,
            cv2.FILLED
        )
        
        # Draw label text
        cv2.putText(
            output_image,
            label,
            (x1, y1 - baseline),
            font,
            font_scale,
            (0, 0, 0),  # Black text
            font_thickness
        )
    
    # Save the output image
    cv2.imwrite(output_path, output_image)
    return output_image
