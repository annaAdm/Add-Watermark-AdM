from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk, UnidentifiedImageError

window = Tk()
window.title('Add AdM watermark')
window.config(padx=20, pady=20)

canvas = Canvas(width=400, height=600)
background_img = PhotoImage(file="background.png")
canvas.create_image(200, 300, image=background_img)

# Create a global variable to store the PhotoImage object
photo_images = []


def remove_label(error_label, ok_btn):
    error_label.destroy()
    ok_btn.destroy()


def open_file():
    error_label = None
    ok_btn = None
    file_path = askopenfile(mode='rb', filetypes=[('Image Files', '*.jpeg;*.jpg;*.png')])
    if file_path is not None:
        try:
            image1 = Image.open(file_path)
            resized_image = image1.resize((150, 120))
            little_pic = ImageTk.PhotoImage(resized_image)
            chosen_img = ImageTk.PhotoImage(image1)

            label = Label(window, image=little_pic)
            label.grid(row=2, column=0, pady=10)

            # Store the reference to the image to prevent it from being garbage collected
            label.image = little_pic
            photo_images.append(chosen_img)
            Label(window, text='File Generated Successfully!', foreground='teal', ).grid(row=3, column=0, pady=10)

            return True, image1
        except UnidentifiedImageError:
            error_label = Label(window, text='The selected file is not a valid image.', foreground='teal')
            error_label.grid(row=2, columnspan=2, pady=10)

            ok_btn = Button(window, text='OK', command=lambda: remove_label(error_label, ok_btn))
            ok_btn.grid(row=2, column=3, pady=10)
            return False, None
    return False, None


def add_watermark(image1, image2_path):
    # get image1 with on_click()
    image2 = Image.open(image2_path)

    # image1 and image2 must have the same size
    image2 = image2.resize(image1.size)

    # Overlay the images
    result = Image.blend(image1, image2, alpha=0.2)  # Adjust opacity by changing the value of alpha

    # save the result
    wm_file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[('Image Files', "*.jpg"), ("All files", "*.*")])
    if wm_file_path:
        result.save(wm_file_path)
        print("Done")
        Label(window, text='File Saved Successfully!', foreground='teal', ).grid(row=6, column=0, pady=10)


def on_click():
    _, image1 = open_file()  # here i get image1
    image2_path = "AnnaAdM.jpg"
    add_watermark(image1, image2_path)


canvas.grid(columnspan=5, rowspan=8)


add_wm_text = canvas.create_text(180, 70, text="Add the AdM watermark to your file.", width=300,
                                font=("Arial", 15),
                                fill="white")

adm_img = PhotoImage(file="adm.png")
adm_button = Button(image=adm_img, command=on_click, width=90)
adm_button.grid(row=5, columnspan=5)


window.mainloop()
