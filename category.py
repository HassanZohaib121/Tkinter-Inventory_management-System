from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3


class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("730x250+350+330")
        self.root.iconbitmap("images/main.ico")
        self.root.title(
            "Inventory Management System  |  Developed by Hassan Zohaib")
        self.root.config(bg="white")
        self.root.focus_force()
        root.resizable(False, False)

        self.var_cid = StringVar()
        self.var_category = StringVar()

        # --------Labels-----------
        self.lbl_main = Label(self.root, text="Manage Categories",
                              font=("goudy old style", 15, "bold"), bg="#4b4de3", fg="white")
        self.lbl_main.place(x=10, y=10, width=710, height=50)

        self.lbl_enter = Label(self.root, text="Enter Category Name",
                               font=("goudy old style", 15, "bold"), bg="#4b4de3", fg="white")
        self.lbl_enter.place(x=30, y=100)

        # -------Entry Field-------
        self.entry_category = Entry(self.root, textvariable=self.var_category, font=(
            "goudy old style", 15), bd=2, bg="lightyellow")
        self.entry_category.place(x=30, y=150, width=310)

        # --------Button-----------
        self.btn_add = Button(self.root, text="Add", command=self.add, font=(
            "goudy old style", 10), bg="#4caf50", fg="white", bd=2, cursor="hand2")
        self.btn_add.place(x=30, y=200, width=140)

        self.btn_del = Button(self.root, text="Delete", command=self.delete, font=(
            "goudy old style", 10), bg="#e90909", fg="white", bd=2, cursor="hand2")
        self.btn_del.place(x=200, y=200, width=140)

        # -------Tree View-----------
        category_frame = Frame(self.root, bd=2, relief=RIDGE)
        category_frame.place(x=350, y=90, width=380, height=150)

        scrolly = Scrollbar(category_frame, orient=VERTICAL)
        scrollx = Scrollbar(category_frame, orient=HORIZONTAL)

        self.CategoryTable = ttk.Treeview(category_frame, columns=(
            "CID", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)

        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("CID", text="Category ID")
        self.CategoryTable.heading("name", text="Name")
        self.CategoryTable["show"] = "headings"

        self.CategoryTable.column("CID", width=30)
        self.CategoryTable.column("name",  width=30)
        self.CategoryTable.pack(fill=BOTH, expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # ------Functions-------------

    # ------------Add---------------

    def add(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_category.get() == "":
                messagebox.showerror(
                    "Error", "Category name is required.", parent=self.root)
            else:
                cursor.execute("SELECT * FROM category WHERE name=?",
                               (self.var_category.get(),))
                row = cursor.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "Category already exists.", parent=self.root)
                else:
                    cursor.execute(
                        "INSERT INTO category(name) values(?)", (self.var_category.get(),))
                    conn.commit()
                    messagebox.showinfo(
                        "Success", "Category added successfully!", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to: {str(ex)}", parent=self.root)
            conn.rollback()
        finally:
            conn.close()

    # -------------Delete---------------
    def delete(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_cid.get() == "":
                messagebox.showerror(
                    "Error", "Please Select the Category From List!.", parent=self.root)
            else:
                cursor.execute(
                    "SELECT * FROM category WHERE cid=?", (self.var_cid.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid category!", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you want to delete the category?", parent=self.root)
                    if op == True:
                        cursor.execute(
                            "delete from category where cid=?", (self.var_cid.get(),))
                        conn.commit()
                        messagebox.showinfo(
                            "Delete", "category Deleted Successfully!", parent=self.root)
                        self.show()
                        self.clear()

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to: {str(ex)}", parent=self.root)
            conn.rollback()
        finally:
            conn.close()

    #  # ----------Show Data in Tree View ---------------------

    def show(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            cursor.execute("Select * From category")
            rows = cursor.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # ---------Clear-----------

    def clear(self):
        self.var_cid.set("")
        self.var_category.set("")

        self.show()

    # -----------Put Data in Fields------------------

    def get_data(self, ev):
        f = self.CategoryTable.focus()
        content = (self.CategoryTable.item(f))
        row = content['values']

        self.var_cid.set(row[0])
        self.var_category.set(row[1])


if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
