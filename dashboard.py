from tkinter import *
from tkinter import messagebox
import time
import sqlite3
import os
from PIL import Image, ImageTk
import bcrypt
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from create_db import Create_db


class DBClass:
    def __init__(self, root):
        self.root = root
        self.root.title('Create Database')
        self.root.geometry('300x300+500+250')
        self.root.iconbitmap("images/main.ico")
        self.root.config(bg="#fff")
        self.root.resizable(False, False)

        lbl_Database = Label(self.root, text='Create Database',
                             font=('goudy old style', 20, 'bold'), bg='#b86502').pack(side=TOP, fill=X)

        self.btn_db = Button(self.root, text='Click me\n\nTo Create\n\nDatabase', command=Create_db,
                             font=('goudy old style', 15, 'bold'), bd=3, relief=RIDGE, cursor='hand2').place(x=75, y=90, width=150, height=150)


class LoginClass:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('925x500+300+200')
        self.root.iconbitmap("images/main.ico")
        self.root.config(bg="#fff")
        self.root.resizable(False, False)
        self.var_auth = StringVar()

        # ---------Sign in Function-----------

        def dashboard():
            new_win = Toplevel(root)
            new_obj = IMS(new_win, self.var_auth)

        def signin():
            name = StringVar()
            pass_ = StringVar()
            conn = sqlite3.connect(r'IMS.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, pass, auth FROM Login where name=?", (user.get(),))
            for row in cursor.fetchall():
                name, pass_, auth = row

            self.var_auth = auth
            stored_password = pass_

            password = bytes(str(code.get()), 'utf-8')

            if bcrypt.checkpw(password, stored_password) and self.var_auth == 'Admin':
                dashboard()
                root.withdraw()
            elif bcrypt.checkpw(password, stored_password) and self.var_auth == 'Employee':
                self.billing()
            else:
                messagebox.showerror("Invalid", "Invalid Username or Password")

        # ---------Image Here----------

        self.img = PhotoImage(file="images/login.png")
        lbl_img = Label(root, image=self.img, bg='white').place(x=50, y=50)

        # ------------Frame-------------

        self.frame = Frame(root, width=350, height=350, bg='white')
        self.frame.place(x=480, y=70)

        heading = Label(self.frame, text='Sign in', fg='#57a1f8', bg='white',
                        font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        # ------------User Functions------------

        def on_enter(e):
            user.delete(0, 'end')

        def on_leave(e):
            name = user.get()
            if name == '':
                user.insert(0, 'Username')

        # ------Entry-----------
        user = Entry(self.frame, width=25, fg='black', border=0,
                     bg='white', font=('Microsoft YaHei UI Light', 11))
        user.place(x=30, y=80)
        user.insert(0, 'Username')
        user.bind('<FocusIn>', on_enter)
        user.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=107)

        # ------------Password Functions------------

        def on_enter(e):
            code.delete(0, 'end')

        def on_leave(e):
            cname = code.get()
            if cname == '':
                code.insert(0, 'Password')

        # -----------------------------------
        code = Entry(self.frame, width=25, fg='black', border=0, show='*',
                     bg='white', font=('Microsoft YaHei UI Light', 11))
        code.place(x=30, y=150)
        code.insert(0, 'Password')
        code.bind('<FocusIn>', on_enter)
        code.bind('<FocusOut>', on_leave)

        frame = Frame(self.frame, width=295, height=2,
                      bg='black').place(x=25, y=177)

        def Signup():
            new_win = Toplevel(root)
            new_obj = SignupClass(new_win)
            root.withdraw()

        # ----------------------------------
        Button(self.frame, width=39, pady=7, text='Sign in',
               bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)

        label = Label(self.frame, text="Don't have an account?", fg='black',
                      bg='white', font=('Microsoft YaHei UI Light', 9))
        label.place(x=75, y=270)

        sign_up = Button(self.frame, width=6, text='Sign up', command=Signup, border=0,
                         bg='white', cursor='hand2', fg='#57a1f8')
        sign_up.place(x=215, y=270)

    def billing(self):
        self.root.destroy()
        os.system("python billing.py")

# ===========================================================================================================================


class IMS(LoginClass):
    def __init__(self, root, auth):
        self.auth = auth
        self.root = root
        self.root.geometry("1280x950+0+0")
        self.root.iconbitmap("images/main.ico")
        self.root.title(
            "Inventory Management System  |  Developed by Hassan Zohaib")
        self.root.config(bg="white")

        # ------Title-----
        self.icon_title = PhotoImage(file="images/logo.png")
        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT,
                      font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        # ----Button_Logout----
        btn_logout = Button(self.root, text="Logout", command=self.Login,
                            font=("times new roman", 15, "bold"), bg="yellow", cursor="hand2").place(x=1100, y=10, height=50, width=150)

        # ----clock-----
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("times new roman", 10, "bold"), bg="#4d636d", fg="white",)
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ----Left Menu-----
        self.MenuLogo = Image.open("Images/menu_im.png")
        self.MenuLogo = self.MenuLogo.resize(
            (200, 200,), Image.Resampling.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        Left_Menu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Left_Menu.place(x=0, y=102, width=200, height=620)

        lbl_menulogo = Label(Left_Menu, image=self.MenuLogo)
        lbl_menulogo.pack(side=TOP, fill=X)

        # ------Left Menu Label------
        btn_menu = Label(Left_Menu, text="Menu",
                         font=("times new roman", 20), bg="#009688", fg="white").pack(side=TOP, fill=X)
        self.btn_img = PhotoImage(file="images/btn_logo.png")

        # -------Menu Button------
        menu_employee = Button(Left_Menu, text="Employee", command=self.employee, image=self.btn_img, compound=LEFT, padx=5, anchor="w",
                               font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        menu_DB = Button(Left_Menu, text="Create DB", command=self.database, image=self.btn_img, compound=LEFT, padx=5, anchor="w",
                         font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        menu_Supplier = Button(Left_Menu, text="Supplier", command=self.supplier, image=self.btn_img, compound=LEFT, padx=5, anchor="w",
                               font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        menu_category = Button(Left_Menu, text="Categories", command=self.category, image=self.btn_img, compound=LEFT, padx=5, anchor="w",
                               font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        menu_product = Button(Left_Menu, text="Products", command=self.product, image=self.btn_img, compound=LEFT, padx=5, anchor="w",
                              font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        menu_sales = Button(Left_Menu, text="Sales", command=self.sales, image=self.btn_img, compound=LEFT, padx=5, anchor="w",
                            font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        menu_exit = Button(Left_Menu, text="Exit", command=quit, image=self.btn_img, compound=LEFT, padx=5, anchor="w",
                           font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)

        # ----Content------
        self.lbl_employee = Label(
            self.root, text="Total Employee\n [ 0]", bd=2, relief=RIDGE, bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=250, y=150, height=150, width=300)

        self.lbl_supplier = Label(
            self.root, text="Total Suppliers\n [ 0]", bd=2, relief=RIDGE, bg="#ff5722", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=575, y=150, height=150, width=300)

        self.lbl_category = Label(
            self.root, text="Total Category\n [ 0]", bd=2, relief=RIDGE, bg="#e42f53", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=900, y=150, height=150, width=300)

        self.lbl_product = Label(
            self.root, text="Total Products\n [ 0]", bd=2, relief=RIDGE, bg="#b87f56", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=250, y=350, height=150, width=300)

        self.lbl_sale = Label(
            self.root, text="Total Sales\n [ 0]", bd=2, relief=RIDGE, bg="#8d71dc", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_sale.place(x=575, y=350, height=150, width=300)

        # ----Footer-----
        lbl_footer = Label(self.root, text="Inventory Management System | Developed by Hassan Zohaib\n For any Technical Issue Contact hassan.zohaib.184@gmail.com",
                           font=("times new roman", 12, "bold"), bg="#4d636d", fg="white",).pack(side=BOTTOM, fill=X)

        self.update_date_time()
        self.update_content()
# --------------------------------------------------------------------------------------------------------------------------------------

    def Login(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = LoginClass(self.new_win)
        self.root.withdraw()

    def employee(self):
        if self.auth == 'Admin':
            self.new_win = Toplevel(self.root)
            self.new_obj = employeeClass(self.new_win)
        else:
            messagebox.showwarning("Warning!", "Access Denied!")

    def database(self):
        if self.auth == 'Admin':
            self.new_win = Toplevel(self.root)
            self.new_obj = DBClass(self.new_win)
        else:
            messagebox.showwarning("Warning!", "Access Denied!")

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(time_)}\t\t Time: {str(date_)}",
                              font=("times new roman", 10, "bold"), bg="#4d636d", fg="white",)
        self.lbl_clock.after(200, self.update_date_time)

    def update_content(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            cursor.execute("select * from product")
            product = cursor.fetchall()
            self.lbl_product.config(
                text=f"Total Products\n [ {str(len(product))} ]")

            cursor.execute("select * from employee")
            employee = cursor.fetchall()
            self.lbl_employee.config(
                text=f"Total Employees\n [ {str(len(employee))} ]")

            cursor.execute("select * from supplier")
            supplier = cursor.fetchall()
            self.lbl_supplier.config(
                text=f"Total Suppliers\n [ {str(len(supplier))} ]")

            cursor.execute("select * from category")
            category = cursor.fetchall()
            self.lbl_category.config(
                text=f"Total Category\n [ {str(len(category))} ]")

            self.lbl_sale.config(
                text=f"Total Sales\n [{str(len(os.listdir('bill')))}]")

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)


# =======================================================================================


class SignupClass(LoginClass):
    def __init__(self, root):
        super().__init__(root)
        self.root.title('Sign Up')
        self.root.geometry('925x500+300+200')
        self.root.iconbitmap("images/main.ico")
        self.root.config(bg="#fff")
        self.root.resizable(False, False)

        # -------Sign up Function----------

        def sign_up():
            def login():
                new_win = Toplevel(root)
                new_obj = LoginClass(new_win)
                root.withdraw()
            username = user.get()
            password = code.get()
            confirmpassword = confirmcode.get()

            if password == confirmpassword:
                root.withdraw()
                login()

        # ---------Image Here----------

        self.img = PhotoImage(file='images/Signup.png')
        lbl_img = Label(self.root, image=self.img,
                        bg='white').place(x=50, y=50)

        # ------------Frame-------------

        self.frame = Frame(root, width=350, height=350, bg='white')
        self.frame.place(x=480, y=70)

        heading = Label(self.frame, text='Sign Up', fg='#57a1f8', bg='white',
                        font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        # ------------User Functions------------

        def on_enter(e):
            user.delete(0, 'end')

        def on_leave(e):
            name = user.get()
            if name == '':
                user.insert(0, 'Username')

        # ------Entry-----------
        user = Entry(self.frame, width=25, fg='black', border=0,
                     bg='white', font=('Microsoft YaHei UI Light', 11))
        user.place(x=30, y=70)
        user.insert(0, 'Username')
        user.bind('<FocusIn>', on_enter)
        user.bind('<FocusOut>', on_leave)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=97)

        # ------------Password Functions------------

        def on_enter(e):
            code.delete(0, 'end')

        def on_leave(e):
            cname = code.get()
            if cname == '':
                code.insert(0, 'Password')

        # -----------------------------------
        code = Entry(self.frame, width=25, fg='black', border=0,
                     bg='white', font=('Microsoft YaHei UI Light', 11))
        code.place(x=30, y=140)
        code.insert(0, 'Password')
        code.bind('<FocusIn>', on_enter)
        code.bind('<FocusOut>', on_leave)

        frame = Frame(self.frame, width=295, height=2,
                      bg='black').place(x=25, y=167)

        # -------Confirm Password Functions------------

        def on_enter(e):
            confirmcode.delete(0, 'end')

        def on_leave(e):
            ccname = confirmcode.get()
            if ccname == '':
                confirmcode.insert(0, 'Confirm Password')

        # -----------------------------------
        confirmcode = Entry(self.frame, width=25, fg='black', border=0,
                            bg='white', font=('Microsoft YaHei UI Light', 11))
        confirmcode.place(x=30, y=210)
        confirmcode.insert(0, 'Confirm Password')
        confirmcode.bind('<FocusIn>', on_enter)
        confirmcode.bind('<FocusOut>', on_leave)

        frame = Frame(self.frame, width=295, height=2,
                      bg='black').place(x=25, y=237)

        # ----------------------------------
        Button(self.frame, width=39, pady=7, text='Sign up',
               bg='#57a1f8', fg='white', border=0, command=sign_up).place(x=35, y=270)

        label = Label(self.frame, text="I have an account?", fg='black',
                      bg='white', font=('Microsoft YaHei UI Light', 9))
        label.place(x=90, y=320)

        self.sign_up = Button(self.frame, width=6, text='Sign in', border=0, command=self.login,
                              bg='white', cursor='hand2', fg='#57a1f8').place(x=200, y=320)

    def login(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = LoginClass(self.new_win)
        self.root.withdraw()


if __name__ == "__main__":
    root = Tk()
    obj = LoginClass(root)
    root.mainloop()
