# Libraries for parallelism and concurrency
from concurrent.futures import thread
import multiprocessing
import time
import threading

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
    def __init__(self, id, number_files, outfilepath, semaphore, buffer, brightness_factor, sharpness_factor, contrast_factor, text_file_cont):
        multiprocessing.Process.__init__(self)
        self.id = id
        self.number_files = int(number_files/3)
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

                global s
                s = threading.Semaphore()

                t1 = threading.Thread(target=self.enhance_brightness)
                t2 = threading.Thread(target=self.enhance_sharpness)
                t3 = threading.Thread(target=self.enhance_contrast)

                t1.start()
                t2.start()
                t3.start()

                t1.join()
                t2.join()
                t3.join()

                end_time = time.time()
                elapsed_time = end_time - start_time

                format = str(i) + ".png"
                savepath = os.path.join(self.outfilepath, format) 

                self.text_file_cont.append("Image: " + str(self.item))
                self.text_file_cont.append("Output filename: " + str(savepath))
                self.text_file_cont.append("Start time: " + str(start_time) + " seconds")
                self.text_file_cont.append("End time: " + str(end_time) + " seconds")
                self.text_file_cont.append("Time elapsed: " + str(elapsed_time) + " seconds")
                self.text_file_cont.append("------------------")

                self.item.save(savepath)
                print("Consumer enhanced an image!")
    
    def enhance_brightness(self):
        global s
        s.acquire()
        self.item = ImageEnhance.Brightness(self.item).enhance(self.brightness_factor)
        s.release()

    def enhance_contrast(self):
        global s
        s.acquire()
        self.item = ImageEnhance.Contrast(self.item).enhance(self.contrast_factor)
        s.release()

    def enhance_sharpness(self):
        global s
        s.acquire()
        self.item = ImageEnhance.Sharpness(self.item).enhance(self.sharpness_factor)
        s.release()


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

    # Output text file
    text_file_cont.append("Number of files enhanced: " + str(number_files))
    text_file_cont.append("Output directory: " + str(outfilepath))
    text_file_cont.append("------------------")

    # Running multiprocessing
    start_time = time.time()
    t1 = Producer(filepath, semaphore, shared_resource_buffer)
    t2 = Consumer(1,number_files, outfilepath, semaphore, shared_resource_buffer, 
                  brightness_enhancement_factor, sharpness_enhancement_factor, 
                  contrast_enhancement_factor, text_file_cont)
    t3 = Consumer(2,number_files, outfilepath, semaphore, shared_resource_buffer, 
                  brightness_enhancement_factor, sharpness_enhancement_factor, 
                  contrast_enhancement_factor, text_file_cont)
    t4 = Consumer(3,number_files, outfilepath, semaphore, shared_resource_buffer, 
                  brightness_enhancement_factor, sharpness_enhancement_factor, 
                  contrast_enhancement_factor, text_file_cont)            
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    # Finalization
    elapsed = time.time() - start_time
    print("--- Time elapsed: %s seconds ---" % (elapsed))
    with open('Statistics.txt', 'w') as f:
        for line in text_file_cont:
            f.write(line)
            f.write('\n')
        
        f.write("Total time elapsed: " + str(elapsed) + " seconds")

