# Libraries for parallelism and concurrency
import multiprocessing
import time

# Libraries for tasks
import os
from PIL import Image, ImageEnhance

class Producer(multiprocessing.Process):
    def __init__(self, filepath, semaphore, buffer):
        multiprocessing.Process.__init__(self)
        self.filepath = filepath
        self.semaphore = semaphore
        self.buffer = buffer

    def run(self):
        print("Producer is waking up...")
        for filename in os.listdir(self.filepath):
            img = Image.open(os.path.join(self.filepath,filename))
            self.buffer.append(img)
            self.semaphore.release()
            print("Producer appended an image to the shared resource buffer")
    

class Consumer(multiprocessing.Process):
    def __init__(self, number_files, outfilepath, semaphore, buffer, brightness_factor, sharpness_factor, contrast_factor):
        multiprocessing.Process.__init__(self)
        self.number_files = number_files
        self.outfilepath = outfilepath
        self.semaphore = semaphore
        self.buffer = buffer
        self.brightness_factor = float(brightness_factor)
        self.sharpness_factor = float(sharpness_factor)
        self.contrast_factor = float(contrast_factor)

        self.item = Image.new(mode="RGB", size=(200, 200))


    def run(self):
        print("Consumer is waking up...")
        for i in range(self.number_files):
            self.semaphore.acquire()
            if self.buffer:
                self.item = self.buffer.pop()
                self.item = self.enhance_brightness(self.item, self.brightness_factor)
                self.item = self.enhance_sharpness(self.item, self.sharpness_factor)
                self.item = self.enhance_contrast(self.item, self.contrast_factor)

                format = str(i) + ".png"
                savepath = os.path.join(self.outfilepath, format) 
                self.item.save(savepath)
                print("Consumer enhanced an image!")
    
    def enhance_brightness(self, image, factor):
        return ImageEnhance.Brightness(image).enhance(factor)

    def enhance_contrast(self, image, factor):
        return ImageEnhance.Contrast(image).enhance(factor)

    def enhance_sharpness(self, image, factor):
        return ImageEnhance.Sharpness(image).enhance(factor)


if __name__ == "__main__":

    # Multiprocessing initialisation
    manager = multiprocessing.Manager()
    shared_resource_buffer = manager.list()
    semaphore = multiprocessing.Semaphore(0)

    # Input taking
    filepath = input("File directory for input images: ")
    outfilepath = input("File directory for output images: ")
    brightness_enhancement_factor = input("Brightness Enhancement Factor: ")
    sharpness_enhancement_factor = input("Sharpness Enhancement Factor: ")
    contrast_enhancement_factor = input("Contrast Enhancement Factor: ")
    number_files = len(os.listdir(filepath))

    # Running multiprocessing
    start_time = time.time()
    t1 = Consumer(number_files, outfilepath, semaphore, shared_resource_buffer, brightness_enhancement_factor, sharpness_enhancement_factor, contrast_enhancement_factor)
    t2 = Producer(filepath, semaphore, shared_resource_buffer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("--- Time elapsed: %s seconds ---" % (time.time() - start_time))
