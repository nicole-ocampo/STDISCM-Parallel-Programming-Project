from PIL import Image, ImageEnhance
import os

def load(filepath):
    images = []
    for filename in os.listdir(filepath):
        img = Image.open(os.path.join(filepath,filename))
        images.append(img)
    
    return images

def enhance_brightness(image, factor):
    return ImageEnhance.Brightness(image).enhance(factor)

def enhance_contrast(image, factor):
    return ImageEnhance.Contrast(image).enhance(factor)

def enhance_sharpness(image, factor):
    return ImageEnhance.Sharpness(image).enhance(factor)

if __name__ == "__main__":
    filepath = input("File directory for input images: ")
    outfilepath = input("File directory for output images: ")
    number_files = len(os.listdir(filepath))
    print(number_files)
    images = load(filepath)

    # brightness_enhancement_factor = input("Brightness Enhancement Factor: ")
    # sharpness_enhancement_factor = input("Sharpness Enhancement Factor: ")
    # contrast_enhancement_factor = input("Contrast Enhancement Factor: ")

    # image = Image.open("1.jpg")
    # image = enhance_brightness(image, float(brightness_enhancement_factor))
    # image = enhance_sharpness(image, float(sharpness_enhancement_factor))
    # image = enhance_contrast(image, float(contrast_enhancement_factor))
    i=0
    for image in images:
        format = str(i) + ".png"
        savepath = os.path.join(outfilepath, format) 
        image.save(savepath)
        i+=1
