import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from mtcnn import MTCNN
from tkinter import simpledialog
import os
class FaceLabelingApp(tk.Frame):
    def __init__(self, master):
        # set cac tham so cua cua so window
        self.master = master
        self.master.title("Attendence")
        self.master.rowconfigure(0, minsize=800, weight=1)
        self.master.columnconfigure(1, minsize=800, weight=1)
        #frame
        self.frame_img = tk.Frame(self.master, relief=tk.RAISED, bd=2)
        # Scrollbar
        self.scrollbar_y = tk.Scrollbar(self.frame_img, orient="vertical")
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x = tk.Scrollbar(self.frame_img, orient="horizontal")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas = tk.Canvas(self.frame_img, yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.scrollbar_y.config(command=self.canvas.yview)
        self.scrollbar_x.config(command=self.canvas.xview)
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        
        ##
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()
        ##define button in frame button
        self.frm_buttons = tk.Frame(self.master, relief=tk.RAISED, bd=2)
        self.upload_button = tk.Button(self.frm_buttons, text="Upload Image", command=self.upload_image)
        self.detect_button = tk.Button(self.frm_buttons, text="Detect Face", command=self.detect_face)
        self.label_IDclass = tk.Label(self.frm_buttons, text="ID Class")
        self.combo = ttk.Combobox(self.frm_buttons, values=())
        self.label_student = tk.Label(self.frm_buttons, text="ID Student")
        self.label_entry = tk.Entry(self.frm_buttons)
        #self.label_button = tk.Button(self.frm_buttons, text="Label Face", command=self.label_face)
        #grid frame button
        self.upload_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.detect_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.label_IDclass.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.combo.grid(row=3, column=0, padx=5, pady=5)
        self.label_student.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        self.label_entry.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        #self.label_button.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        #grid frame
        self.frm_buttons.grid(row=0, column=0, sticky="ns")
        self.frame_img.grid(row=0, column=1, sticky="nsew")
        ##
        self.image_path = ""
        self.image = None
        self.faces = []  # Danh sách các bounding box của khuôn mặt
        self.ID_class = "dataset"
        #Event
        self.image_frame.bind("<Configure>", self.on_frame_configure)
        self.image_label.bind("<Button-1>", self.on_click)
        self.update_combobox()
    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if file_path != self.image_path:
                self.image_path = file_path
                self.display_image()

    def display_image(self):
        if self.image_path:
            image = Image.open(self.image_path)
            photo = ImageTk.PhotoImage(image)

            # Cập nhật image_label
            self.image_label.config(image=photo)
            self.image_label.image = photo
    def detect_face(self):
        if self.image_path:
            image = cv2.imread(self.image_path)
            detector = MTCNN()
            self.faces = detector.detect_faces(image)
            # Vẽ hộp xung quanh khuôn mặt đã nhận diện
            for face in self.faces:
                x, y, w, h = face['box']
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            photo = ImageTk.PhotoImage(pil_image)
            # Cập nhật image_label
            self.image_label.config(image=photo)
            self.image_label.image = photo
    def update_combobox(self):
        folder_names = [d for d in os.listdir(self.ID_class) if os.path.isdir(os.path.join(self.ID_class, d))]
        self.combo['values'] = tuple(folder_names)
    def on_frame_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    def on_click(self, event):
        for i, face in enumerate(self.faces):
            x, y, w, h = face['box']
            if x <= event.x <= x + w and y <= event.y <= y + h:
                self.label_face(i)
    def label_face(self, index=None):
        if index is None and self.faces:
            index = 0
        label = self.label_entry.get()
        if label:
            print(f"Labeling face {index + 1} with label: {label}")
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceLabelingApp(root)
    root.mainloop()
