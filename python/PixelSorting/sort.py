from PIL import Image
from typing import Literal




def sort_func(e):
    return e[0]

def image_sort(sort_type:Literal["Hue", "Lightness", "Saturation"],
               image_path="input.jpg", 
               output_path="output2.png"):
    

    
    im = Image.open(image_path).convert("HSV")
    img = im.load()
    width, height = im.size

    imlist:list[list] = []
    sortedlist:list[list] = []
    fullimage:list = []
    
    for i in range(width):
        imlist.append([])
        sortedlist.append([])
        for j in range(height):
            imlist[i].append(img[i,j])
            fullimage.append(img[i,j])
    
    for i in range(width):
        sortedlist[i] = imlist[i].copy()
        sortedlist[i].sort(key = sort_func)
    
    newimage = Image.new("HSV", (width,height))
    newerimage = Image.new("HSV", (width,height))

    for i in range(width):
        for j in range(height):
            newimage.putpixel((i,j), sortedlist[i][j])
            newerimage.putpixel((i,j), fullimage[i+j])
    
    newimage = newimage.convert("RGBA")
    newimage.save(output_path)
    
    newerimage = newerimage.convert("RGBA")
    newerimage.save("full.png")
    
    #print(newimage)
if __name__ == "__main__":
    image_sort("Lightness")