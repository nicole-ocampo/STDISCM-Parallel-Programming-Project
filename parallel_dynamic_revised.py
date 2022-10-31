# Libraries for parallelism and concurrency
from concurrent.futures import thread
import multiprocessing
import time
import threading

# Libraries for tasks
import os
import psutil
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
    def __init__(self, id, number_files, num_workers, outfilepath, semaphore, buffer, brightness_factor, sharpness_factor, contrast_factor, text_file_cont):
        multiprocessing.Process.__init__(self)
        self.id = id
        self.number_files = int(number_files/num_workers)
        self.outfilepath = outfilepath
        self.semaphore = semaphore
        self.buffer = buffer
        self.brightness_factor = float(brightness_factor)
        self.sharpness_factor = float(sharpness_factor)
        self.contrast_factor = float(contrast_factor)
        self.text_file_cont = text_file_cont

        self.item = Image.new(mode="RGB", size=(200, 200))


    def run(self):
        print("Consumer is waking up...")
        for i in range(self.number_files):
            self.semaphore.acquire()
            if self.buffer:
                self.item = self.buffer.pop()
                start_time = time.time()

                self.enhance_brightness()
                self.enhance_sharpness()
                self.enhance_contrast()


                end_time = time.time()
                elapsed_time = end_time - start_time

                format = str(i) + ".png"
                savepath = os.path.join(self.outfilepath, format) 

                self.text_file_cont.append("Image: " + str(self.item))
                self.text_file_cont.append("Output filename: " + str(savepath))
                self.text_file_cont.append("Start time: " + str(start_time) + " seconds")
                self.text_file_cont.append("End time: " + str(end_time) + " seconds")
                self.text_file_cont.append("Time elapsed: " + str(elapsed_time) + " seconds")
                self.text_file_cont.append("CPU Usage: " + str(psutil.cpu_percent()))
                self.text_file_cont.append("------------------")

                self.item.save(savepath)
                print("Consumer enhanced an image!")
    
    def enhance_brightness(self):
        self.item = ImageEnhance.Brightness(self.item).enhance(self.brightness_factor)

    def enhance_contrast(self):
        self.item = ImageEnhance.Contrast(self.item).enhance(self.contrast_factor)

    def enhance_sharpness(self):
        self.item = ImageEnhance.Sharpness(self.item).enhance(self.sharpness_factor)


if __name__ == "__main__":

    # Multiprocessing initialisation
    manager = multiprocessing.Manager()
    shared_resource_buffer = manager.list()
    text_file_cont = manager.list()
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
    num_workers = psutil.cpu_count(logical = False) - 1 # 1 for producer
    t1 = Producer(filepath, semaphore, shared_resource_buffer)
    consumers = []

    # Output text file
    text_file_cont.append("Number of files enhanced: " + str(number_files))
    text_file_cont.append("Output directory: " + str(outfilepath))
    text_file_cont.append("Number of Processes to spawn: " + str(num_workers+1))
    text_file_cont.append("------------------")

    for i in range(num_workers):
        worker = Consumer(i,number_files, num_workers, outfilepath, semaphore, shared_resource_buffer, 
                    brightness_enhancement_factor, sharpness_enhancement_factor, 
                    contrast_enhancement_factor, text_file_cont)
        consumers.append(worker)
    
    t1.start()
    for consumer in consumers:
        consumer.start()

    t1.join()
    for consumer in consumers:
        consumer.join()


    # Finalization
    elapsed = time.time() - start_time
    print("--- Time elapsed: %s seconds ---" % (elapsed))
    with open('Statistics.txt', 'w') as f:
        for line in text_file_cont:
            f.write(line)
            f.write('\n')
        
        f.write("Total time elapsed: " + str(elapsed) + " seconds")

