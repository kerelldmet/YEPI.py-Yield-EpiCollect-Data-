#yield epiCollect -> yepi
import json
import re
import os
import sys

import urllib.request
from PIL import Image
import albumentations as A
import numpy as np
from pyfiglet import Figlet

figlet = Figlet()
fonts_list = figlet.getFonts()



def main():

    #to be provided by user
    my_folder = "D:\\DESKTOP D\\PythonTutorials\\project\\ML_Database"
    my_json_file = "form-1__form-01.json"
    image_output_size = "500x500" #square only(!)

    #to be proccessed by the script
    dataset_manipulation_interface(my_folder, my_json_file, image_output_size)


def get_json_url(json_file):
    try:
        if ".json" not in str(json_file): raise TypeError

        with open(json_file, "r") as json_file:
            json_object = json.load(json_file)

    except FileNotFoundError:
        sys.exit("File not found...👀 Please check file spelling and/or path")
    except TypeError:
        sys.exit("Not a .JSON file...👀")

    #json_pretty = json.dumps(json_object, indent=2)

    url_list = []
    for j in json_object["data"]:
        
        link_pattern = r"^(\bhttps\b\:.*\.jpg)$" 
        dict_values = j.values()

        for value in dict_values:
            try:
                matches = re.search(link_pattern, value)
            except TypeError:
                pass
            else:
                if matches: url_list.append(matches.group())
    
    print("Step_1: Successfully completed:", len(url_list), "links found 😍")
    return url_list 

def save_url_to(dir, u_list):

    for n,url in enumerate(u_list):
        save_as = dir + "\\" + str(n) + ".jpg"

        try:
            urllib.request.urlretrieve(url, save_as)
        except FileNotFoundError:
            sys.exit("Please, create the folder first, or check the path")
        except EOFError:
            print("Process is aborted")
        else:
            print(f"Downloaded {n+1}/{len(u_list)}...")

    print("STEP_2: Successfully saved", len(os.listdir(dir)), "files from", len(u_list), "links 😍")
    
def delete_by_size(dir):
    
    folder_list = os.listdir(dir)
    img_removed = 0
    
    for f in folder_list:
        
        with Image.open(f"{dir}\\{f}", "r") as im :
            
            if im.size == (256, 256):  
                im.close()
                os.remove(f"{dir}\\{f}")
                img_removed += 1
    
    print(f"STEP_3: Successfully removed {img_removed} invalid images 😍, {len(os.listdir(dir))} left 🤗")

def crop_and_resize_images(dir, my_size):
   folder_list = os.listdir(dir)
   my_size = int(my_size.split("x")[0])

   for i,f in enumerate(folder_list):

        with Image.open(dir + "\\" + str(f)) as im:

            rotated = im 
            if im.width > im.height: #if image is in landscape mode
                rotated = im.transpose(Image.Transpose.ROTATE_90)

             # w * he
            original_ratio = rotated.height / rotated.width
            #print("original:", rotated.size) 

            resized = rotated.resize((my_size, int(my_size*original_ratio) + 1 ), resample=Image.Resampling.LANCZOS )
            #print("resized:", resized.size)

            #(left, upper, right, lower), with (0, 0) in the upper left corner
            box_y = int((resized.height - resized.width) /2)
            box = (0, box_y , my_size, box_y + my_size )
            cropped = resized.crop(box)
            #print("cropped", cropped.size)
            
            if im.width > im.height: #come back to landscape
                cropped = cropped.transpose(Image.Transpose.ROTATE_270)
            
            #im.close()
            
            #save_as = dir + "\\" + "Cropped" + "\\" + str(f).replace(".jpg", "") + "_500x500_" + ".jpg"
            save_as = f"{dir}\\Dataset_{i:04}_500x500_ReCr.jpg"
            
            os.remove(dir + "\\" + f) #delete originals
            cropped.save(save_as)
            print(f"Resizing and cropping {i}/{len(folder_list)} file")

   
   print(f"STEP_4: Successfully resized and cropped {len(os.listdir(dir))} files")

def dataset_manipulation_interface(dir, json_file, user_size): #combinatory function to controll dataset modifications and react to users' response
    answer = ""
    no = "Only 'yes' or 'no' answers are allowed. "
    #1---------------------------------------------------------------------
    print(f"{'STEP_1:Get URLS':.^100}")
    url_list = get_json_url(json_file)
    #2---------------------------------------------------------------------
    print(f"{'STEP_2: Downloading URLS':.^100}")
    if len(os.listdir(dir)) == 0: answer = input("Files are ready to be downloaded, start (yes/no)? ").strip().lower()
    elif len(os.listdir(dir)) > 0: answer = input("Files are already downloaded, (resave/skip)? ").strip().lower()
    
    if answer == "yes": save_url_to(dir, url_list)
    elif answer == "resave": 
        clean_folder(dir) 
        save_url_to(dir, url_list)
    elif answer == "skip": print("'STEP_2: Downloading URLS' Skipped")
    else: print(no)
    
    #3---------------------------------------------------------------------
    print(f"{'STEP_3: Validating Images (simple)':.^100}")
    delete_by_size(dir)
    #4---------------------------------------------------------------------
    print(f"{'STEP_4: Crop & Resize':.^100}")
    if len(os.listdir(dir)) == 0: answer = input("Files are ready to perform 'Crop & Resize', proceed? (yes, no) ").strip().lower()
    if len(os.listdir(dir)) > 0: answer = input("Folder is already full, redo 'Crop & Resize'? (yes, no) ").strip().lower()

    if answer == "yes": crop_and_resize_images(dir, user_size)
    elif answer == "no": print("STEP_4: 'Crop & Resize' Skipped")
    else: print(no)

    #5---------------------------------------------------------------------
    print(f"{'STEP_5: Augmentation':.^100}")
    answer = input("Dataset is ready to be augmented. Would you like to proceed? (yes/no) ").strip().lower()
    if answer == "yes": augment_images(dir)
    elif answer == "no": print("STEP_5: 'Downloading URLS': Skipped")
    else: print(no)
    
    
    #final report
    print("Total dataset capacity: ", len(os.listdir(dir)))
    print(figlet.renderText("Your Dataset is ready!"))
    
def augment_images(dir):
    images_list = os.listdir(dir)
    
    transform = A.Compose([
        A.HorizontalFlip(p=0.8),
        A.RandomBrightnessContrast(p=0.5),
        A.Equalize(p=0.5)
    ])
    
    agm_images = []
    for n, image in enumerate(images_list):
        pillow_image = Image.open(dir + "\\" + image)
        image_array = np.array(pillow_image)

        transformed = transform(image=image_array)
        transformed_image = transformed["image"]
        agm_images.append(transformed_image)

        im = Image.fromarray(transformed_image)
        im.save(dir + "\\" + f"{image}_Augmented{n:03}.png") 
        
        print(f"Augmented {n+1}/{len(images_list)}...")
    
    print("STEP_5: Successfully augmented", len(images_list), "files 😍")

def clean_folder(dir):
    
    for item in os.listdir(dir): 
        os.remove(dir + "\\" + item)
        
    print("Folder is cleaned")

if __name__=="__main__":
    main()