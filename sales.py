from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os


class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x550+220+130")
        self.root.iconbitmap("images/main.ico")
        self.root.title(
            "Inventory Management System  |  Developed by Hassan Zohaib")
        self.root.config(bg="white")
        self.root.focus_force()
        root.resizable(False, False)

        self.var_entry = StringVar()
        self.bill_list = []

        # --------Title-----------
        lbl_main = Label(self.root, text="Customer Sales Area",
                         font=("goudy old style", 15, "bold"), bg="#4b4de3", fg="white",)
        lbl_main.place(x=0, y=0, width=1000, height=50)

        lbl_invoice = Label(
            self.root, text="Invoice No.", font=("goudy old style", 12, "bold"))
        lbl_invoice.place(x=20, y=80, height=50)

        entry_invoice = Entry(
            self.root, textvariable=self.var_entry, font=("goudy old style", 15, "bold"), bg="lightyellow")
        entry_invoice.place(x=120, y=90, width=200, height=30)

        btn_search = Button(
            self.root, text="Search", command=self.search, bg="#2196f3", fg="white", font=("goudy old style", 12, "bold"), cursor="hand2").place(x=340, y=90, width=120, height=30)
        btn_clear = Button(
            self.root, text="Clear", command=self.clear, bg="lightgray", font=("goudy old style", 12, "bold"), cursor="hand2").place(x=480, y=90, width=120, height=30)

        # --------Frame------------

        # -------Bill List---------

        customer_frame = Frame(self.root, relief=RIDGE, bd=2)
        customer_frame.place(x=30, y=140, width=200, height=330)

        scrolly = Scrollbar(customer_frame, orient=VERTICAL)
        self.sales_list = Listbox(
            customer_frame, font=("goudy old style", 12, "bold"), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH, expand=1)
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)

        # --------Bill Area------------

        bill_frame = Frame(self.root, relief=RIDGE, bd=2)
        bill_frame.place(x=250, y=140, width=410, height=330)

        lbl_bill_area = Label(bill_frame, text="Customer Bill Area",
                              font=("goudy old style", 20, "bold"), bg="orange").pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_frame, orient=VERTICAL)
        self.bill_area = Text(
            bill_frame, font=("goudy old style", 12, "bold"), bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        # ---------image------------
        self.bill_photo = Image.open("images/bill_area.png")
        self.bill_photo = self.bill_photo.resize(
            (300, 272), Image.Resampling.LANCZOS)
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        lbl_image = Label(self.root, image=self.bill_photo)
        lbl_image.place(x=680, y=150)
        self.show()

    # ------------------------------Functions--------------------------------------
    def show(self):
        self.sales_list.delete(0, END)
        for i in os.listdir('bill'):
            if i.split('.')[-1] == 'txt':
                self.sales_list.insert(END, i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self, ev):
        index_ = self.sales_list.curselection()
        file_name = self.sales_list.get(index_)
        self.bill_area.delete('1.0', END)
        fp = open(f'bill/{file_name}', 'r')
        for i in fp:
            self.bill_area.insert(END, i)
        fp.close()

    def search(self):
        if self.var_entry.get() == "":
            messagebox.showerror(
                "Error", "Invoice no. is Requireed!", parent=self.root)
        else:
            if self.var_entry.get() in self.bill_list:
                fp = open(f'bill/{self.var_entry.get()}.txt', 'r')
                self.bill_area.delete('1.0', END)
                for i in fp:
                    self.bill_area.insert(END, i)
                fp.close()
            else:
                messagebox.showerror(
                    "Error", "Invalid Invoice number!", parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0', END)
        self.var_entry.set("")


if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
