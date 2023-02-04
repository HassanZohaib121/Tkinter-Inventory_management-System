from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3


class productClass:
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
        self.var_category = StringVar()
        self.var_supplier = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_barcode = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()
        self.var_status = StringVar()
        self.var_quantity = StringVar()

        # -----Search Frame-------
        SearchFrame = LabelFrame(self.root, text="Search Product", font=(
            "goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=200, y=20, height=70, width=600)

        # ----Search options------
        cmb_search = ttk.Combobox(SearchFrame, values=(
            "Select", "Bar Code", "Category", "Name", "Supplier"), textvariable=self.var_searchby, state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, font=(
            "goudy old style", 15), textvariable=self.var_searchtxt, bd=2, bg="lightyellow")
        txt_search.place(x=200, y=10, width=200)

        search_btn = Button(SearchFrame, command=self.search, text="Search", font=(
            "goudy old style", 10), bg="#4caf50", fg="white", bd=2, cursor="hand2")
        search_btn.place(x=430, y=9, width=150)

        # --------Title-----------
        self.lbl_main = Label(self.root, text="Manage Product Detail",
                              font=("goudy old style", 15, "bold"), bg="#4b4de3", fg="white",)
        self.lbl_main.place(x=10, y=100, width=980, height=50)

        # --------Content---------

        # ---------row1--------
        lbl_barcode = Label(self.root, text="Barcode", bg="white",
                            font=("goudy old style", 15, "bold")).place(x=5, y=170)

        # --------Entry row1 ---------
        entry_barcode = Entry(self.root, textvariable=self.var_barcode, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=120, y=170)

        # --------row2----------
        lbl_name = Label(self.root, text="Name", bg="white",
                         font=("goudy old style", 15, "bold")).place(x=5, y=230)

        # --------Entry row2 ---------
        entry_name = Entry(self.root, textvariable=self.var_name, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=120, y=230)

        # --------row3---------
        lbl_price = Label(self.root, text="Price", bg="white",
                          font=("goudy old style", 15, "bold")).place(x=5, y=280)

        # --------Entry row3 ---------
        entry_price = Entry(self.root, textvariable=self.var_price, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=120, y=280)

        # ----------row4-----------

        lbl_quantity = Label(self.root, text="Quantity", bg="white",
                             font=("goudy old style", 15, "bold")).place(x=5, y=330)

        # --------Entry row4 ---------
        entry_quantity = Entry(self.root, textvariable=self.var_quantity, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=120, y=330)

        # --------row5--------
        lbl_category = Label(self.root, text="Category", bg="white",
                             font=("goudy old style", 15, "bold")).place(x=5, y=380)

        # --------Entry row5----------
        entry_category = ttk.Combobox(self.root, textvariable=self.var_category, values=self.cat_list,
                                      state='readonly', justify=CENTER, font=("goudy old style", 15))
        entry_category.place(x=120, y=380, width=150)
        entry_category.current(0)

        # --------row6--------
        lbl_supplier = Label(self.root, text="Supplier", bg="white",
                             font=("goudy old style", 15, "bold")).place(x=5, y=430)

        # --------Entry row6----------
        entry_supplier = ttk.Combobox(self.root, textvariable=self.var_supplier, values=self.sup_list,
                                      state='readonly', justify=CENTER, font=("goudy old style", 15))
        entry_supplier.place(x=120, y=430, width=150)
        entry_supplier.current(0)

        # --------row7--------
        lbl_status = Label(self.root, text="Status", bg="white",
                           font=("goudy old style", 15, "bold")).place(x=5, y=480)

        # --------Entry row7----------
        entry_status = ttk.Combobox(self.root, textvariable=self.var_status, values=("Active", "Inactive"),
                                    state='readonly', justify=CENTER, font=("goudy old style", 15))
        entry_status.place(x=120, y=480, width=150)
        entry_status.current(0)

        # --------Buttons-----------
        Save_btn = Button(self.root, command=self.save, text="Save", font=(
            "goudy old style", 10), bg="#0b6deb", fg="white", bd=2, cursor="hand2")
        Save_btn.place(x=10, y=550, width=100)
        Update_btn = Button(self.root, command=self.update, text="Update", font=(
            "goudy old style", 10), bg="#4caf50", fg="white", bd=2, cursor="hand2")
        Update_btn.place(x=130, y=550, width=100)
        Delete_btn = Button(self.root, command=self.delete, text="Delete", font=(
            "goudy old style", 10), bg="#e90909", fg="white", bd=2, cursor="hand2")
        Delete_btn.place(x=250, y=550, width=100)
        Clear_btn = Button(self.root, command=self.clear, text="Clear", font=(
            "goudy old style", 10), bg="#848688", fg="white", bd=2, cursor="hand2")
        Clear_btn.place(x=370, y=550, width=100)

        # ----supplier Details----
        sup_frame = Frame(self.root, bd=2, relief=RIDGE)
        sup_frame.place(x=480, y=150, width=510, height=450)

        scrolly = Scrollbar(sup_frame, orient=VERTICAL)
        scrollx = Scrollbar(sup_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(sup_frame, columns=(
            "barcode", "name", "price", "quantity", "status", "category", "supplier"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("barcode", text="Barcode")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("quantity", text="Quantity")
        self.ProductTable.heading("category", text="Category")
        self.ProductTable.heading("supplier", text="Supplier")
        self.ProductTable.heading("status", text="Status")
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("barcode", width=30)
        self.ProductTable.column("name",  width=30)
        self.ProductTable.column("price",  width=30)
        self.ProductTable.column("quantity",  width=30)
        self.ProductTable.column("category", width=30)
        self.ProductTable.column("supplier", width=30)
        self.ProductTable.column("status", width=30)
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # --------------------Functions------------------------

    # ------------fetch category and suppliers--------------

    def fetch_cat_sup(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            cursor.execute("Select name from category")
            cat = cursor.fetchall()
            self.cat_list.append("Empty")
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cursor.execute("Select name from supplier")
            sup = cursor.fetchall()
            self.sup_list.append("Empty")
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # -------------------Save Button-----------------------

    def save(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_barcode.get() == "":
                messagebox.showerror(
                    "Error", "Barcode is Required.", parent=self.root)
            else:
                cursor.execute(
                    "Select * from product where barcode=?", (self.var_barcode.get(),))
                row = cursor.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "Barcode is already assigned.", parent=self.root)
                else:
                    cursor.execute(
                        "Insert into product(barcode , name , price , quantity, category, supplier, status) values(?,?,?,?,?,?,?)", (
                            self.var_barcode.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_quantity.get(),
                            self.var_category.get(),
                            self.var_supplier.get(),
                            self.var_status.get()
                        ))
                    conn.commit()
                    messagebox.showinfo(
                        "Success", "Product Added Successfully!", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # ----------Show Data in Tree View ---------------------

    def show(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            cursor.execute("Select * From product")
            rows = cursor.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # -----------Put Data in Fields------------------

    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']

        self.var_barcode.set(row[0])
        self.var_name.set(row[1])
        self.var_price.set(row[2])
        self.var_quantity.set(row[3])
        self.var_category.set(row[4])
        self.var_supplier.set(row[5])
        self.var_status.set(row[6])

    # -----------Update Button--------------

    def update(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_barcode.get() == "":
                messagebox.showerror(
                    "Error", "Barcodee is Required.", parent=self.root)
            else:
                cursor.execute(
                    "Select * from product where barcode=?", (self.var_barcode.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Barcode!", parent=self.root)
                else:
                    cursor.execute(
                        "Update product set name=? ,price=?, quantity=?, category=?, supplier=?, status=?  where barcode=?", (
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_quantity.get(),
                            self.var_category.get(),
                            self.var_supplier.get(),
                            self.var_status.get(),
                            self.var_barcode.get()
                        ))
                    conn.commit()
                    messagebox.showinfo(
                        "Success", "Product Updated Successfully!", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # -------Delete Button------------
    def delete(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_barcode.get() == "":
                messagebox.showerror(
                    "Error", "Barcode is Required.", parent=self.root)
            else:
                cursor.execute(
                    "Select * from product where barcode=?", (self.var_barcode.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Barcode!", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you want to delete the product?", parent=self.root)
                    if op == True:
                        cursor.execute("delete from product where barcode=?",
                                       (self.var_barcode.get(),))
                        conn.commit()
                        messagebox.showinfo(
                            "Delete", "Product Deleted Successfully!", parent=self.root)
                        self.show()
                        self.clear()

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # -------Clear Button--------------
    def clear(self):
        self.var_barcode.set(""),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_quantity.set(""),
        self.var_category.set("Select"),
        self.var_supplier.set("Select"),
        self.var_status.set("Active"),

        self.var_searchby.set("Select"),
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
                # check if the user selected barcode as the method to search by
                if self.var_searchby.get() == "Bar Code":
                    cursor.execute(
                        "SELECT * FROM product WHERE barcode = ?", (self.var_searchtxt.get(),))
                else:
                    cursor.execute("SELECT * FROM product WHERE " + self.var_searchby.get() +
                                   " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cursor.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(
                        *self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No Record Found!", parent=self.root)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()

    obj = productClass(root)
    root.mainloop()
