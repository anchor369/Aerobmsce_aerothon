import torch
import torchvision.transforms as T
import cv2
import numpy as np
from PIL import Image

# Load MiDaS
model_type = "DPT_Small"  # light for edge devices
midas = torch.hub.load("intel-isl/MiDaS", model_type)
midas.eval()

transform = torch.hub.load("intel-isl/MiDaS", "transforms").small_transform

def estimate_depth(frame, bbox):
    x1, y1, x2, y2 = [int(v) for v in bbox]
    region = frame[y1:y2, x1:x2]
    
    img = Image.fromarray(cv2.cvtColor(region, cv2.COLOR_BGR2RGB))
    input_batch = transform(img).unsqueeze(0)

    with torch.no_grad():
        prediction = midas(input_batch)
        depth_map = prediction.squeeze().cpu().numpy()

    avg_depth = np.median(depth_map)
    return avg_depth  # raw depth estimate, relative scale
