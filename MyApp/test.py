import os
import tkinter as tk
from tkinter import ttk

def update_combobox():
    folder_names = [d for d in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, d))]
    combo['values'] = tuple(folder_names)

# Thư mục chính
main_folder = "dataset"

# Tạo cửa sổ chính
root = tk.Tk()
root.title("ComboBox từ Tên Thư mục")

# Tạo ComboBox
combo = ttk.Combobox(root, values=())
combo.grid(row=0, column=0, padx=10, pady=10)

# Nút để cập nhật ComboBox
update_button = tk.Button(root, text="Cập nhật", command=update_combobox)
update_button.grid(row=0, column=1, padx=10, pady=10)

# Mỗi khi cần, gọi hàm update_combobox để cập nhật ComboBox
update_combobox()

root.mainloop()
