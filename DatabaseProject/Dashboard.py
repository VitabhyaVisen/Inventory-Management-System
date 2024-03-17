from tkinter import *
from PIL import Image, ImageTk
from Employee import employeeClass
from Supplier import supplierClass
from Category import categoryClass
from Products import productClass
from Sales import salesClass
from tkinter import messagebox
import sqlite3
import os
import time

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Student")
        self.root.config(bg="white")

        # ------TITLE-------
        self.icon_title = PhotoImage(file="images/images/logo1.png")
        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT, font=("Helvetica", 40, "bold"), bg="teal", fg="#FFFDD0", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        # ------LOG-OUT BUTTON-----
        btn_logout = Button(self.root, text="Logout", command=self.logout, font=("Verdana", 15, "bold"), bg="light grey", fg="#36454F", cursor="hand2").place(x=1100, y=10, height=50, width=150)

        #-------CLOCK-----------
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="light grey", fg="#36454F")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #------LEFT MENU-------
        self.MenuLogo = Image.open("images/images/menu_im.png")
        self.MenuLogo = self.MenuLogo.resize((200, 200),  Image.Resampling.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)
        
        self.icon_side = PhotoImage(file="images/images/side.png")
        lbl_Menu = Label(LeftMenu, text="Menu", font=("Verdana", 20), bg="teal", fg="#FFFDD0").pack(side=TOP, fill=X)
        btn_employee = Button(LeftMenu, text="Employee", command= self.employee, image= self.icon_side, compound=LEFT, padx= 5, anchor="w" ,font=("Verdana", 15, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_supplier = Button(LeftMenu, text="Supplier", command= self.supplier, image= self.icon_side, compound=LEFT, padx= 5, anchor="w" ,font=("Verdana", 15, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_category = Button(LeftMenu, text="Category", command=self.category, image= self.icon_side, compound=LEFT, padx= 5, anchor="w" ,font=("Verdana", 15, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_product = Button(LeftMenu, text="Products", command=self.product, image= self.icon_side, compound=LEFT, padx= 5, anchor="w" ,font=("Verdana", 15, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_sales = Button(LeftMenu, text="Sales", command=self.sales, image= self.icon_side, compound=LEFT, padx= 5, anchor="w" ,font=("Verdana", 15, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_exit = Button(LeftMenu, text="Exit", image= self.icon_side, compound=LEFT, padx= 5, anchor="w" ,font=("Verdana", 15, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)

        # -------CONTENT------
        self.lbl_employee = Label(self.root, text= "Total Employee\n[0]", bd=5, relief=RIDGE, bg="#0F52BA", fg="white", font= ("Palatino", 20, "bold"))
        self.lbl_employee.place(x=300,y=120, height=150, width=265)

        self.lbl_supplier = Label(self.root, text= "Total Suppliers\n[0]", bd=5, relief=RIDGE, bg="#FF4500", fg="white", font= ("Palatino", 20, "bold"))
        self.lbl_supplier.place(x=650,y=120, height=150, width=265)

        self.lbl_category = Label(self.root, text= "Total Categories\n[0]", bd=5, relief=RIDGE, bg="#008000", fg="white", font= ("Palatino", 20, "bold"))
        self.lbl_category.place(x=1000,y=120, height=150, width=265)

        self.lbl_Products = Label(self.root, text= "Total Products\n[0]", bd=5, relief=RIDGE, bg="#9966CC", fg="white", font= ("Palatino", 20, "bold"))
        self.lbl_Products.place(x=300,y=300, height=150, width=265)

        self.lbl_Sales = Label(self.root, text= "Total Sales\n[0]", bd=5, relief=RIDGE, bg="#DAA520", fg="white", font= ("Palatino", 20, "bold"))
        self.lbl_Sales.place(x=650,y=300, height=150, width=265)

         #-------FOOTER-----------
        lbl_footer = Label(self.root, text="IMS-Inventory Management System | Developed by Students\nFor any Technical issue Contact: 987xxxxx01", font=("times new roman", 12), bg="light grey", fg="#36454F").pack(side=BOTTOM, fill=X)

        self.update_CONTENT()
# ------------------------------------------------------------------------------------------------------------
        
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)
    
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

    def update_CONTENT(self):
        con = sqlite3.connect(database='DatabaseProject.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_Products.config(text= f"Total Products\n[{str(len(product))}]")

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text= f"Total Supplier\n[{str(len(supplier))}]")

            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text= f"Total Employee\n[{str(len(employee))}]")
            
            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text= f"Total Categories\n[{str(len(category))}]")

            self.lbl_Sales.config(text= f'Total Sales\n[{str(len(os.listdir('bill')))}]')
            
            TIME_ = time.strftime("%I:%M:%S")
            DATE_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config( text=f"Welcome to Inventory Management System\t\t Date: {str(DATE_)}\t\t Time: {str(TIME_)}")
            self.lbl_clock.after(200, self.update_CONTENT)

        except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)

    def logout(self):
        self.root.destroy()
        os.system("python Login.py")

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
