# STDISCM Parallel-Programming-Project
 
Images have inherently become an essential part of one's social life. A majority of young adults and teens spend an abundant amount of time online, and this usually involves sharing images and the likes to show other individuals what they are up to. Almost all social media platforms provide its users with tools to upload photos and videos. Most platforms give users the ability to share their thoughts and experiences online using images, but social media platforms–like Instagram–who focus on photo and video sharing usually provide users with tools like filters that enhance images and videos to increase the overall viewing experience.

Since a majority of young adults use various social media platforms, it could be said that a huge portion of the population has used or at least heard of image enhancement in one way or another. Photos frequently turn out differently due to the camera, where there are various factors that may affect the brightness, contrast, among other factors. In order for the photo to accurately portray the visual presented in the real world, photographers either have to change the camera settings or use image enhancers. Image enhancers can help users adjust the image to accurately represent real world visuals, or perhaps match the idea the user has.

Although it may seem like adjusting images is as simple as adding numbers to current values of the image, a lot more is going on. Thousands of pixels are being manipulated, and each manipulation is not as simple as adding or subtracting values. This could take quite some time for the process to finish especially for huge images and multiple queries, which is where multiprocessing and threading comes into play. Usually machines read instructions sequentially but parallel programming techniques allow the machine to run multiple instructions at the same time leading to remarkable performance gains.

This project focuses on the design and implementation of an Image Enhancement program using parallel programming to improve performance and efficiency. The program takes the following input from the user:

1. Folder location of images 
2. Folder location of enhanced images 
3. Enhancing time in minutes 
4. Brightness enhancement factor 
5. Sharpness enhancement factor 
C6. ontrast enhancement factor 

Once the input has been parsed, the program will enhance the images according to the input enhancement factors, and will be outputted in the folder location for processed images. A text file containing summary statistics will also be generated for further analysis.
