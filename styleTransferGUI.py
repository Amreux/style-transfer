import customtkinter
from os import access,R_OK
from PIL import Image,ImageTk
from tkinter import Label,messagebox


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

root_window=customtkinter.CTk()
root_window.geometry("1200x400")
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
        messagebox.showerror(title="Error",message="this image is not an image")
        return
    photo=ImageTk.PhotoImage(Image.open(path).resize((300,300)))
    l1=Label(frame,image=photo)
    l1.image=photo
    l1.grid(row=1,column=0,rowspan=10,columnspan=3,padx=20,pady=20)
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
    photo=ImageTk.PhotoImage(Image.open(path).resize((300,300)))
    l2=Label(frame,image=photo)
    l2.image=photo
    l2.grid(row=1,column=5,rowspan=10,columnspan=3,padx=20,pady=20)
    style_image_path.set(path)

    return
############################################################################################
original_image_path=customtkinter.Variable()
style_image_path=customtkinter.Variable()

############################################################################################
main_frame=customtkinter.CTkFrame(root_window)
main_frame.grid(row=0,column=0,rowspan=1,columnspan=10,padx=20,pady=20,sticky="nsew")

original_image_label=customtkinter.CTkLabel(main_frame,text="Original Image")
original_image_label.grid(row=0,column=0,pady=(20,20),padx=(20,0))

original_image_path_entry=customtkinter.CTkEntry(main_frame,width=300,textvariable=original_image_path)
original_image_path_entry.grid(row=0,column=1,columnspan=3,padx=(10,0),pady=(20,20))

original_image_path_button=customtkinter.CTkButton(main_frame,text="Browse",width=70,command=lambda:open_original_image(images_frame))
original_image_path_button.grid(row=0,column=4,padx=(10,0),pady=(20,20))

style_image_label=customtkinter.CTkLabel(main_frame,text="Style Image")
style_image_label.grid(row=0,column=5,pady=(20,20),padx=(50,0))

style_image_path_entry=customtkinter.CTkEntry(main_frame,width=300,textvariable=style_image_path)
style_image_path_entry.grid(row=0,column=6,columnspan=3,padx=(10,0),pady=(20,20))

style_image_path_button=customtkinter.CTkButton(main_frame,text="Browse",width=70,command=lambda:open_style_image(images_frame))
style_image_path_button.grid(row=0,column=9,padx=(10,0),pady=(20,20))

############################################################################################

images_frame=customtkinter.CTkFrame(root_window)
images_frame.grid(row=1,column=0,rowspan=10,columnspan=10,padx=20,pady=(0,20),sticky="nsew")

# photo=ImageTk.PhotoImage(Image.open("vat.jpg").resize((300,300)))
# l1=Label(images_frame,image=photo)
# l1.grid(row=1,column=0,rowspan=10,columnspan=3,padx=20,pady=20)



############################################################################################
root_window.mainloop()
