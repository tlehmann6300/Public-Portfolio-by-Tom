"""
This Python code implements a graphical user interface (GUI) for a QR code generator. 
The user can enter URLs in an input field, select the size and file format of the QR code 
and save the QR code to any location. The main features are:

1.URL entry and validation: The user enters a URL, which is validated and, if necessary, automatically 
   with “http://” if it looks like an IP address.
2.Dynamic history function: The most recently generated URLs are saved and can be selected from a drop-down menu.
3.Customizable options: The user can choose between different sizes (Small, Medium, Large) and file formats (PNG, JPEG, WEBP).
4.Saving options: The generated QR code can be saved to any location.
5.Error handling: It is ensured that invalid inputs or actions result in clear error messages.

The user interface is created with `tkinter` and the QR code generation is done using the `qrcode` module. 
The 'Pillow' library is used to display the QR code. The code provides a user-friendly and modern 
and modern design with a clearly structured GUI.
"""



import qrcode
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image

url_history = []

def generate_qr_code():
    global url_history
    url = url_entry.get()
    size = size_var.get()

    if size == "Small":
        box_size = 5
    elif size == "Medium":
        box_size = 10
    elif size == "Large":
        box_size = 20
    else:
        messagebox.showerror("Error", "Please select a valid size.")
        return

    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    
    if url.replace(".", "").isdigit():
        url = f"http://{url}"
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)


    if url not in url_history:
        url_history.insert(0, url)
        if len(url_history) > 5:
            url_history.pop()
        history_menu.menu.delete(0, "end")
        for item in url_history:
            history_menu.menu.add_command(label=item, command=lambda value=item: url_entry.delete(0, tk.END) or url_entry.insert(0, value))

    
    file_format = format_var.get()
    if file_format == "PNG":
        ext = "png"
    elif file_format == "JPEG":
        ext = "jpg"
    elif file_format == "WEBP":
        ext = "webp"
    else:
        messagebox.showerror("Error", "Please select a valid file format.")
        return

    
    file_path = filedialog.asksaveasfilename(
        defaultextension=f".{ext}",
        filetypes=[(f"{file_format} Files", f"*.{ext}")],
        initialfile=f"generated_qrcode.{ext}",
        title="Select location to save the QR code"
    )

    if not file_path:
        messagebox.showinfo("Cancelled", "Save operation was cancelled.")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    try:
        img.save(file_path)

       
        url_entry.delete(0, tk.END)
        size_var.set("Medium")
        format_var.set("PNG")

        messagebox.showinfo("Success", f"QR code was successfully saved to: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving the QR code: {e}")

root = tk.Tk()
root.title("QR Code Generator")
root.geometry("450x500")
root.configure(bg="#1e1e2f")

header_label = tk.Label(root, text="QR Code Generator", font=("Helvetica", 20, "bold"), bg="#34ebeb", fg="white", pady=15, relief=tk.RIDGE, bd=2)
header_label.pack(fill=tk.X)

url_frame = tk.Frame(root, bg="#1e1e2f")
url_frame.pack(pady=20)
url_label = tk.Label(url_frame, text="URL:", font=("Helvetica", 14), bg="#1e1e2f", fg="white")
url_label.pack(side=tk.LEFT, padx=10)
url_entry = tk.Entry(url_frame, width=35, font=("Helvetica", 14), relief=tk.SUNKEN, bd=2)
url_entry.pack(side=tk.LEFT, padx=10)


size_frame = tk.Frame(root, bg="#1e1e2f")
size_frame.pack(pady=20)
size_label = tk.Label(size_frame, text="Size:", font=("Helvetica", 14), bg="#1e1e2f", fg="white")
size_label.pack(side=tk.LEFT, padx=10)

size_var = tk.StringVar(value="Medium")
size_options = ["Small", "Medium", "Large"]
size_menu = ttk.Combobox(size_frame, textvariable=size_var, values=size_options, state="readonly", width=12, font=("Helvetica", 14))
size_menu.pack(side=tk.LEFT, padx=10)


format_frame = tk.Frame(root, bg="#1e1e2f")
format_frame.pack(pady=20)
format_label = tk.Label(format_frame, text="Format:", font=("Helvetica", 14), bg="#1e1e2f", fg="white")
format_label.pack(side=tk.LEFT, padx=10)

format_var = tk.StringVar(value="PNG")
format_options = ["PNG", "JPEG", "WEBP"]
format_menu = ttk.Combobox(format_frame, textvariable=format_var, values=format_options, state="readonly", width=12, font=("Helvetica", 14))
format_menu.pack(side=tk.LEFT, padx=10)


generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr_code, bg="#34ebeb", fg="white", font=("Helvetica", 14, "bold"), relief=tk.RAISED, bd=3)
generate_button.pack(pady=25)

history_menu = tk.Menubutton(root, text="History", relief=tk.RAISED, bg="#34ebeb", fg="white", font=("Helvetica", 12))
history_menu.menu = tk.Menu(history_menu, tearoff=0)
history_menu["menu"] = history_menu.menu
history_menu.pack(pady=10)


footer_label = tk.Label(root, text="Copyright © Tom Lehmann", font=("Helvetica", 12), bg="#1e1e2f", fg="white")
footer_label.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
