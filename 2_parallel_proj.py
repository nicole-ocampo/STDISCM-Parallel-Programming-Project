# Libraries for parallelism and concurrency
from concurrent.futures import thread
import multiprocessing
import time
import threading

# Libraries for tasks
import os
from PIL import Image, ImageEnhance
import psutil

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
    def __init__(self, number_files, outfilepath, semaphore, buffer, 
                 brightness_factor, sharpness_factor, contrast_factor, 
                 text_file_cont, ave_cpu, total_enhanced_images, enhancement_time,
                 start_time):
        multiprocessing.Process.__init__(self)
        self.number_files = number_files
        self.outfilepath = outfilepath
        self.semaphore = semaphore
        self.buffer = buffer
        self.brightness_factor = float(brightness_factor)
        self.sharpness_factor = float(sharpness_factor)
        self.contrast_factor = float(contrast_factor)
        self.text_file_cont = text_file_cont
        self.ave_cpu = ave_cpu
        self.total_enhanced_images = total_enhanced_images
        self.enhancement_time = enhancement_time
        self.start_time = start_time

        self.item = Image.new(mode="RGB", size=(200, 200))


    def run(self):
        print("Consumer is waking up...")
        for i in range(self.number_files):
            self.semaphore.acquire()
            curr_time = time.time()
            if self.buffer:
                if (curr_time - self.start_time) < self.enhancement_time:
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
                    cpu_usage= psutil.cpu_percent()

                    elapsed_time = end_time - start_time
                    self.ave_cpu.append(cpu_usage)

                    format = str(i) + ".png"
                    savepath = os.path.join(self.outfilepath, format) 

                    self.text_file_cont.append("Image: " + str(self.item))
                    self.text_file_cont.append("Output filename: " + str(savepath))
                    self.text_file_cont.append("Start time: " + str(start_time) + " seconds")
                    self.text_file_cont.append("End time: " + str(end_time) + " seconds")
                    self.text_file_cont.append("Time elapsed: " + str(elapsed_time) + " seconds")
                    self.text_file_cont.append("CPU Usage: " + str(cpu_usage))
                    self.text_file_cont.append("------------------")

                    self.item.save(savepath)
                    print("Consumer enhanced an image!")

                    temp_val = self.total_enhanced_images.value
                    temp_val += 1
                    self.total_enhanced_images.value = temp_val
                else:
                    print("Enhancement time exceed. Terminating...")
                    break
    
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
    ave_cpu = manager.list()
    total_enhanced_images = manager.Value('i',0)
    semaphore = multiprocessing.Semaphore(0)

    # Input taking
    filepath = input("File directory for input images: ")
    outfilepath = input("File directory for output images: ")
    enhancement_time = input("Enhancement time (in minutes): ")
    brightness_enhancement_factor = input("Brightness Enhancement Factor: ")
    sharpness_enhancement_factor = input("Sharpness Enhancement Factor: ")
    contrast_enhancement_factor = input("Contrast Enhancement Factor: ")
    number_files = len(os.listdir(filepath))

    enhancement_time = float(enhancement_time) * 60

    # Output text file
    text_file_cont.append("Input number of files to be enhanced: " + str(number_files))
    text_file_cont.append("Output directory: " + str(outfilepath))
    text_file_cont.append("------------------")

    # Running multiprocessing
    start_time = time.time()
    t1 = Consumer(number_files, outfilepath, semaphore, shared_resource_buffer, 
                  brightness_enhancement_factor, sharpness_enhancement_factor, 
                  contrast_enhancement_factor, text_file_cont, ave_cpu, total_enhanced_images,
                  enhancement_time, start_time)
    t2 = Producer(filepath, semaphore, shared_resource_buffer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Finalization
    elapsed = time.time() - start_time
    ave_cpu_final = sum(ave_cpu) / len(ave_cpu)
    print("--- Time elapsed: %s seconds ---" % (elapsed))
    print("--- Average CPU Usage: %s ---" % (ave_cpu_final))
    print("--- Total Images Enhanced: %s  ---" % (total_enhanced_images.value))
    with open('Statistics.txt', 'w') as f:
        for line in text_file_cont:
            f.write(line)
            f.write('\n')
        
        f.write("Total time elapsed: " + str(elapsed) + " seconds\n")
        f.write("Average CPU Usage: " + str(ave_cpu_final) +  " \n")
        f.write("Total Images Enhanced: " + str(total_enhanced_images.value))