from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import bcrypt


class employeeClass:
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
        self.var_emp_id = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_pass = StringVar()
        self.var_contact = StringVar()
        self.var_doj = StringVar()
        self.var_usr_type = StringVar()
        self.var_salary = StringVar()

        # -----Search Frame-------
        SearchFrame = LabelFrame(self.root, text="Search Employee", font=(
            "goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=200, y=20, height=70, width=600)

        # ----Search options------
        cmb_search = ttk.Combobox(SearchFrame, values=(
            "Select", "emp_id", "Name", "Email"), textvariable=self.var_searchby, state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, font=(
            "goudy old style", 15), textvariable=self.var_searchtxt, bd=2, bg="lightyellow")
        txt_search.place(x=200, y=10, width=200)

        search_btn = Button(SearchFrame, command=self.search, text="Search", font=(
            "goudy old style", 10), bg="#4caf50", fg="white", bd=2, cursor="hand2")
        search_btn.place(x=430, y=9, width=150)

        # --------Label-----------
        self.lbl_main = Label(self.root, text="Employee Detail",
                              font=("goudy old style", 15, "bold"), bg="#4b4de3", fg="white",)
        self.lbl_main.place(x=10, y=100, width=980, height=50)

        # --------Content---------

        # --------row1----------
        lbl_empid = Label(self.root, text="Emp No.", bg="white",
                          font=("goudy old style", 15, "bold")).place(x=5, y=160)
        lbl_gender = Label(self.root, text="Gender", bg="white",
                           font=("goudy old style", 15, "bold")).place(x=330, y=160)
        lbl_contact = Label(self.root, text="Contact", bg="white",
                            font=("goudy old style", 15, "bold")).place(x=650, y=160)

        # --------Entry row1 ---------
        entry_Id = Entry(self.root, textvariable=self.var_emp_id, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=100, y=160)

        entry_Gender = ttk.Combobox(self.root, values=("Select", "Male", "Female", "Others"), textvariable=self.var_gender,
                                    state='readonly', justify=CENTER, font=("goudy old style", 15))
        entry_Gender.place(x=420, y=160, width=150)
        entry_Gender.current(0)

        entry_Contact = Entry(self.root, textvariable=self.var_contact, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=750, y=160)

        # --------row2---------
        lbl_name = Label(self.root, text="Name", bg="white",
                         font=("goudy old style", 15, "bold")).place(x=5, y=220)
        lbl_dob = Label(self.root, text="D.O.B", bg="white",
                        font=("goudy old style", 15, "bold")).place(x=330, y=220)
        lbl_doj = Label(self.root, text="D.O.J", bg="white",
                        font=("goudy old style", 15, "bold")).place(x=650, y=220)

        # --------Entry row2 ---------
        entry_name = Entry(self.root, textvariable=self.var_name, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=100, y=220)
        entry_dob = Entry(self.root, textvariable=self.var_dob, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=420, y=220)
        entry_doj = Entry(self.root, textvariable=self.var_doj, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=750, y=220)

        # ---------row3--------
        lbl_email = Label(self.root, text="Email", bg="white",
                          font=("goudy old style", 15, "bold")).place(x=5, y=280)
        lbl_pass = Label(self.root, text="Password", bg="white",
                         font=("goudy old style", 13, "bold")).place(x=330, y=280)
        lbl_usr_type = Label(self.root, text="User Type", bg="white",
                             font=("goudy old style", 15, "bold")).place(x=650, y=280)

        # --------Entry row3 ---------
        entry_email = Entry(self.root, textvariable=self.var_email, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=100, y=280)
        entry_pass = Entry(self.root, textvariable=self.var_pass, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=420, y=280)
        entry_usr_type = ttk.Combobox(self.root, textvariable=self.var_usr_type, values=("Admin", "Employee"),
                                      state='readonly', justify=CENTER, font=("goudy old style", 15))
        entry_usr_type.place(x=760, y=280, width=150)
        entry_usr_type.current(0)

        # --------row4--------
        lbl_address = Label(self.root, text="Address", bg="white",
                            font=("goudy old style", 15, "bold")).place(x=5, y=340)
        lbl_salary = Label(self.root, text="Salary", bg="white",
                           font=("goudy old style", 15, "bold")).place(x=400, y=340)

        # --------Entry row4----------
        self.txt_address = Text(self.root, font=(
            "goudy old style", 15), bd=2, bg="lightyellow")
        self.txt_address.place(x=100, y=340, width=300, height=75)
        entry_salary = Entry(self.root, textvariable=self.var_salary, font=(
            "goudy old style", 15), bd=2, bg="lightyellow").place(x=500, y=340)

        # --------Buttons-----------
        Save_btn = Button(self.root, command=self.save, text="Save", font=(
            "goudy old style", 10), bg="#0b6deb", fg="white", bd=2, cursor="hand2")
        Save_btn.place(x=420, y=380, width=100)
        Update_btn = Button(self.root, command=self.update, text="Update", font=(
            "goudy old style", 10), bg="#4caf50", fg="white", bd=2, cursor="hand2")
        Update_btn.place(x=540, y=380, width=100)
        Delete_btn = Button(self.root, command=self.delete, text="Delete", font=(
            "goudy old style", 10), bg="#e90909", fg="white", bd=2, cursor="hand2")
        Delete_btn.place(x=660, y=380, width=100)
        Clear_btn = Button(self.root, command=self.clear, text="Clear", font=(
            "goudy old style", 10), bg="#848688", fg="white", bd=2, cursor="hand2")
        Clear_btn.place(x=780, y=380, width=100)

        # ----Employee Details----
        emp_frame = Frame(self.root, bd=2, relief=RIDGE)
        emp_frame.place(x=0, y=450, relwidth=1, height=150)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=(
            "emp_id", "name", "email", "gender", "dob",  "contact", "doj", "usr_type", "address", "salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("emp_id", text=" Employee ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("dob", text="Date of Birth")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("doj", text="Date of joining")
        self.EmployeeTable.heading("usr_type", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")
        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.column("emp_id", width=30)
        self.EmployeeTable.column("name",  width=100)
        self.EmployeeTable.column("email",  width=100)
        self.EmployeeTable.column("gender",  width=100)
        self.EmployeeTable.column("dob",  width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("doj",  width=100)
        self.EmployeeTable.column("usr_type",  width=100)
        self.EmployeeTable.column("salary", width=100)
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # --------------------Functions------------------------

    # -------------------Save Button-----------------------

    def save(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror(
                    "Error", "Employee's ID is Required.", parent=self.root)
            else:
                cursor.execute(
                    "Select * from employee where emp_id=?", (self.var_emp_id.get(),))
                row = cursor.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "Employee's ID is already assigned.", parent=self.root)
                else:
                    # cursor.execute(
                    #     "Select auth from Login where name=?", (self.var_name.get(),))
                    # column = cursor.fetchone()[0]
                    if self.var_usr_type.get() == 'Admin':
                        messagebox.showerror(
                            "Error", "Only one Admin is Allowed.", parent=self.root)
                    elif self.var_pass.get() == "":
                        messagebox.showerror(
                            "Error", "Password is required!", parent=self.root)
                    else:
                        password = str(self.var_pass.get())
                        password_bytes = bytes(password, 'utf-8')
                        salt = bcrypt.gensalt()
                        hash = bcrypt.hashpw(password_bytes, salt)

                        cursor.execute(
                            "Insert into employee(emp_id , name , email , gender , dob , contact , doj , usr_type , address , salary) values(?,?,?,?,?,?,?,?,?,?)", (
                                self.var_emp_id.get(),
                                self.var_name.get(),
                                self.var_email.get(),
                                self.var_gender.get(),
                                self.var_dob.get(),
                                self.var_contact.get(),
                                self.var_doj.get(),
                                self.var_usr_type.get(),
                                self.txt_address.get("1.0", END),
                                self.var_salary.get()
                            ))
                        cursor.execute(
                            "Insert into Login(name, pass, auth) values(? , ?, ?)", (
                                self.var_name.get(),
                                hash,
                                self.var_usr_type.get()
                            ))
                        conn.commit()
                        messagebox.showinfo(
                            "Success", "Employee Added Successfully!", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # ----------Show Data in Tree View ---------------------

    def show(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            cursor.execute("Select * From employee")
            rows = cursor.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # -----------Put Data in Fields------------------

    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content['values']

        self.var_emp_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_dob.set(row[4]),
        self.var_contact.set(row[5]),
        self.var_doj.set(row[6]),
        self.var_usr_type.set(row[7]),
        self.txt_address.delete("1.0", END),
        self.txt_address.insert(END, row[8]),
        self.var_salary.set(row[9])

    # -----------Update Button--------------

    def update(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror(
                    "Error", "Employee's ID is Required.", parent=self.root)
            else:
                cursor.execute(
                    "Select * from employee where emp_id=?", (self.var_emp_id.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Employee's ID!", parent=self.root)
                else:
                    cursor.execute(
                        "Update employee set name=? ,email=? ,gender=? ,dob=? ,contact=? ,doj=? ,usr_type=? ,address=? ,salary=? where emp_id=?", (
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_dob.get(),
                            self.var_contact.get(),
                            self.var_doj.get(),
                            self.var_usr_type.get(),
                            self.txt_address.get("1.0", END),
                            self.var_salary.get(),
                            self.var_emp_id.get()
                        ))

                    password = str(self.var_pass.get())
                    password_bytes = bytes(password, 'utf-8')
                    salt = bcrypt.gensalt()
                    hash = bcrypt.hashpw(password_bytes, salt)

                    cursor.execute("Update Login set pass=?, auth=? where name=?", (
                        hash,
                        self.var_usr_type.get(),
                        self.var_name.get()

                    ))
                    conn.commit()
                    messagebox.showinfo(
                        "Success", "Employee Updated Successfully!", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # -------Delete Button------------
    def delete(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror(
                    "Error", "Employee's ID is Required.", parent=self.root)
            elif self.var_name.get() == "":
                messagebox.showerror(
                    "Error", "Employee's Name is Required.", parent=self.root)
            else:
                cursor.execute(
                    "Select * from employee where emp_id=?", (self.var_emp_id.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Employee's ID!", parent=self.root)
                else:
                    cursor.execute(
                        "Select auth from Login where name=?", (self.var_name.get(),))
                    column = cursor.fetchone()[0]

                    if column == 'Admin':
                        messagebox.showerror(
                            "Error", "Cannot delete Admin.", parent=self.root)
                        self.clear()
                    else:
                        op = messagebox.askyesno(
                            "Confirm", "Do you want to delete the employee?", parent=self.root)
                        if op == True:
                            cursor.execute("delete from employee where emp_id=?",
                                           (self.var_emp_id.get(),))
                            conn.commit()
                            messagebox.showinfo(
                                "Delete", "Employee Deleted Successfully!", parent=self.root)
                            self.show()
                            self.clear()

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    # -------Clear Button--------------
    def clear(self):
        self.var_emp_id.set(""),
        self.var_name.set(""),
        self.var_email.set(""),
        self.var_gender.set("Select"),
        self.var_dob.set(""),
        self.var_pass.set(""),
        self.var_contact.set(""),
        self.var_doj.set(""),
        self.var_usr_type.set("Admin"),
        self.txt_address.delete("1.0", END),
        self.var_salary.set("")
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
                cursor.execute("Select * From employee where " +
                               self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cursor.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(
                        *self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No Record Found!", parent=self.root)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()
