from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import time
import os
import tempfile


class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x950+0+0")
        self.root.iconbitmap("images/main.ico")
        self.root.title(
            "Inventory Management System  |  Developed by Hassan Zohaib")
        self.root.config(bg="white")

        self.cart_list = []
        self.chk_print = 0
        # ------Title-----
        self.icon_title = PhotoImage(file="images/logo.png")
        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT,
                      font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        # ----Button_Logout----
        btn_logout = Button(self.root, text="Logout", command=self.logout,
                            font=("times new roman", 20, "bold"), bg="yellow", cursor="hand2").place(x=1100, y=10, height=50, width=150)

        # ----clock-----
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("times new roman", 10, "bold"), bg="#4d636d", fg="white",)
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ---------Frame 1----------
        self.var_search = StringVar()
        self.var_barcode = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_status = StringVar()

        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg='white')
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        pTitle = Label(ProductFrame1, text='All Products', font=(
            'goudy old style', 20, 'bold'), bg='#262626', fg='white').pack(side=TOP, fill=X)

        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg='white')
        ProductFrame2.place(x=4, y=42, width=394, height=90)

        lbl_search = Label(ProductFrame2, text="Search product | By name", font=(
            'times new roman', 15, 'bold'), bg="white", fg="green").place(x=2, y=5)
        lbl_name = Label(ProductFrame2, text='Product name', font=(
            'times new roman', 15, 'bold'), bg="white").place(x=2, y=45)

        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=(
            'times new roman', 15), bg="lightyellow").place(x=125, y=47, width=150, height=22)

        btn_search = Button(ProductFrame2, text="Search", command=self.search, font=(
            "goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=280, y=45, width=100, height=25)

        btn_showall = Button(ProductFrame2, text="Show All", command=self.show, font=(
            "goudy old style", 15), bg="#083531", fg="white", cursor="hand2").place(x=280, y=10, width=100, height=25)

        # ------Product Details---------

        ProductFrame3 = Frame(ProductFrame1, bd=4, relief=RIDGE, bg='white')
        ProductFrame3.place(x=2, y=140, width=398, height=380)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(ProductFrame3, columns=(
            "barcode", "name", "price", "quantity", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("barcode", text="Code")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("quantity", text="Quantity")
        self.ProductTable.heading("status", text="Status")
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("barcode", width=20)
        self.ProductTable.column("name",  width=40)
        self.ProductTable.column("price",  width=30)
        self.ProductTable.column("quantity", width=30)
        self.ProductTable.column("status", width=30)
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        lbl_note = Label(ProductFrame1, text="Note: 'Enter 0 quantity to remove item from cart' ", bg='white',
                         fg='red', font=("goudy old style", 12, 'bold'), anchor='w').pack(side=BOTTOM, fill=X)

        # -------------Customer Frame---------------------------
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg='white')
        CustomerFrame.place(x=420, y=110, width=380, height=140)

        cTitle = Label(CustomerFrame, text='Customer Details', font=(
            'goudy old style', 15, 'bold'), bg='lightgray').pack(side=TOP, fill=X)

        lbl_cname = Label(CustomerFrame, text='Name:', font=(
            'times new roman', 15), bg="white").place(x=5, y=35)

        txt_cname = Entry(CustomerFrame, textvariable=self.var_cname, font=(
            'times new roman', 15), bg="lightyellow").place(x=80, y=35, width=180)

        lbl_ccontact = Label(CustomerFrame, text='Contact:', font=(
            'times new roman', 15), bg="white").place(x=5, y=80)

        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=(
            'times new roman', 15), bg="lightyellow").place(x=80, y=80, width=180)

        # --------------Cal frame-------------------------
        self.var_cal_input = StringVar()
        CalFrame = Frame(self.root, bd=8, relief=RIDGE, bg='white')
        CalFrame.place(x=420, y=250, width=380, height=410)

        text_cal_input = Entry(CalFrame, textvariable=self.var_cal_input, font=(
            'arial', 15, 'bold'), width=21, bd=10, relief=GROOVE, state='readonly', justify=RIGHT)
        text_cal_input.grid(row=0, columnspan=4)

        btn_7 = Button(CalFrame, text='7', command=lambda: self.get_input(7), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=1, column=0)
        btn_8 = Button(CalFrame, text='8', command=lambda: self.get_input(8), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=1, column=1)
        btn_9 = Button(CalFrame, text='9', command=lambda: self.get_input(9), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=1, column=2)
        btn_sum = Button(CalFrame, text='+', command=lambda: self.get_input('+'), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=1, column=3)

        btn_4 = Button(CalFrame, text='4', command=lambda: self.get_input(4), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=2, column=0)
        btn_5 = Button(CalFrame, text='5', command=lambda: self.get_input(5), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=2, column=1)
        btn_6 = Button(CalFrame, text='6', command=lambda: self.get_input(6), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=2, column=2)
        btn_sub = Button(CalFrame, text='-', command=lambda: self.get_input('-'), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=2, column=3)

        btn_1 = Button(CalFrame, text='1', command=lambda: self.get_input(1), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=3, column=0)
        btn_2 = Button(CalFrame, text='2', command=lambda: self.get_input(2), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=3, column=1)
        btn_3 = Button(CalFrame, text='3', command=lambda: self.get_input(3), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=3, column=2)
        btn_mul = Button(CalFrame, text='*', command=lambda: self.get_input('*'), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=3, column=3)

        btn_0 = Button(CalFrame, text='0', command=lambda: self.get_input(0), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=4, column=0)
        btn_c = Button(CalFrame, text='c', command=self.clear_cal, font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=4, column=1)
        btn_eq = Button(CalFrame, text='=', command=self.perform_cal, font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=4, column=2)
        btn_div = Button(CalFrame, text='/', command=lambda: self.get_input('/'), font=(
            'arial', 15, 'bold'), bd=5, width=4, pady=20, cursor='hand2').grid(row=4, column=3)

        # --------------Cart Frame------------------------
        CartFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        CartFrame.place(x=6, y=670, width=410, height=230)
        self.lbl_cart = Label(CartFrame, text=' Cart\t\t  Total Product: [0]', font=(
            'goudy old style', 15, 'bold'), bg='lightgray', anchor='w')
        self.lbl_cart.pack(side=TOP, fill=X)

        scrolly = Scrollbar(CartFrame, orient=VERTICAL)
        scrollx = Scrollbar(CartFrame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(CartFrame, columns=(
            "barcode", "name", "price", "quantity"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("barcode", text="Code")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("quantity", text="Quantity")
        self.CartTable["show"] = "headings"

        self.CartTable.column("barcode", width=50)
        self.CartTable.column("name",  width=100)
        self.CartTable.column("price",  width=100)
        self.CartTable.column("quantity", width=100)
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_Cartdata)

        # ----------ADD Cart Button Frame-----------------------

        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_instock = StringVar()

        AddCartFrame = Frame(self.root, bd=4, relief=RIDGE, bg='white')
        AddCartFrame.place(x=420, y=670, width=380, height=230)

        lbl_pname = Label(AddCartFrame, text='Name:', font=(
            'times new roman', 15), bg="white").place(x=5, y=20)

        txt_pname = Entry(AddCartFrame, textvariable=self.var_pname, state='readonly', font=(
            'times new roman', 15), bg="lightyellow").place(x=85, y=20, width=180)

        lbl_pPrice = Label(AddCartFrame, text='Price:', font=(
            'times new roman', 15), bg="white").place(x=5, y=65)

        txt_Price = Entry(AddCartFrame, textvariable=self.var_price, state='readonly', font=(
            'times new roman', 15), bg="lightyellow").place(x=85, y=65, width=180)

        lbl_pquantity = Label(AddCartFrame, text='Quantity:', font=(
            'times new roman', 15), bg="white").place(x=5, y=110)

        txt_quantity = Entry(AddCartFrame, textvariable=self.var_quantity, font=(
            'times new roman', 15), bg="lightyellow").place(x=85, y=110, width=180)

        self.lbl_stock = Label(AddCartFrame, text='In Stock', font=(
            'times new roman', 15), bg="white")
        self.lbl_stock.place(x=280, y=20)

        btn_clear = Button(AddCartFrame, text="Clear", font=(
            "goudy old style", 15), bg="lightgray", cursor="hand2").place(x=25, y=170, width=100, height=25)

        btn_add = Button(AddCartFrame, text="Add | Update Cart", command=self.add_cart, font=(
            "goudy old style", 15), bg="green", fg="white", cursor="hand2").place(x=135, y=170, width=200, height=25)

        # ---------------Bill Area-----------------------------
        BillFrame = Frame(self.root, bd=4, relief=RIDGE, bg='white')
        BillFrame.place(x=805, y=110, width=450, height=550)

        bTitle = Label(BillFrame, text='Customer Billing Area', font=(
            'goudy old style', 20, 'bold'), bg='#cb2b2b', fg='white').pack(side=TOP, fill=X)
        scrolly = Scrollbar(BillFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(BillFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)

        scrolly.config(command=self.txt_bill_area.yview)

        BillBtnFrame = Frame(self.root, bd=4, relief=RIDGE, bg='white')
        BillBtnFrame.place(x=805, y=670, width=450, height=230)

        self.lbl_bamount = Label(BillBtnFrame, text='Bill Amount\n0', bd=2, relief=RIDGE, bg="#33bbf9",
                                 fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_bamount.place(x=5, y=10, height=110, width=160)
        self.lbl_discount = Label(BillBtnFrame, text='Discount\n[5%]', bd=2, relief=RIDGE, bg="#ff5722",
                                  fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_discount.place(x=170, y=10, height=110, width=130)
        self.lbl_netpay = Label(BillBtnFrame, text=' Net pay \n[0]]', bd=2, relief=RIDGE, bg="#e42f53",
                                fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_netpay.place(x=310, y=10, height=110, width=130)

        btn_print = Button(BillBtnFrame, text="Print\nBill", command=self.print_bill, font=(
            "goudy old style", 15), bg="lightgray", cursor="hand2").place(x=15, y=130, width=100, height=90)

        btn_clear = Button(BillBtnFrame, text="Clear All", command=self.clear_all, font=(
            "goudy old style", 15), bg="green", fg="white", cursor="hand2").place(x=120, y=130, width=100, height=90)

        btn_Genbill = Button(BillBtnFrame, text="Generate\n Save Bill", command=self.generate_bill, font=(
            "goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=230, y=130, width=100, height=90)

        btn_exit = Button(BillBtnFrame, text="Exit", command=quit, font=(
            "goudy old style", 15), bg="red", fg="white", cursor="hand2").place(x=340, y=130, width=100, height=90)

        # ----Footer-----
        lbl_footer = Label(self.root, text="Inventory Management System | Developed by Hassan Zohaib\n For any Technical Issue Contact hassan.zohaib.184@gmail.com",
                           font=("times new roman", 12, "bold"), bg="#4d636d", fg="white",).pack(side=BOTTOM, fill=X)
        self.show()
        self.update_date_time()


# =========================================================Functions=======================================================================
        # ----------Show Data in Tree View ---------------------

    def show(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                "Select barcode, name, price, quantity, status from product where status = 'Active'")
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
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_quantity.set(row[3])
        self.var_status.set(row[4])
        self.lbl_stock.config(text=f"In Stock\n[{str(row[3])}]")
        self.var_instock.set(row[3])
        self.var_quantity.set('1')

    def get_Cartdata(self, ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        row = content['values']

        self.var_barcode.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_quantity.set(row[3])
        self.lbl_stock.config(text=f"In Stock\n[{str(row[4])}]")
        self.var_instock.set(row[4])

    # --------------calculator functions--------------------

    def get_input(self, num):
        xnum = self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    # ----------search functions--------------
    def search(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()

        try:
            if self.var_search.get() == "":
                messagebox.showerror(
                    "Error", "Select area should not be empty!", parent=self.root)
            elif self.var_search.get() == "":
                messagebox.showerror("Error", "Product name is required")
            else:
                cursor.execute(
                    "Select barcode, name, price, quantity, status from product WHERE name LIKE '%" + self.var_search.get() + "%' and status='Active'")
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

    def add_cart(self):
        if self.var_quantity.get() == "":
            messagebox.showerror(
                "Error", "Quantity is Required!", parent=self.root)
        elif self.var_barcode.get() == "":
            messagebox.showerror(
                "Error", "Please select product from the list.", parent=self.root)
        elif int(self.var_quantity.get()) > int(self.var_instock.get()):
            messagebox.showerror(
                "Error", "Invalid quantity.", parent=self.root)
        elif self.var_status.get() == 'Inactive':
            messagebox.showerror(
                "Error", "Product must be Active.", parent=self.root)
        else:
            price_cal = self.var_price.get()

            cart_data = [self.var_barcode.get(), self.var_pname.get(),
                         price_cal, self.var_quantity.get(), self.var_instock.get()]

            present = 'no'
        index_ = 0
        for row in self.cart_list:
            if self.var_barcode.get() == row[0]:
                present = 'yes'
                break
            index_ += 1

        if present == 'yes':
            op = messagebox.askyesno(
                "Confirm", "Product already present\nDo you want to update?", parent=self.root)
            if op == True:
                if self.var_quantity.get() == "0":
                    self.cart_list.pop(index_)
                else:
                    self.cart_list[index_][3] = self.var_quantity.get()

        else:
            self.cart_list.append(cart_data)

        self.show_cart()
        self.bill_update()

    def bill_update(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0

        for row in self.cart_list:
            self.bill_amnt = self.bill_amnt+(float(row[2])*int(row[3]))
        self.net_pay = self.bill_amnt-((self.bill_amnt*5)/100)
        self.discount = (self.bill_amnt*5)/100
        self.lbl_bamount.config(text=f'Bill Amount\n[{str(self.bill_amnt)}]')
        self.lbl_netpay.config(text=f'Net Pay\n[{str(self.net_pay)}]')
        self.lbl_cart.config(
            text=f' Cart\t\t  Total Product: [{str(len(self.cart_list))}]')

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get == '' or self.var_contact.get == '':
            messagebox.showerror(
                "Error", "Customer Details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror(
                "Error", "Please Add Product to the cart.", parent=self.root)
        else:
            # -----------Bill top---------------
            self.bill_top()

            # ----------Bill Middle-------------
            self.bill_middle()

            # ----------Bill Bottom-------------
            self.bill_bottom()

            fp = open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo(
                "Saved", "Bill has been Generated/Saved.", parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + \
            int(time.strftime("%d%m%y"))
        bill_top_temp = f'''
 \t\tXYZ-Inventory
 Phone No. 030xxxxxx,\tSargodha-10040
 {str("="*44)}
 Customer Name: {self.var_cname.get()}
 Ph no. :{self.var_contact.get()}
 Bill no. {str(self.invoice)} \t Date:{str(time.strftime("%d/%m/%Y"))}
 {str("="*44)}
 Product Name\t\tQTY\t\tPrice
 {str("="*44)}'''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_middle(self):
        conn = sqlite3.connect(r'IMS.db')
        cursor = conn.cursor()
        try:
            for row in self.cart_list:
                name = row[1]
                qty = int(row[4])-int(row[3])

                if int(row[3]) == int(row[4]):
                    status = 'Inactive'
                if int(row[3]) != int(row[4]):
                    status = 'Active'

                price = float(row[2])*int(row[3])
                price = str(price)
                self.txt_bill_area.insert(
                    END, "\n "+name+"\t\t"+row[3]+" \t\tRs."+price)

                cursor.execute(
                    'Update product set quantity=?, status=?  where name=?', (
                        qty,
                        status,
                        name
                    ))
                conn.commit()
            conn.close()
            self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error Due to : {str(ex)}", parent=self.root)

    def bill_bottom(self):
        bill_bottom_temp = f'''
 {str("="*44)}
 Bill Ammount\t\t\tRs.{self.bill_amnt}
 Discount\t\t\tRs.{self.discount}
 Net Pay\t\t\tRs.{self.net_pay}
 {str("="*44)}\n'''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def clear_cart(self):
        self.var_barcode.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_quantity.set("")
        self.lbl_stock.config(text="In Stock\n[0]")
        self.var_instock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.txt_bill_area.delete('1.0', END)
        self.var_cal_input.set("")
        self.var_cname.set("")
        self.var_contact.set("")
        self.lbl_bamount.config(text='Bill Amount\n[0]')
        self.lbl_netpay.config(text='Net Pay\n[0]')
        self.lbl_cart.config(
            text=' Cart\t\t  Total Product: [0]')
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(time_)}\t\t Time: {str(date_)}",
                              font=("times new roman", 10, "bold"), bg="#4d636d", fg="white",)
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo(
                "Print", "Please wait while printing", parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showerror(
                "Print", "Please Generate Bill before Printing Receipt.", parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
