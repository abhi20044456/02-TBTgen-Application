import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
from tkinter.ttk import Progressbar, Style
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import threading
import time

class TBTGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TBT Gen")
        self.root.geometry("600x550")
        self.root.config(bg="#F0F0F0")

        # Apply style for a professional look
        self.style = Style()
        self.style.configure("TButton", font=("Arial", 10), padding=6, relief="flat")
        self.style.map("TButton",
                       foreground=[('active', 'white')],
                       background=[('active', '#3b5998')])

        # App Title
        title_label = tk.Label(root, text="TBT Gen", font=("Arial", 28, "bold"), fg="#3b5998", bg="#F0F0F0")
        title_label.pack(pady=10)

        # Team and Date Selection Row
        selection_frame = tk.Frame(root, bg="#F0F0F0")
        selection_frame.pack(pady=5)

        # Team Selection Dropdown
        tk.Label(selection_frame, text="Select Team:", font=("Arial", 12), bg="#F0F0F0").grid(row=0, column=0, padx=10)
        self.team_var = tk.StringVar()
        self.team_dropdown = tk.OptionMenu(selection_frame, self.team_var, "Team-1", "Team-2", "Team-3", "Team-4", "Team-5")
        self.team_var.set("Team-1")  # Default selection
        self.team_dropdown.grid(row=0, column=1, padx=10)
        self.team_dropdown.config(font=("Arial", 12), bg="white", fg="black", width=10)

        # Date Selection
        tk.Label(selection_frame, text="Select Date:", font=("Arial", 12), bg="#F0F0F0").grid(row=0, column=2, padx=10)
        self.date_entry = DateEntry(selection_frame, date_pattern='dd/mm/yyyy', font=("Arial", 12))
        self.date_entry.grid(row=0, column=3, padx=10)

        # Image Selection Buttons Row
        button_frame = tk.Frame(root, bg="#F0F0F0")
        button_frame.pack(pady=10)

        self.tbt_button = self.create_custom_button(button_frame, "Select TBT Images", self.select_tbt_images)
        self.tbt_button.grid(row=0, column=0, padx=10)

        self.team_button = self.create_custom_button(button_frame, "Select Team Images", self.select_other_images)
        self.team_button.grid(row=0, column=1, padx=10)

        # Progress Bar with Percentage
        self.progress_frame = tk.Frame(root, bg="#F0F0F0")
        self.progress_frame.pack(pady=10)

        self.progress_label = tk.Label(self.progress_frame, text="Progress: 0%", font=("Arial", 12), bg="#F0F0F0")
        self.progress_label.pack()

        self.progress = Progressbar(self.progress_frame, orient="horizontal", length=400, mode='determinate', style="TProgressbar")
        self.progress.pack(pady=10)

        # Set initial style
        self.style.configure("TProgressbar",
                            troughcolor='lightgrey',
                            background='yellow',
                            )

        # Generate TBT Button
        self.generate_button = tk.Button(root, text="Generate TBT", command=self.generate_tbt, state='disabled', bg="#3b5998", fg="white", font=("Arial", 12), relief="flat")
        self.generate_button.pack(pady=20)

        # WhatsApp Button
        self.whatsapp_button = tk.Button(root, text="Share on WhatsApp", command=self.open_whatsapp, state='disabled', bg="green", fg="white", font=("Arial", 12), relief="flat")
        self.whatsapp_button.pack(pady=5)

        # Developer Info and Social Links
        dev_info_frame = tk.Frame(root, bg="#F0F0F0")
        dev_info_frame.pack(pady=20)

        dev_info = tk.Label(dev_info_frame, text="All Right Reserved © 2024", font=("Arial", 8, "italic"), bg="#F0F0F0")
        dev_info.pack(pady=4)

        dev_info = tk.Label(dev_info_frame, text="Developed by Soumy(Abhi) Chauhan", font=("Arial", 10, "italic"), bg="#F0F0F0")
        dev_info.pack(pady=10)

        social_frame = tk.Frame(root, bg="#F0F0F0")
        social_frame.pack(pady=5)

        self.create_social_button("LinkedIn", "#0e76a8", self.open_linkedin, social_frame)
        self.create_social_button("Instagram", "#E4405F", self.open_instagram, social_frame)

        # Variables for selected images
        self.tbt_images = []
        self.other_images = []

    def create_custom_button(self, root, text, command):
        button = tk.Button(root, text=text, command=command, bg="#3b5998", fg="white", font=("Arial", 12), relief="flat", activebackground="#2d4373")
        return button

    def create_social_button(self, text, color, command, root):
        button = tk.Button(root, text=text, command=command, bg=color, fg="white", font=("Arial", 10), relief="flat")
        button.pack(side=tk.LEFT, padx=10)
        button.bind("<Enter>", lambda e: button.config(bg="gray"))
        button.bind("<Leave>", lambda e: button.config(bg=color))

    def select_tbt_images(self):
        self.tbt_images = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.tbt_images:
            self.update_progress(25)
            self.check_images_selected()

    def select_other_images(self):
        self.other_images = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.other_images:
            self.update_progress(50)
            self.check_images_selected()

    def update_progress(self, value):
        self.progress['value'] = value
        self.progress_label.config(text=f"Progress: {int(value)}%")
        if value == 100:
            self.progress.configure(style="TProgressbar")
            self.style.configure("TProgressbar",
                                troughcolor='lightgrey',
                                background='green')

    def check_images_selected(self):
        if self.tbt_images and self.other_images:
            self.generate_button.config(state='normal')

    def generate_tbt(self):
        if not self.tbt_images or not self.other_images:
            messagebox.showwarning("Error", "Please select both TBT and Team images.")
            return

        self.update_progress(50)
        self.generate_button.config(state='disabled')

        team = self.team_var.get()
        date = self.date_entry.get().replace("/", "-")
        filename = f"TBT_{team}_{date}.pdf"
        
        save_path = filedialog.askdirectory()
        if save_path:
            pdf_file = os.path.join(save_path, filename)

            # Start PDF generation in a separate thread
            threading.Thread(target=self.create_pdf, args=(pdf_file,)).start()

    def create_pdf(self, pdf_file):
        c = canvas.Canvas(pdf_file, pagesize=A4)
        width, height = A4

        left_margin = 50
        top_margin = 50
        right_margin = width - 50
        bottom_margin = height - 50

        # Add TBT images to the PDF, each on a new page
        for idx, img in enumerate(self.tbt_images):
            c.setFont("Helvetica-Bold", 24)
            header_text = f"TBT of {self.team_var.get()} _ {self.date_entry.get().replace('/', '-')}"
            text_width = c.stringWidth(header_text, "Helvetica-Bold", 24)
            header_x_position = (width - text_width) / 2

            c.drawString(header_x_position, height - top_margin + 10, header_text)
            
            underline_y_position = height - top_margin + 10 - 5
            c.setLineWidth(1)
            c.line(header_x_position, underline_y_position, header_x_position + text_width, underline_y_position)
            c.setLineWidth(0.5)
            c.line(header_x_position, underline_y_position - 2, header_x_position + text_width, underline_y_position - 2)

            # Add margin below header
            top_margin += 10

            image = Image.open(img)
            img_width, img_height = image.size

            if img_width > (right_margin - left_margin):
                ratio = (right_margin - left_margin) / img_width
                img_width = img_width * ratio
                img_height = img_height * ratio

            if img_height > (bottom_margin - top_margin):
                ratio = (bottom_margin - top_margin) / img_height
                img_width = img_width * ratio
                img_height = img_height * ratio

            x = (width - img_width) / 2
            y = height - top_margin - img_height

            c.drawImage(img, x, y, width=img_width, height=img_height)
            c.showPage()
            top_margin = 50  # Reset top margin for new page

        # Add other images to the PDF, each on a new page
        for img in self.other_images:
            c.setFont("Helvetica-Bold", 24)
            header_text = f"TBT of {self.team_var.get()} - {self.date_entry.get().replace('/', '-')}"
            text_width = c.stringWidth(header_text, "Helvetica-Bold", 24)
            header_x_position = (width - text_width) / 2

            c.drawString(header_x_position, height - top_margin + 10, header_text)
            
            underline_y_position = height - top_margin + 10 - 5
            c.setLineWidth(1)
            c.line(header_x_position, underline_y_position, header_x_position + text_width, underline_y_position)
            c.setLineWidth(0.5)
            c.line(header_x_position, underline_y_position - 2, header_x_position + text_width, underline_y_position - 2)

            # Add margin below header
            top_margin += 10

            image = Image.open(img)
            img_width, img_height = image.size

            if img_width > (right_margin - left_margin):
                ratio = (right_margin - left_margin) / img_width
                img_width = img_width * ratio
                img_height = img_height * ratio

            if img_height > (bottom_margin - top_margin):
                ratio = (bottom_margin - top_margin) / img_height
                img_width = img_width * ratio
                img_height = img_height * ratio

            x = (width - img_width) / 2
            y = height - top_margin - img_height

            c.drawImage(img, x, y, width=img_width, height=img_height)
            c.showPage()
            top_margin = 50  # Reset top margin for new page

        c.save()
        self.update_progress(100)
        messagebox.showinfo("Success", f"TBT of {self.team_var.get()} of {self.date_entry.get().replace('/', '-')}.pdf is saved successfully.")
        self.generate_button.config(state='normal')
        self.whatsapp_button.config(state='normal')

    def update_progress(self, value):
        def smooth_progress():
            current = self.progress['value']
            increment = 0.5  # Smooth increment
            while current < value:
                current += increment
                self.progress['value'] = current
                self.progress_label.config(text=f"Progress: {int(current)}%")
                self.progress.update()
                time.sleep(0.02)  # Adjust speed of progress

        threading.Thread(target=smooth_progress).start()

    def open_whatsapp(self):
        os.system("start https://web.whatsapp.com/")

    def open_linkedin(self):
        os.system("start https://www.linkedin.com/in/soumy-chauhan/")

    def open_instagram(self):
        os.system("start https://www.instagram.com/mrx_3.2/")

if __name__ == "__main__":
    root = tk.Tk()
    app = TBTGenApp(root)
    root.mainloop()
