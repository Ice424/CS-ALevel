from PIL import Image
from typing import Literal

def image_sort(sort_type:Literal["Hue", "Lightness", "Saturation"],
               image_path="input.png", 
               output_path="output.png"):
    
    img = Image.open(image_path).convert("HSV")
    img = img.load()
    

if __name__ == "__main__":
    image_sort("Hue")