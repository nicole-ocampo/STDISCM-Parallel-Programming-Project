from PIL import Image, ImageEnhance
import os
import time
import psutil

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
    images = load(filepath)
    official_start = time.time()
    cpu_usage = []
    formats = []
    frames = []

    brightness_enhancement_factor = input("Brightness Enhancement Factor: ")
    sharpness_enhancement_factor = input("Sharpness Enhancement Factor: ")
    contrast_enhancement_factor = input("Contrast Enhancement Factor: ")

    # Output statistics file
    text_file_cont = []
    text_file_cont.append("Number of files enhanced: " + str(number_files))
    text_file_cont.append("Output directory: " + str(outfilepath))
    text_file_cont.append("------------------")

    i=0
    for image in images:
        start_time = time.time()
        format = image.filename[-4:]
        formats.append(format)
        frames.clear()

        if format != '.gif':
            image = enhance_brightness(image, float(brightness_enhancement_factor))
            image = enhance_sharpness(image, float(sharpness_enhancement_factor))
            image = enhance_contrast(image, float(contrast_enhancement_factor))
        else:
            for j in range(image.n_frames):
                image.seek(j)
                frame = image.copy()
                frame = frame.convert('RGB')
                frame = enhance_brightness(frame, float(brightness_enhancement_factor))
                frame = enhance_sharpness(frame, float(sharpness_enhancement_factor))
                frame = enhance_contrast(frame, float(contrast_enhancement_factor))
                frames.append(frame)


        end_time = time.time()
        elapsed_time = time.time()
        cpu_time = psutil.cpu_percent()
        cpu_usage.append(cpu_time)

        outformat = str(i) + format
        savepath = os.path.join(outfilepath, outformat) 

        text_file_cont.append("Image: " + str(image))
        text_file_cont.append("Output filename: " + str(savepath))
        text_file_cont.append("Start time: " + str(start_time) + " seconds")
        text_file_cont.append("End time: " + str(end_time) + " seconds")
        text_file_cont.append("Time elapsed: " + str(elapsed_time) + " seconds")
        text_file_cont.append("CPU Usage: " + str(cpu_time))
        text_file_cont.append("------------------")

        if format != '.gif':
            image.save(savepath)
        else:
            frames[0].save(savepath, save_all=True,
                           append_images=frames[1:], optimize=False, loop=0)
        
        print("Enhanced an image!")
        i+=1
    
    elapsed = time.time() - official_start
    ave_cpu = sum(cpu_usage) / len(cpu_usage)

    # Finalization
    print("--- Time elapsed: %s seconds ---" % (elapsed))
    print("--- Average CPU Usage: %s  ---" % (ave_cpu))
    with open('Statistics.txt', 'w') as f:
        for line in text_file_cont:
            f.write(line)
            f.write('\n')
        
        f.write("Total time elapsed: " + str(elapsed) + " seconds\n")
        f.write("Average CPU Usage: " + str(ave_cpu))

