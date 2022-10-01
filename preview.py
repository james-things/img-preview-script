# Render Preview GUI Script

# imports
import os
import tkinter as tk
from PIL import ImageTk, Image
from datetime import datetime

# get path to directory of script file
target_path = os.path.dirname(os.path.realpath(__file__)) + "\\"
display_image_path = ""

# convert a datetime to float
def datetime_to_float(d):
    epoch = datetime.utcfromtimestamp(0)
    total_seconds = (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds


# function to get most recent image in folder
def get_newest_img_filename():
    min_delta = 99999999999999.9
    now = datetime.now()
    filename_string = ""

    for filename in os.listdir(target_path):
        full_path = target_path + filename
        if not os.path.isdir(full_path):
            try:
                file_creation_time = os.path.getmtime(full_path)
                delta = datetime_to_float(now) - file_creation_time;
                if delta < min_delta:
                    potential_image_file = ImageTk.PhotoImage(Image.open(full_path)) # fail try if not image
                    filename_string = filename
            except IOError:
                print("skipping " + full_path)
    return filename_string


# initialize gui
root = tk.Tk()
root.title("Render Preview")
display_image_path = target_path + get_newest_img_filename()
display_image = ImageTk.PhotoImage(Image.open(display_image_path))
panel = tk.Label(root, image=display_image)
panel.pack(side="bottom", fill="both", expand=1)


# update cycle to update image on label
def update_clock():
    next_image_path = target_path + get_newest_img_filename()
    if not next_image_path == display_image_path:
        print("newer image found!")
        print("d: " + display_image_path + ", n: " + next_image_path)
        next_image = ImageTk.PhotoImage(Image.open(next_image_path))

        panel.configure(image=next_image)
        panel.image = next_image  # prevent gc
    root.after(5000, update_clock)


# main function
if __name__ == '__main__':
    update_clock()
    root.mainloop()
