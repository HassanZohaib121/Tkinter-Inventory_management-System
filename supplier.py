from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3


class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600+220+130")
        self.root.iconbitmap("images/main.ico")
        self.root.title(
            "Inventory Management System  |  Developed by Hassan Zohaib")
        self.root.config(bg="white")
        self.root.focus_force()
        root.resizable(False, False)

        # ----All Variables------
        # -----Search Variables--
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        # ------Variables---------
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_contact = StringVar()

        # -----Search Frame-------
        SearchFrame = LabelFrame(self.root, text="Search Supplier", font=(
            "goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=200, y=20, height=70, width=600)

        # ----Search options------
        cmb_search = ttk.Combobox(SearchFrame, values=(
            "Select", "invoice", "Name", "Email"), textvariable=self.var_searchby, state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, font=(
            "goudy old style", 15), textvariable=self.var_searchtxt, bd=2, bg="lightyellow")
        txt_search.place(x=200, y=10, width=200)

        search_btn = Button(SearchFrame, command=self.search, text="Search", font=(
            "goudy old style", 10), bg="#4caf50", fg="white", bd=2, cursor="hand2")
        search_btn.place(x=430, y=9, width=150)

        # --------Label-----------
        self.lbl_main = Label(self.root, text="Supplier Detail",
                              font=("goudy old style", 15, "bold"), bg="#4b4de3", fg="white",)
        self.lbl_main.place(x=10, y=100, width=980, height=50)

        # --------Content---------

        # --------row1----------
        lbl_sup_invoice = Label(self.root, text="Invoice No.", bg="white",
                                font=("goudy old style", 15, "bold")).place(x=5, y=160)

        # --------Entry row1 ---------
        sup_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=120, y=160)

        # --------row2---------
        lbl_name = Label(self.root, text="Name", bg="white",
                         font=("goudy old style", 15, "bold")).place(x=5, y=220)

        # --------Entry row2 ---------
        entry_name = Entry(self.root, textvariable=self.var_name, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=120, y=220)

        # ---------row3--------
        lbl_email = Label(self.root, text="Email", bg="white",
                          font=("goudy old style", 15, "bold")).place(x=5, y=280)

        # --------Entry row3 ---------
        entry_email = Entry(self.root, textvariable=self.var_email, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=120, y=280)

        # --------row4--------
        lbl_detail = Label(self.root, text="Details", bg="white",
                           font=("goudy old style", 15, "bold")).place(x=5, y=340)

        # --------Entry row4----------
        self.txt_detail = Text(self.root, font=(
            "goudy old style", 15), bd=2, bg="lightyellow")
        self.txt_detail.place(x=120, y=340, width=300, height=75)

        # --------Buttons-----------
        Save_btn = Button(self.root, command=self.save, text="Save", font=(
            "goudy old style", 10), bg="#0b6deb", fg="white", bd=2, cursor="hand2")
        Save_btn.place(x=10, y=500, width=100)
        Update_btn = Button(self.root, command=self.update, text="Update", font=(
            "goudy old style", 10), bg="#4caf50", fg="white", bd=2, cursor="hand2")
        Update_btn.place(x=130, y=500, width=100)
        Delete_btn = Button(self.root, command=self.delete, text="Delete", font=(
            "goudy old style", 10), bg="#e90909", fg="white", bd=2, cursor="hand2")
        Delete_btn.place(x=250, y=500, width=100)
        Clear_btn = Button(self.root, command=self.clear, text="Clear", font=(
            "goudy old style", 10), bg="#848688", fg="white", bd=2, cursor="hand2")
        Clear_btn.place(x=370, y=500, width=100)

        # ----supplier Details----
        sup_frame = Frame(self.root, bd=2, relief=RIDGE)
        sup_frame.place(x=480, y=150, width=510, height=450)

        scrolly = Scrollbar(sup_frame, orient=VERTICAL)
        scrollx = Scrollbar(sup_frame, orient=HORIZONTAL)

        self.SupplierTable = ttk.Treeview(sup_frame, columns=(
            "invoice", "name", "email", "contact", "detail"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("invoice", text="Invoice no.")
        self.SupplierTable.heading("name", text="Name")
        self.SupplierTable.heading("email", text="Email")
        self.SupplierTable.heading("contact", text="Contact")
        self.SupplierTable.heading("detail", text="Detail")
        self.SupplierTable["show"] = "headings"

        self.SupplierTable.column("invoice", width=30)
        self.SupplierTable.column("name",  width=30)
        self.SupplierTable.column("email",  width=30)
        self.SupplierTable.column("contact", width=30)
        self.SupplierTable.pack(fill=BOTH, expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # --------------------Functions------------------------

    # -------------------Save Button-----------------------

    def save(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror(
                    "Error", "Invoice is Required.", parent=self.root)
            else:
                cursor.execute(
                    "Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cursor.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "Invoice is already assigned.", parent=self.root)
                else:
                    cursor.execute(
                        "Insert into supplier(invoice , name , email , contact , detail) values(?,?,?,?,?)", (
                            self.var_sup_invoice.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_contact.get(),
                            self.txt_detail.get("1.0", END)
                        ))
                    conn.commit()
                    messagebox.showinfo(
                        "Success", "Supplier Added Successfully!", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # ----------Show Data in Tree View ---------------------

    def show(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            cursor.execute("Select * From supplier")
            rows = cursor.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # -----------Put Data in Fields------------------

    def get_data(self, ev):
        f = self.SupplierTable.focus()
        content = (self.SupplierTable.item(f))
        row = content['values']

        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_contact.set(row[3])
        self.txt_detail.delete("1.0", END)
        self.txt_detail.insert(END, row[4])

    # -----------Update Button--------------

    def update(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror(
                    "Error", "Invoice is Required.", parent=self.root)
            else:
                cursor.execute(
                    "Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Invoice!", parent=self.root)
                else:
                    cursor.execute(
                        "Update supplier set name=? ,email=? , contact=?, detail=?  where invoice=?", (
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_contact.get(),
                            self.txt_detail.get("1.0", END),
                            self.var_sup_invoice.get()
                        ))
                    conn.commit()
                    messagebox.showinfo(
                        "Success", "supplier Updated Successfully!", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # -------Delete Button------------
    def delete(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror(
                    "Error", "Invoice is Required.", parent=self.root)
            else:
                cursor.execute(
                    "Select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Invoice!", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you want to delete the supplier?", parent=self.root)
                    if op == True:
                        cursor.execute("delete from supplier where invoice=?",
                                       (self.var_sup_invoice.get(),))
                        conn.commit()
                        messagebox.showinfo(
                            "Delete", "supplier Deleted Successfully!", parent=self.root)
                        self.show()
                        self.clear()

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # -------Clear Button--------------
    def clear(self):
        self.var_sup_invoice.set(""),
        self.var_name.set(""),
        self.var_email.set(""),
        self.var_contact.set(""),
        self.txt_detail.delete("1.0", END),

        self.var_searchby.set("Select")
        self.var_searchtxt.set("")

        self.show()

    # -------Search--------------

    def search(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror(
                    "Error", "Select the meathod to search by.", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror(
                    "Error", "Select area should not be empty!", parent=self.root)
            else:
                cursor.execute("Select * From supplier where " +
                               self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cursor.fetchall()
                if len(rows) != 0:
                    self.SupplierTable.delete(
                        *self.SupplierTable.get_children())
                    for row in rows:
                        self.SupplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No Record Found!", parent=self.root)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()
