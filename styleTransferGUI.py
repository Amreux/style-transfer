import customtkinter
from os import access,R_OK
from PIL import Image,ImageTk
from tkinter import Label,messagebox
import Optimization_Functions.segmentation as seg
import style_transfer as st
import skimage.io as io
import cv2
import numpy as np
import imageio.v3 as iio


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

root_window=customtkinter.CTk()
root_window.geometry("1350x490")
root_window.title("Style Transfer")
root_window.resizable(width=False,height=False)

root_window.grid_rowconfigure(list(range(0,11)),weight=1)
root_window.grid_columnconfigure(list(range(0,10)),weight=1)
####################################################################################
def is_image_file(filename):
    try:
        with Image.open(filename) as img:
            img.verify()  # Verify that it is, in fact, an image
        return True
    except (IOError, SyntaxError) as e:
        print(f"Error: {e}")
        return False

def open_original_image(frame):
    path=customtkinter.filedialog.askopenfilename()
    if(access(path,R_OK)==False):
        messagebox.showerror(title="Error",message="this image is unreadable")
        return
    if(is_image_file(path)==False):
        messagebox.showerror(title="Error",message="this file is not an image")
        return
    photo=ImageTk.PhotoImage(Image.open(path).resize((350,350)))
    l1=Label(frame,image=photo)
    l1.image=photo
    l1.grid(row=1,column=0,rowspan=10,columnspan=3,padx=(30,20),pady=30)
    original_image_path.set(path)

    return
def open_style_image(frame):
    path=customtkinter.filedialog.askopenfilename()
    if(access(path,R_OK)==False):
        messagebox.showerror(title="Error",message="this image is unreadable")
        return
    if(is_image_file(path)==False):
        messagebox.showerror(title="Error",message="this image is not an image")
        return
    photo=ImageTk.PhotoImage(Image.open(path).resize((350,350)))
    l2=Label(frame,image=photo)
    l2.image=photo
    l2.grid(row=1,column=5,rowspan=10,columnspan=3,padx=(20,20),pady=30)
    style_image_path.set(path)

    return

def enable_advanced_options():
    if(advanced_options_switch_value.get()==True):
        color_transfer_type_label.configure(state="normal")
        color_transfer_type_combo.configure(state="readonly")
        patch_sizes_combo.configure(state="readonly")
        segmentation_type_combo.configure(state="readonly")
        guassian_layers_entry.configure(state="normal")
        regularization_entry.configure(state="normal")
        sampling_gaps_entry.configure(state="readonly")
        mask_weight_entry.configure(state="readonly")
    else:
        color_transfer_type_label.configure(state="disabled")
        color_transfer_type_combo.configure(state="disabled")
        patch_sizes_combo.configure(state="disabled")   
        segmentation_type_combo.configure(state="disabled")
        guassian_layers_entry.configure(state="disabled")
        regularization_entry.configure(state="disabled")
        sampling_gaps_entry.configure(state="disabled")
        mask_weight_entry.configure(state="disabled")
    return

def start():
    if(original_image_path.get()==""):
        messagebox.showerror(title="Error",message="please select an original image")
        return
    if(style_image_path.get()==""):
        messagebox.showerror(title="Error",message="please select a style image")
        return
    X=io.imread(original_image_path.get(),).astype(np.float32)/255
    
    X=cv2.resize(X, (400,400))
    style=io.imread(style_image_path.get()).astype(np.float32)/255

    style = cv2.resize(style, (np.shape(X)[0], np.shape(X)[1]))
    
    patches_sizes = list(map(int,patch_sizes_value.get().split(",")))
    sampling_gaps = list(map(int,sampling_gaps_value.get().split(",")))

    I_irls = 5
    I_alg = 3
    out = st.style_transfer(X,style,float(regularization_value.get()),int(guassian_layers_value.get()),I_irls,patches_sizes,sampling_gaps,I_alg ,color_transfer_type_value.get(),segmentation_type_value.get(),float(mask_weight_value.get()))
    iio.imwrite(uri="imgs\output\content_styl50.jpg", image=(out[:-patches_sizes[0],:-patches_sizes[0],:]*255).astype(np.uint8))
    photo=ImageTk.PhotoImage(Image.open("imgs\output\content_styl50.jpg").resize((350,350)))
    l3=Label(images_frame,image=photo)
    l3.image=photo
    l3.grid(row=1,column=8,rowspan=10,columnspan=3,padx=10,pady=30)
    return

############################################################################################
original_image_path=customtkinter.Variable()
style_image_path=customtkinter.Variable()
color_transfer_type_value=customtkinter.Variable(value="histogram")
advanced_options_switch_value=customtkinter.Variable(value=False)
patch_sizes_value=customtkinter.Variable(value="40,30")
segmentation_type_value=customtkinter.Variable(value="edge")
guassian_layers_value=customtkinter.Variable(value=3);
regularization_value=customtkinter.Variable(value=0.8);
sampling_gaps_value=customtkinter.Variable(value="30,20")
mask_weight_value=customtkinter.Variable(value=0.8);

############################################################################################
main_frame=customtkinter.CTkFrame(root_window)
main_frame.grid(row=0,column=0,rowspan=1,columnspan=10,padx=20,pady=20,sticky="nsew")

original_image_label=customtkinter.CTkLabel(main_frame,text="Content Image")
original_image_label.grid(row=0,column=0,pady=(20,20),padx=(20,0))

