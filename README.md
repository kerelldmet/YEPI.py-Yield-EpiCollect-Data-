# "YEPI" - Yield data from EpiCollect #
    #### Video Demo:  <URL HERE>
    #### The Python script that helps to extract and downaload the links from your EpiCollect project:   
    TODO

**WORKFLOW, general notes**:
General Workflow consists of the 5 STEPS for each dataset process.
All the most time-consuming functions (such as: downloading URLS, Crop&Resize, Augmentation etc) prompt user for "yes" or "no" in order to continue. If the user inputs "yes" -> the step is being excecuted. Otherwise, it is skipped and the next one is promted until the script runs out of functions.

This is done for a easier navigation and more "save" way of workflow. 
In case the script faces an error, some of the steps will be executed anyways. Moreover the error could be located much faster, hence - much effective.

The intention is to allow user to follow the process of data harvesing and processing,
not spending the time for the steps that have been executed wrongly.
In addition to it, if the User wants to repeat some of the steps (for example, resize images) he can skip all the steps and accept only the one (in this: "Step 4" Resize & Crop")

**WORKFLOW, step by step**
*Step1* 
- > using "json" library, the user's .json file is being process
- > going into the nested dictionaries, the regex expression looks though the values 
and extracts the "link-like" strings and stores them in a list
...extra: in order to view the structure of your Json file feel free to print "json_pretty" variable (currently commented out)
*Step2*
- > using "urllib.request" library the script access the list of urls collected in Step1 and retrieve them
- > images are therefore stored in local drive (dir should be specified)
*Step3*
- > cleans the list of downaloaded images from wrong, non-representing images (removing logo images of 256*256)
*Step4*
- > using PIL library the script accesses every image 
- > applies resize (scale image to the user specified desired image size) - in order to preserve as much pixels as possible. note: it aplplies for portrait- as well as landscale-oriented images, no need to worry about it:)
- > then images are being cropped in a square ratio
- > images are stored back to the folder
- > old (original) images are removed.
*Step5*
- > using "Albumentations" library scrip suggests to expand the data set using augmentation techniques.
- > currently in the script only 3 transformations are applied (Horizontal flip, RandomBrightnessContrast and Equalized(color effect)), 
...extra: The transformations can be added (60+ available in the library), however consider the accuracy of the ML process later. The link to play & test with transformations available in the library - https://demo.albumentations.ai/

*final*
- > process is finish by fancy-looking text made with "figlet" library.


                                                                                    Please Enjoy!

                                                                                    Made by Kyryll Dmytrenko, 
                                                                                    as a final project for CS50p course
                                                                                    27th of December, 2022


**Steps for later release**
- > would be much effective to compose most of the functions into the class, 
in order to provide much easier nabigation and usage outside of the main file. 

