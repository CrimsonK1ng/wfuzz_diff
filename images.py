from PIL import Image, ImageChops
import os

def diff(img_file1, img_file2):
    """Diff images using Pillow (Pixel by pixel diff) probablytoo slow but what ever

    Args:
        img_file1 (str): image location 1 and ideally base image
        img_file2 (str): image location 2 
    """
    try:
        img1 = Image.open(img_file1)
    except Exception as e:
        print(f"Error processing image 1 {e}")
    try:
        img2 = Image.open(img_file2)
    except Exception as e:
        print(f"Error processing image 2 {e}")

    diff_cont =  ImageChops.difference(img1, img2)

    if not os.path.exists(os.path.join(os.getcwd(), "diffs")):
        os.mkdir("diffs")


    diff_img = diff_cont.convert("RGB")

    
    diff_img.save(os.path.join(os.getcwd(), "diffs", f"diff_{os.path.basename(img_file2)}"))
