from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from PIL import Image, ImageTk

root = Tk()

style = Style()

root.title("Watermarker")
root.geometry("600x600")
root.configure(background='white')

pil_logo = Image.open("watermarker.png")
pil_logo.thumbnail((400, 400))

tk_logo = ImageTk.PhotoImage(pil_logo)
logo_label = Label(root, image=tk_logo, background='white')
logo_label.image = tk_logo
logo_label.grid(row=0, column=0, pady=(40, 20), padx=100)

style.configure('TButton', font=('calibri', 15, 'bold'), borderwidth='4')

style.map('TButton', foreground=[('active', '!disabled', 'grey')],
                     background=[('active', 'black')])

selected_image_path = None
selected_watermark_path = None

def load_image():
    global selected_image_path
    loaded_image = filedialog.askopenfilename(
        title="Open Image File",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")]
    )
    if loaded_image:
        selected_image_path = loaded_image
        display_loaded_image(loaded_image)
        apply_watermark()

def display_loaded_image(loaded_image):
    image = Image.open(loaded_image)
    image.thumbnail((150, 150))
    loaded_image_photo = ImageTk.PhotoImage(image)
    image_label.config(image=loaded_image_photo)
    image_label.photo = loaded_image_photo

def load_watermark():
    global selected_watermark_path
    loaded_wm = filedialog.askopenfilename(
        title="Open Watermark File",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")]
    )
    if loaded_wm:
        selected_watermark_path = loaded_wm
        display_watermark(loaded_wm)
        apply_watermark()

def display_watermark(loaded_wm):
    wm = Image.open(loaded_wm)
    wm.thumbnail((150, 150))
    wm_photo = ImageTk.PhotoImage(wm)
    watermark_label.config(image=wm_photo)
    watermark_label.photo = wm_photo

def apply_watermark():
    if not selected_image_path or not selected_watermark_path:
        return

    base_img = Image.open(selected_image_path).convert("RGBA")
    watermark = Image.open(selected_watermark_path).convert("RGBA")

    wm_width = int(base_img.width * 0.25)
    wm_ratio = wm_width / watermark.width
    wm_height = int(watermark.height * wm_ratio)
    watermark = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)

    opacity = 0.5
    alpha = watermark.getchannel("A")
    alpha = alpha.point(lambda p: int(p * opacity))
    watermark.putalpha(alpha)

    x = base_img.width - watermark.width - 20
    y = base_img.height - watermark.height - 20

    transparent_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    transparent_layer.paste(watermark, (x, y))
    watermarked = Image.alpha_composite(base_img, transparent_layer)

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg")]
    )
    if save_path:
        if save_path.lower().endswith((".jpg", ".jpeg")):
            watermarked = watermarked.convert("RGB")
        watermarked.save(save_path)

root.grid_rowconfigure(1, minsize=180)

image_label = Label(root, background='white')
image_label.grid(row=1, column=0, sticky='w', padx=80)

watermark_label = Label(root, background='white')
watermark_label.grid(row=1, column=0, sticky='e', padx=95)

load_btn = Button(root, text='Load Image', command=load_image)
load_btn.grid(row=2, column=0, sticky="w", padx=95, pady=(10, 0))

water_btn = Button(root, text='Load Watermark', command=load_watermark)
water_btn.grid(row=2, column=0, sticky="e", padx=95, pady=(10, 0))

root.mainloop()
