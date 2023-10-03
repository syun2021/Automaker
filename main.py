import os
import json
import ctypes
import pathlib
import shutil
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

class Maker:
    def __init__(self):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)
        except:
            pass

        with open("init_format.json") as f:
            self.form = json.load(f)
        self.set = self.form["set3"]
        self.driver_row = 0
        self.count = False
        self.mode = ["click", "send", "get_text", "get_attribute", "URL open"]
        self.find = ["XPATH", "ID", "NAME", "CLASS_NAME"]
        self.ProgramLabels = []

        self.root = tk.Tk()
        self.control_frame = tk.Frame(self.root)
        self.program_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.LEFT, anchor=tk.N)
        self.program_frame.pack(side=tk.RIGHT, anchor=tk.N, expand=1)

        # self.w, self.h= self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        # self.root.geometry("%dx%d" % (self.w, self.h))
        self.root.geometry("1200x800")
        self.root.protocol("WM_DELETE_WINDOW", exit)
        self.Widget()
        self.main()
        self.__SumPrograms()
        self.__Reload()
        self.root.mainloop()

    def Widget(self):
        url_num = 0
        find_num = 10
        element_num = 20
        entry_element_num = 30
        variable_num = 50
        excute_num = 80
        insert_num = 100
        driver_num = 1000
        Label1 = tk.Label(self.control_frame, text="Entry URL : ")
        Label2 = tk.Label(self.control_frame, text="\tSelect mode : ")
        Label3 = tk.Label(self.control_frame, text="\tHow find : ")
        Label4 = tk.Label(self.control_frame, text="\tEntry elements : ")
        Label5 = tk.Label(self.control_frame, text="Chrome Driver Path : ")
        Label6 = tk.Label(self.control_frame, text="\tSend Text : ")
        Label7 = tk.Label(self.control_frame, text="\tGet variable name : ")
        tk.Label(self.control_frame, text = " ").grid(column=0, row = variable_num-1)
        Label8 = tk.Label(self.control_frame, text="\tSelect row num : ")
        self.Entry1 = ttk.Entry(self.control_frame, width=50)
        self.Entry2 = ttk.Entry(self.control_frame, width=50)
        self.Entry3 = ttk.Entry(self.control_frame, width=40)
        self.Entry3.insert(0, "chromedriver.exe")
        self.Entry4 = ttk.Entry(self.control_frame, width=30)
        self.Entry5 = ttk.Entry(self.control_frame, width=20)
        self.Entry6 = ttk.Entry(self.control_frame, width=5)
        self.Entry7 = ttk.Entry(self.control_frame, width=50)
        self.Entry8 = ttk.Entry(self.control_frame, width=5)
        self.Entry8.insert(0, "1")
        self.Button1 = ttk.Button(self.control_frame, text="Add", command=lambda:self.__Add())
        self.Button2 = ttk.Button(self.control_frame, text="Reload", command=lambda:self.__Reload())
        self.Button3 = ttk.Button(self.control_frame, text="Write", command=lambda:self.__Writer())
        self.Button4 = ttk.Button(self.control_frame, text=":", width=2, command=lambda:self.__driver_update())
        self.Button5 = ttk.Button(self.control_frame, text="Delete", width=6, command=lambda:self.__Delete())
        self.Button6 = ttk.Button(self.control_frame, text="Insert", width=6, command=lambda:self.__Insert())
        self.mode_select = ttk.Combobox(self.control_frame, values=self.mode, state="readonly")
        self.mode_select.set(self.mode[0])
        self.element_select = ttk.Combobox(self.control_frame, values=self.find, state="readonly")
        self.element_select.set([self.find[0]])

        Label1.grid(column=0, row=url_num, pady=5, sticky=tk.E)
        Label2.grid(column=0, row=element_num, pady=1, sticky=tk.E)
        Label3.grid(column=0, row=find_num, pady=1, sticky=tk.E)
        Label4.grid(column=0, row=entry_element_num, pady=1, sticky=tk.E)
        Label5.grid(column=0, row=driver_num, sticky=tk.E)
        Label6.grid(column=0, row=variable_num, sticky=tk.E)
        Label7.grid(column=0, row=variable_num+1, sticky=tk.E)
        Label8.grid(column=0, row=insert_num, sticky=tk.E)
        self.Entry1.grid(column=1, row=url_num)
        self.Entry2.grid(column=1, row=entry_element_num)
        self.Entry3.grid(column=1, row=driver_num)
        self.Entry4.grid(column=1, row=variable_num, sticky=tk.W)
        self.Entry5.grid(column=1, row=variable_num+1, sticky=tk.W)
        self.Entry6.grid(column=1, row=insert_num, sticky=tk.W)
        self.Entry7.grid(column=1, row=insert_num+1, sticky=tk.W)
        self.Entry8.grid(column=0, row=insert_num+1, sticky=tk.E, padx=4)
        self.mode_select.grid(column=1, row=element_num)
        self.element_select.grid(column=1, row=find_num)
        self.Button1.grid(column=1, row=excute_num)
        self.Button2.grid(column=1, row=excute_num+1)
        self.Button3.grid(column=1, row=excute_num+2)
        self.Button4.grid(column=2, row=driver_num, sticky=tk.W)
        self.Button5.grid(column=2, row=insert_num)
        self.Button6.grid(column=2, row=insert_num+1)

    def main(self):
        self.set["class_main"].append("\t\tself.driver = webdriver.Chrome(\"chromedriver.exe\")")
        self.driver_row = len(self.set["class_main"])

    def __Argument(self, name, default):
        self.set["class_main"].append(f"\t\tself.{name} = kwargs.get(\"{name}\", \"{default}\")")
    
    def __Add(self):
        # self.mode = ["click", "send", "get_text", "get_attribute", "URL open"]
        # self.find = ["XPATH", "ID", "NAME", "CLASS_NAME"]
        self.__Reload()
        element = self.Entry2.get()

        if self.element_select.get() == "XPATH":
            find = "By.XPATH"
        elif self.element_select.get() == "ID":
            find = "By.ID"
        elif self.element_select.get() == "NAME":
            find = "By.NAME"
        elif self.element_select.get() == "CLASS_NAME":
            find = "By.CLASS_NAME"

        if self.mode_select.get() == "URL open":
            self.set["main"].append(f"\t\tself.driver.get(\"{self.Entry1.get()}\")")
            self.set["main"].append("\t\tself.driver.implicitly_wait(30)")
            self.set["main"].append("\t\ttime.sleep(1)")

        elif self.mode_select.get() == "click":
            self.set["main"].append(f"\t\tself.driver.find_element({find}, \"{element}\").click()")

        elif self.mode_select.get() == "send":
            text = self.Entry4.get()
            self.set["main"].append(f"\t\tself.driver.find_element({find}, \"{element}\").send_keys(\"{text}\")")

        elif self.mode_select.get() == "get_text":
            args = self.Entry5.get()
            self.set["main"].append(f"\t\t{args} = self.driver.find_element({find}, \"{element}\").text")
        elif self.mode_select.get() == "get_attribute":
            self.set["main"].append(f"\t\t{args} = self.driver.find_element({find}, \"{element}\").get_atribute(\"href\")")
        print(1)
        self.__SumPrograms()
        self.__Reload()

    def __Reload(self):
        if self.count:
            for label in self.ProgramLabels:
                label.grid_forget()
                label.update()
            self.ProgramLabels = []
        
        for num, programs in enumerate(self.sums):  
            self.ProgramLabels.append(tk.Label(self.program_frame, text=f"{num}:\t{programs}"))
        for num, label in enumerate(self.ProgramLabels):
            label.grid(column=0, row=num, sticky = tk.W)
        self.count = True

    def __SumPrograms(self):
        self.sums = []
        for row in self.set["import"]:
            self.sums.append(row)
        for row in self.set["class_main"]:
            self.sums.append(row)
        for row in self.set["main"]:
            self.sums.append(row)
        for row in self.set["call"]:
            self.sums.append(row)

    def __Writer(self):
        # self.__SumPrograms()
        with open("sample.txt", "w") as o:
            for row in self.sums:
                print(row, sep="\n", file=o)
        shutil.move("sample.txt", "sample.py")
        print("Completed!")
    
    def __driver_update(self):
        self.__filedialog_clicked(self.Entry3)
        driver_path = self.Entry3.get()
        self.set["class_main"][self.driver_row-1] = f"\t\tself.driver = webdriver.Chrome(\"{driver_path}\")"
        self.__SumPrograms()
        self.__Reload()

    def __Delete(self):
        num = int(self.Entry6.get())
        self.sums.pop(num)
        self.__Reload()

    def __Insert(self):
        programs = ""
        num = int(self.Entry6.get())
        tabs_num = int(self.Entry8.get())
        variable = self.Entry7.get()
        for i in range(tabs_num):
            programs += "\t"
        programs += variable

        self.sums.insert(num, f"{programs}")
        self.__Reload()

    def __filedialog_clicked(self, entry):
        fType = [("*", ".exe")]
        iFile = os.path.abspath(os.path.dirname(__file__))
        iFilePath = filedialog.askopenfilename(filetype= fType, initialdir=iFile)

        if iFilePath != "":
            entry.delete(0,tk.END)
            entry.insert(0,iFilePath)

if __name__ == "__main__":
    Maker()