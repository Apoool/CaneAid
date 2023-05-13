import tkinter as tk
import subprocess
import platform
import os
import cv2
from datetime import *

class App:
        def __init__(self, master):
                self.master = master
                self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
                self.master.title("CaneAid")
                print("height:" + str(self.master.winfo_screenheight()) + "width:" + str(self.master.winfo_screenwidth()))
                self.master.configure(bg="#EFE7BC")
                self.model_list = []
                self.object_list = []
                self.model = 'model_1'
                self.counter = []
                
                self.check_selected_model()
                self.list_model()
                
                #temporary device info
                
                self.temp_device_name = os.getlogin()
                self.temp_opencv_ver = cv2.__version__
                self.temp_raspberry_os =  f"{platform.system()} {platform.machine()} {platform.release()}"
                self.temp_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.temp_software_version = "CaneAid. ver. 0.5"
                
                
                # Image logo of cane aid
                self.image = tk.PhotoImage(file="/home/caneaid/Desktop/Main/image/CaneAid.png")
                self.label = tk.Label(self.master, image=self.image, height=150, bg="#EFE7BC")
                self.label.pack()
                
                # Frame for menu
                self.menu_frame = tk.Frame(self.master, width=1200, height=100, bg="#EFE7BC")
                self.menu_frame.pack(padx=20, fill="x")        
                
		# Create a dropdown menu list
                self.file_list = tk.StringVar(self.master)
                
                self.dropdown_menu = tk.Menubutton(self.menu_frame, text="Select model", relief="raised", bg="#74BDCB")
                self.dropdown_menu.menu = tk.Menu(self.dropdown_menu, tearoff=0)
                self.dropdown_menu["menu"] = self.dropdown_menu.menu
                self.dropdown_menu.pack(side=tk.TOP, padx=(270, 0), pady=(10,5))
                for model in self.model_list:
                        self.dropdown_menu.menu.add_radiobutton(label=model, variable=self.file_list, value=model, command=lambda value=model: self.update_model(value))
                        
                
                # Frame for general info
                self.general_info_frame = tk.Frame(self.master, width=1200, height=100, bd=5, relief=tk.RIDGE, bg="#EFE7BC")
                self.general_info_frame.pack(padx=20, fill="x")
                
                # Label_frame
                self.label_frame = tk.Frame(self.general_info_frame, bg="#EFE7BC")
                self.label_frame.pack(side=tk.TOP, fill="x")
                
                #Label
                self.device_information_label = tk.Label(self.label_frame, text="Device Information:", font=("Arial", 20), bg="#EFE7BC")
                self.device_information_label.pack(side=tk.LEFT, padx=(0, 400), pady=(5,10))
                self.model_contents_label = tk.Label(self.label_frame, text="Model Contents:", font=("Arial", 20), bg="#EFE7BC")
                self.model_contents_label.pack(side=tk.RIGHT, padx=(0, 390), pady=(5))
                
                
                # Device Information
                self.device_info_frame = tk.Frame(self.general_info_frame,height=100, bg="#EFE7BC")
                self.device_info_frame.pack(side=tk.LEFT, fill="both")
                self.name_label = tk.Label(self.device_info_frame, anchor="w", text=f"Device Name: {self.temp_device_name}", font=("Arial", 12), bg="#EFE7BC")
                self.name_label.pack(side=tk.TOP, pady=(25,10), fill="both")
                self.model_name_label = tk.Label(self.device_info_frame, anchor="w", text=f"Model Used: {self.model}", font=("Arial", 12), bg="#EFE7BC")
                self.model_name_label.pack(side=tk.TOP, pady=12, fill="both")
                self.open_cv_label = tk.Label(self.device_info_frame, anchor="w", text=f"Open CV Version: {self.temp_opencv_ver}", font=("Arial", 12), bg="#EFE7BC")
                self.open_cv_label.pack(side=tk.TOP, pady=12, fill="both")
                self.raspberry_os_label = tk.Label(self.device_info_frame, anchor="w", text=f"Raspberry OS: {self.temp_raspberry_os}", font=("Arial", 12), bg="#EFE7BC")
                self.raspberry_os_label.pack(side=tk.TOP, pady=12, fill="both")
                self.update_label = tk.Label(self.device_info_frame, anchor="w", text=f"Updated On: {self.temp_update}", font=("Arial", 12), bg="#EFE7BC")
                self.update_label.pack(side=tk.TOP, pady=12, fill="both")
                self.software_application_label = tk.Label(self.device_info_frame, anchor="w", text=f"Software Version: {self.temp_software_version}", font=("Arial", 12), bg="#EFE7BC")
                self.software_application_label.pack(side=tk.TOP, pady=12, fill="both")
                
                # Create a listbox to display the counter
                self.object_listbox = tk.Listbox(self.general_info_frame, font=("Arial", 20), height=10, bd=5, relief=tk.SUNKEN)
                self.object_listbox.pack(side=tk.RIGHT, padx=(0, 280), pady=(5))
        
                # Frame for buttons
                self.button_frame = tk.Frame(self.master, bg="#EFE7BC")
                self.button_frame.pack(pady=10)        
        
                # Create a button that starts the program
                self.save_button = tk.Button(self.button_frame, text="Save & Restart", font=("Arial", 24), state="disabled", command=self.restart_system, bg="#74BDCB")
                self.save_button.pack(side=tk.LEFT, padx=10)
                # Create a button that stops the program
                #self.stop_button = tk.Button(self.button_frame, text="Restart", font=("Arial", 30), command="")
                #self.stop_button.pack(side=tk.LEFT, padx=10)
                
                
                self.list_model_entity()

                
        def list_model(self):
                current_dir = os.getcwd() + "/Desktop/Main/models_dir"
                files = os.listdir(current_dir)
                for file_name in files:
                        if not file_name.endswith("txt"):
                                self.model_list.append(file_name)
                
        def check_selected_model(self):
                selected_model = os.getcwd() + "/Desktop/Main/models_dir/selected_model.txt"
                with open(selected_model, 'r') as file:
                        self.model = file.readline().replace('\n', '')
                        #print(self.model)
                                
        def update_model(self, value):
                selected_model = os.getcwd() + "/Desktop/Main/models_dir/selected_model.txt"
                self.model = value
                print(self.model)
                self.model_name_label.config(text=f"Model Used: {self.model}")
                self.object_listbox.delete(0, 'end')
                self.list_model_entity()
                with open(selected_model, 'w') as file:
                        file.writelines(self.model)
                        print(self.model)
                self.save_button.config(state="normal")
                
        def restart_system(self):
                os.system("sudo reboot")
                
        def list_model_entity(self):
                model_files = os.getcwd() + "/Desktop/Main/models_dir/" + self.model + "/labelmap.txt"
                list_model_files = os.getcwd() + "/Desktop/Main/models_dir/" + self.model
                temp_list = []
                self.object_list = []
                
                if not os.listdir(list_model_files):
                        print("empty")
                else:
                        with open(model_files, 'r') as file:
                                file_lines = file.readlines()
                                temp_list.extend(file_lines)
                                
                                
                        for obj in temp_list:
                                temp_obj = obj.replace('\n', '')
                                self.object_list.append(temp_obj)
                        self.object_list = [obj for obj in self.object_list if obj != "???"]
                        for obj in self.object_list:
                                self.object_listbox.insert(tk.END, obj.capitalize())
                        print(self.object_list)
                
        

root = tk.Tk()
app = App(root)
root.mainloop()