original_image_path_entry=customtkinter.CTkEntry(main_frame,width=300,textvariable=original_image_path)
original_image_path_entry.grid(row=0,column=1,columnspan=3,padx=(10,0),pady=(20,20))

original_image_path_button=customtkinter.CTkButton(main_frame,text="Browse",width=70,command=lambda:open_original_image(images_frame))
original_image_path_button.grid(row=0,column=4,padx=(10,0),pady=(20,20))

style_image_label=customtkinter.CTkLabel(main_frame,text="Style Image")
style_image_label.grid(row=0,column=5,pady=(20,20),padx=(30,0))

style_image_path_entry=customtkinter.CTkEntry(main_frame,width=300,textvariable=style_image_path)
style_image_path_entry.grid(row=0,column=6,columnspan=3,padx=(10,0),pady=(20,20))

style_image_path_button=customtkinter.CTkButton(main_frame,text="Browse",width=70,command=lambda:open_style_image(images_frame))
style_image_path_button.grid(row=0,column=9,padx=(10,20),pady=(20,20))

start_button=customtkinter.CTkButton(main_frame,text="Start",width=100,command=lambda:start())
start_button.grid(row=0,column=10,padx=(60,0),pady=(20,20))

############################################################################################

images_frame=customtkinter.CTkFrame(root_window)
images_frame.grid(row=1,column=0,rowspan=10,columnspan=7,padx=(20,10),pady=(0,20),sticky="nsew")

# photo=ImageTk.PhotoImage(Image.open("vat.jpg").resize((300,300)))
# l1=Label(images_frame,image=photo)
# l1.grid(row=1,column=0,rowspan=10,columnspan=3,padx=20,pady=20)

############################################################################################
# 
options_frame=customtkinter.CTkFrame(root_window)
options_frame.grid(row=1,column=7,rowspan=10,columnspan=3,padx=(10,20),pady=(0,20),sticky="nsew")



options_switch=customtkinter.CTkSwitch(options_frame,text="Advanced Options",width=20,onvalue=True,offvalue=False,command=lambda:enable_advanced_options(),variable=advanced_options_switch_value)
options_switch.grid(row=0,column=0,columnspan=4,padx=20,pady=20)


color_transfer_type_label=customtkinter.CTkLabel(options_frame,text="Color Transfer Type")
color_transfer_type_label.grid(row=1,column=0,columnspan=2,padx=20,pady=5)

color_transfer_type_combo=customtkinter.CTkComboBox(options_frame,values=["histogram","lab"],variable=color_transfer_type_value,state="disabled")
color_transfer_type_combo.grid(row=1,column=2,columnspan=2,padx=20,pady=5)


patch_sizes_label=customtkinter.CTkLabel(options_frame,text="Patch Sizes")
patch_sizes_label.grid(row=2,column=0,columnspan=2,padx=20,pady=5)

patch_sizes_combo=customtkinter.CTkComboBox(options_frame,values=["50,40","40,30","30,20","20,10"],state="disabled",variable=patch_sizes_value)
patch_sizes_combo.grid(row=2,column=2,columnspan=2,padx=20,pady=5)


sampling_gaps_label=customtkinter.CTkLabel(options_frame,text="Sampling Gaps")
sampling_gaps_label.grid(row=3,column=0,columnspan=2,padx=20,pady=5)

sampling_gaps_entry=customtkinter.CTkComboBox(options_frame,values=["40,30","30,20","20,10","10,5"],state="disabled",variable=sampling_gaps_value)
sampling_gaps_entry.grid(row=3,column=2,columnspan=2,padx=20,pady=5)


segmentation_type_label=customtkinter.CTkLabel(options_frame,text="Segmentation type")
segmentation_type_label.grid(row=4,column=0,columnspan=2,padx=20,pady=5)


segmentation_type_combo=customtkinter.CTkComboBox(options_frame,values=["grabcut","watershed","edge"],state="disabled",variable=segmentation_type_value)
segmentation_type_combo.grid(row=4,column=2,columnspan=2,padx=20,pady=5)




guassian_label=customtkinter.CTkLabel(options_frame,text="Guassian layers")
guassian_label.grid(row=5,column=0,columnspan=2,padx=20,pady=5)

guassian_layers_entry=customtkinter.CTkEntry(options_frame,state="disabled",textvariable=guassian_layers_value)
guassian_layers_entry.grid(row=5,column=2,columnspan=2,padx=20,pady=5)


regularization_label=customtkinter.CTkLabel(options_frame,text="Regularization (r)")
regularization_label.grid(row=6,column=0,columnspan=2,padx=20,pady=5)


regularization_entry=customtkinter.CTkEntry(options_frame,state="disabled",textvariable=regularization_value)
regularization_entry.grid(row=6,column=2,columnspan=2,padx=20,pady=5)


mask_weight_label=customtkinter.CTkLabel(options_frame,text="Mask Weight")
mask_weight_label.grid(row=7,column=0,columnspan=2,padx=20,pady=5)

mask_weight_entry=customtkinter.CTkComboBox(options_frame,values=["0.5","0.6","0.7","0.8","0.9"],state="disabled",variable=mask_weight_value)
mask_weight_entry.grid(row=7,column=2,columnspan=2,padx=20,pady=5)  




############################################################################################
root_window.mainloop()
