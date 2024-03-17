from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile


class billingClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Student")
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print = 0

        # ------TITLE-------
        self.icon_title = PhotoImage(file="images/images/logo1.png")
        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT, font=("Helvetica", 40, "bold"), bg="teal", fg="#FFFDD0", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        # ------LOG-OUT BUTTON-----
        btn_logout = Button(self.root, text="Logout", command=self.logout, font=("Verdana", 15, "bold"), bg="light grey", fg="#36454F", cursor="hand2").place(x=1100, y=10, height=50, width=150)

        #-------CLOCK-----------
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="light grey", fg="#36454F")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #-----------PRODUCT FRAME1---------------

        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=398, height=530)

        pTitle = Label(ProductFrame1, text= "All Products", font= ("goudy old style", 20, "bold"), bg= "#4682B4", fg= "white").pack(side=TOP, fill=X)

        #-----------PRODUCT FRAME2----------------
        self.var_search = StringVar()

        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=385, height=90)

        lbl_search = Label(ProductFrame2, text= "Search Product | By Name", font= ("times new roman", 15, "bold"), bg= "white", fg= "green").place(x=2, y=5)

        lbl_name = Label(ProductFrame2, text= "Product Name:",font= ("times new roman", 15, "bold"), bg= "white").place(x=2, y=45)

        lbl_SEARCH_name = Entry(ProductFrame2, textvariable= self.var_search, font= ("times new roman", 15), bg= "lightyellow" ).place(x=135, y=47, width=140, height=22)

        btn_search = Button(ProductFrame2, text="Search", command=self.search, font= ("Goudy old style", 15, "bold"), bg= "teal", fg= "#FFFDD0", cursor= "hand2").place(x=282, y=45, width=90, height=25)

        btn_showall = Button(ProductFrame2, text="Show All", command=self.show, font= ("Goudy old style", 15, "bold"), bg= "#4682B4", fg= "#FFFDD0", cursor= "hand2").place(x=282, y=10, width=90, height=25)

        #------------PRODUCT FRAME3---------

        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=385, height=360)

        scrolly = Scrollbar(ProductFrame3, orient= VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient= HORIZONTAL)

        self.Product_Table = ttk.Treeview(ProductFrame3, columns= ("pid", "name", "price", "qty", "status"), yscrollcommand= scrolly.set, xscrollcommand= scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.Product_Table.xview)
        scrolly.config(command=self.Product_Table.yview)

        self.Product_Table.heading("pid", text= "P Id.")
        self.Product_Table.heading("name", text= "Name")
        self.Product_Table.heading("price", text= "Price")
        self.Product_Table.heading("qty", text= "Quantity")
        self.Product_Table.heading("status", text= "Status")

        self.Product_Table["show"] = "headings"

        self.Product_Table.column("pid", width= 40)
        self.Product_Table.column("name", width= 100)
        self.Product_Table.column("price", width= 100)
        self.Product_Table.column("qty", width= 40)
        self.Product_Table.column("status", width= 90)

        self.Product_Table.pack(fill=BOTH, expand=1)
        self.Product_Table.bind("<ButtonRelease-1>", self.get_DATA)

        lbl_note = Label(ProductFrame1, text= "Note: 'Enter 0 Quantity to remove product from the cart'", font= ("goudy old style",12), anchor= 'w', bg= "white", fg= "red").pack(side=BOTTOM, fill= X)

        #--------------COSTUMER FRAME---------------------------
        self.var_name = StringVar()
        self.var_contact = StringVar()

        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=408, y=110, width=530, height=70)

        cTitle = Label(CustomerFrame, text= "Customer Details", font= ("goudy old style", 15), bg= "lightgray").pack(side=TOP, fill=X)

        lbl_name2 = Label(CustomerFrame, text= "Name:",font= ("times new roman", 15), bg= "white").place(x=5, y=35)

        lbl_SEARCH_name2 = Entry(CustomerFrame, textvariable= self.var_name, font= ("times new roman", 13), bg= "lightyellow" ).place(x=63, y=35, width=170)

        lbl_contact = Label(CustomerFrame, text= "Contact No:",font= ("times new roman", 15), bg= "white").place(x=250, y=35)

        lbl_SEARCH_contact = Entry(CustomerFrame, textvariable= self.var_contact, font= ("times new roman", 13), bg= "lightyellow" ).place(x=350, y=35, width=165)

        #------------CALCULATOR AND CART FRAME-------------------

        Cal_CartFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Cal_CartFrame.place(x=408, y=190, width=530, height=360)

        #--------CALCULATOR FRAME-------------------
        self.var_cal_input = StringVar()

        Cal_Frame = Frame(Cal_CartFrame, bd=9, relief=RIDGE, bg="white")
        Cal_Frame.place(x=5, y=10, width=268, height=340)

        self.txt_cal_input = Entry(Cal_Frame, textvariable= self.var_cal_input, font= ("arial", 15, "bold"), width=21, bd=10, relief=GROOVE, state='readonly', justify=RIGHT)
        self.txt_cal_input.grid(row=0, columnspan=4)

        btn_7 = Button(Cal_Frame, text= '7', font=("arial", 15, "bold"), command=lambda:self.get_INPUT(7), bd=5, width=4, pady=12, cursor= "hand2").grid(row=1, column=0)
        btn_8 = Button(Cal_Frame, text= '8', font=("arial", 15, "bold"), command=lambda:self.get_INPUT(8), bd=5, width=4, pady=12, cursor= "hand2").grid(row=1, column=1)
        btn_9 = Button(Cal_Frame, text= '9', font=("arial", 15, "bold"), command=lambda:self.get_INPUT(9), bd=5, width=4, pady=12, cursor= "hand2").grid(row=1, column=2)
        btn_plus = Button(Cal_Frame, text= '+', font=("arial", 15, "bold"), command=lambda:self.get_INPUT('+'), bd=5, width=4, pady=12, cursor= "hand2").grid(row=1, column=3)

        btn_4 = Button(Cal_Frame, text= '4', font=("arial", 15, "bold"), command=lambda:self.get_INPUT(4), bd=5, width=4, pady=12, cursor= "hand2").grid(row=2, column=0)
        btn_5 = Button(Cal_Frame, text= '5', font=("arial", 15, "bold"), command=lambda:self.get_INPUT(5), bd=5, width=4, pady=12, cursor= "hand2").grid(row=2, column=1)
        btn_6 = Button(Cal_Frame, text= '6', font=("arial", 15, "bold"), command=lambda:self.get_INPUT(6), bd=5, width=4, pady=12, cursor= "hand2").grid(row=2, column=2)
        btn_minus = Button(Cal_Frame, text= '-', font=("arial", 15, "bold"), command=lambda:self.get_INPUT('-'), bd=5, width=4, pady=12, cursor= "hand2").grid(row=2, column=3)

        btn_1 = Button(Cal_Frame, text= '1', font=("arial", 15, "bold"), command=lambda:self.get_INPUT(1), bd=5, width=4, pady=12, cursor= "hand2").grid(row=3, column=0)
        btn_2 = Button(Cal_Frame, text= '2', font=("arial", 15, "bold"), command=lambda:self.get_INPUT(2), bd=5, width=4, pady=12, cursor= "hand2").grid(row=3, column=1)
        btn_3 = Button(Cal_Frame, text= '3', font=("arial", 15, "bold"), command=lambda:self.get_INPUT(3), bd=5, width=4, pady=12, cursor= "hand2").grid(row=3, column=2)
        btn_multiply = Button(Cal_Frame, text= '*', font=("arial", 15, "bold"), command=lambda:self.get_INPUT('*'), bd=5, width=4, pady=12, cursor= "hand2").grid(row=3, column=3)

        btn_0 = Button(Cal_Frame, text= '0', font=("arial", 15, "bold"), command=lambda:self.get_INPUT(0), bd=5, width=4, pady=12, cursor= "hand2").grid(row=4, column=0)
        btn_c = Button(Cal_Frame, text= 'C', font=("arial", 15, "bold"), command=self.clear_cal, bd=5, width=4, pady=12, cursor= "hand2").grid(row=4, column=1)
        btn_eq = Button(Cal_Frame, text= '=', font=("arial", 15, "bold"), command= self.perform_cal, bd=5, width=4, pady=12, cursor= "hand2").grid(row=4, column=2)
        btn_div = Button(Cal_Frame, text= '/', font=("arial", 15, "bold"), command=lambda:self.get_INPUT('/'), bd=5, width=4, pady=12, cursor= "hand2").grid(row=4, column=3)
        #----------CART FRAME-------------------

        Cart_Frame = Frame(Cal_CartFrame, bd=3, relief=RIDGE)
        Cart_Frame.place(x=280, y=8, width=245, height=342)

        self.cartTitle = Label(Cart_Frame, text= "Cart \t Total Product: [0]", font= ("goudy old style", 14), bg= "lightgray")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(Cart_Frame, orient= VERTICAL)
        scrollx = Scrollbar(Cart_Frame, orient= HORIZONTAL)

        self.Cart_Table = ttk.Treeview(Cart_Frame, columns= ("pid", "name", "price", "qty"), yscrollcommand= scrolly.set, xscrollcommand= scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.Cart_Table.xview)
        scrolly.config(command=self.Cart_Table.yview)

        self.Cart_Table.heading("pid", text= "P Id.")
        self.Cart_Table.heading("name", text= "Name")
        self.Cart_Table.heading("price", text= "Price")
        self.Cart_Table.heading("qty", text= "Qty")

        self.Cart_Table["show"] = "headings"

        self.Cart_Table.column("pid", width= 40)
        self.Cart_Table.column("name", width= 90)
        self.Cart_Table.column("price", width= 90)
        self.Cart_Table.column("qty", width= 40)

        self.Cart_Table.pack(fill=BOTH, expand=1)
        self.Cart_Table.bind("<ButtonRelease-1>", self.get_DATA_cart)

        #----------CART WIDGETS BUTTONS--------------
        self.var_pid = StringVar()
        self.var_p_name = StringVar()
        self.var_p_price = StringVar()
        self.var_p_qty = StringVar()
        self.var_stock = StringVar()

        CartWidgetsFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        CartWidgetsFrame.place(x=408, y=550, width=530, height=90)

        lbl_p_name = Label(CartWidgetsFrame, text= "Product Name", font= ("times new roman", 13), bg= "white"). place(x=5, y=2)
        txt_p_name = Entry(CartWidgetsFrame, textvariable= self.var_p_name, font= ("times new roman", 13), bg= "lightyellow", state= 'readonly'). place(x=5, y=30, width=190, height=22)

        
        lbl_p_price = Label(CartWidgetsFrame, text= "Price per Unit", font= ("times new roman", 13), bg= "white"). place(x=230, y=2)
        txt_p_price = Entry(CartWidgetsFrame, textvariable= self.var_p_price, font= ("times new roman", 13), bg= "lightyellow", state= 'readonly'). place(x=230, y=30, width=150, height=22)

        lbl_p_qty = Label(CartWidgetsFrame, text= "Quantity", font= ("times new roman", 13), bg= "white"). place(x=390, y=2)
        txt_p_qty = Entry(CartWidgetsFrame, textvariable= self.var_p_qty, font= ("times new roman", 13), bg= "lightyellow"). place(x=390, y=30, width=120, height=22)

        self.lbl_p_instock = Label(CartWidgetsFrame, text= "In Stock", font= ("times new roman", 13), bg= "white")
        self.lbl_p_instock.place(x=5, y=55)

        btn_clear_cart = Button(CartWidgetsFrame, text="Clear", command= self.clear_CART, font= ("times new roman", 15, "bold"), bg= "lightgray", cursor= "hand2").place(x=180, y=57, width=120, height=25)

        btn_add_cart = Button(CartWidgetsFrame, text="Add | Update Cart", command= self.add_update_cart, font= ("times new roman", 15, "bold"), bg= "orange", cursor= "hand2").place(x=310, y=57, width=200, height=25)

        #-----------------BILLING AREA-----------------------

        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg= "white")
        billFrame.place(x=943, y=110, width=330, height=410) 

        bTitle = Label(billFrame, text= "Customer Bill Area", font= ("goudy old style", 20, "bold"), bg= "#f44336", fg= "white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)  
        scrolly.pack(side=RIGHT, fill=Y)
        self.txt_bill_area = Text(billFrame, yscrollcommand= scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #-------------BILLING BUTTONS-----------------------

        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg= "white")
        billMenuFrame.place(x=943, y=520, width=330, height=120)

        self.lbl_amount = Label(billMenuFrame, text= "Bill Amount\n[0]", font= ("goudy old style", 13, "bold"), bg= "#3f51b5", fg= "white")
        self.lbl_amount.place(x=2, y=5, width=111, height=60)

        self.lbl_discount = Label(billMenuFrame, text= "Discount\n[5%]", font= ("goudy old style", 13, "bold"), bg= "#8bc34a", fg= "white")
        self.lbl_discount.place(x=114, y=5, width=95, height=60)

        self.lbl_net_pay = Label(billMenuFrame, text= "Net Pay\n[0]", font= ("goudy old style", 13, "bold"), bg= "#607d8b", fg= "white")
        self.lbl_net_pay.place(x=210, y=5, width=110, height=60)

        #----------BILL MENU BUTTONS----------------------

        btn_print = Button(billMenuFrame, text= "Print", command=self.print_BILL, font= ("goudy old style", 13, "bold"), bg= "lightgreen", fg= "white", cursor= "hand2")
        btn_print.place(x=2, y=70, width=111, height=40)

        btn_clear_all = Button(billMenuFrame, text= "Clear All", command=self.clear_ALL, font= ("goudy old style", 13, "bold"), bg= "gray", fg= "white",cursor= "hand2")
        btn_clear_all.place(x=114, y=70, width=95, height=40)

        btn_generate = Button(billMenuFrame, text= "Generate", command= self.generate_bill, font= ("goudy old style", 13, "bold"), bg= "#009688", fg= "white", cursor= "hand2")
        btn_generate.place(x=210, y=70, width=110, height=40)

        #----------------FOOTER--------------------
        # footer = Label(self.root, text= "IMS-Inventory Management System | Developed by student\nFor any Technical Issue Contact: 98xxxxx01", font= ("times new roman", 8), bg= "#4d636d" , fg= "white").pack(side=BOTTOM, fill=X)

        self.show()
        # self.bill_TOP()
        self.update_DATE_TIME()

#----------------ALL FUNCTIONS---------------------
        
    def get_INPUT(self,num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con = sqlite3.connect(database='DatabaseProject.db')
        cur = con.cursor()
        try:
            cur.execute("select pid, name, price, qty, status from product where status = 'Active'")
            rows = cur.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            for row in rows:
               self.Product_Table.insert('', END, values=row)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)

    
    def search(self):
        con = sqlite3.connect(database='DatabaseProject.db')
        cur = con.cursor()
        try:
            if self.var_search.get()=="":
                 messagebox.showerror("Error", "Selected criteria should be required", parent= self.root)
            else:               
             cur.execute("select pid, name, price, qty, status from product where name  LIKE '%" + self.var_search.get()+"%' and status = 'Active' ")
             rows = cur.fetchall()
             if len(rows) != 0:
              self.Product_Table.delete(*self.Product_Table.get_children())
              for row in rows:
                self.Product_Table.insert('', END, values=row)
             else:
                messagebox.showerror("Error", "No Record Found", parent= self.root)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)

    def get_DATA(self, ev):
        f =self.Product_Table.focus()
        content =self.Product_Table.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_p_name.set(row[1])
        self.var_p_price.set(row[2])
        self.lbl_p_instock.config(text= f"In Stock[{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_p_qty.set('1')

    def get_DATA_cart(self, ev):
        f =self.Cart_Table.focus()
        content =self.Cart_Table.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_p_name.set(row[1])
        self.var_p_price.set(row[2])
        self.var_p_qty.set(row[3])
        self.lbl_p_instock.config(text= f"In Stock[{str(row[4])}]")
        self.var_stock.set(row[4])
    

    def add_update_cart(self):
       if self.var_pid.get()=='':
          messagebox.showerror('Error', "Please select product from the list", parent = self.root)
       elif self.var_p_qty.get()=='':
          messagebox.showerror('Error', "Quantity is required", parent = self.root)
       elif int(self.var_p_qty.get()) > int(self.var_stock.get()):
          messagebox.showerror('Error', "Invalid Quantity", parent = self.root)
    
       else:
        #   price_cal = float(int(self.var_p_qty.get()) * float(self.var_p_price.get()))
        # pid,name,price,qty,status
          
          price_cal = self.var_p_price.get()
          
          cart_data = [self.var_pid.get(),self.var_p_name.get(),price_cal,self.var_p_qty.get(), self.var_stock.get()]

        #----------UPDATE CART-----------------
          present = 'no'
          index_ = 0
          for row in self.cart_list:
               if self.var_pid.get() == row[0]:
                  present = 'yes'
                  break
               index_+=1
          if present == 'yes':
               op = messagebox.askyesno('Confirmation', "Product already present\nDo you want to Update| Remove from the Cart List", parent = self.root)
               if op == True:
                   if self.var_p_qty.get() == "0":
                          self.cart_list.pop(index_)
                   else:
                    #   self.cart_list[index_][2] = price_cal #price
                      self.cart_list[index_][3] = self.var_p_qty.get() #qty
          else:
               self.cart_list.append(cart_data)

       self.show_cart()
       self.bill_updates()


    def bill_updates(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
             self.bill_amnt = self.bill_amnt + (float(row[2])*int(row[3]))
        
        self.discount = (self.bill_amnt*5)/100
        self.net_pay = self.bill_amnt - self.discount
        self.lbl_amount.config(text= f'Bill Amnt.\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text= f'Net Pay\n{str(self.net_pay)}')
        self.cartTitle.config( text= f"Cart \t Total Product: [{str(len(self.cart_list))}]")


    def show_cart(self):
        try:
            self.Cart_Table.delete(*self.Cart_Table.get_children())
            for row in self.cart_list:
               self.Cart_Table.insert('', END, values=row)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)

    def generate_bill(self):
        if self.var_name.get()=='' or self.var_contact.get() =='':
            messagebox.showerror("Error","Customer Details are Required", parent= self.root)
        elif len(self.cart_list) == 0: 
            messagebox.showerror("Error","Please select the product first!!!", parent= self.root)
        else:
            #-------------BILL TOP----------------
            self.bill_TOP()

             #-------------BILL MIDDLE----------------
            self.bill_MIDDLE()
            
             #-------------BILL BOTTOM----------------
            self.bill_BOTTOM()

            fp = open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved', "Bill has been generated/saved in backend", parent = self.root)
            self.chk_print = 1
            

    def bill_TOP(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%y"))

        bill_Top_temp = f'''
\t\tXYZ-Inventory
\t Phone No. 98725******, Delhi-110074
{str("="*38)}
Customer Name: {self.var_name.get()}
Ph No. : {self.var_contact.get()}
Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d%m%y"))}
{str("="*38)}
    Product Name\t\t\tQTY\tPrice
{str("="*38)}
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_Top_temp)

    def bill_BOTTOM(self):
        bill_BOTTOM_temp = f'''
{str("="*38)}
Bill Amount\t\t\tRs.{self.bill_amnt}
Discount\t\t\tRs.{self.discount}
Net Pay\t\t\tRs.{self.net_pay}
{str("="*38)}\n
        '''
        self.txt_bill_area.insert(END, bill_BOTTOM_temp)
    
    def bill_MIDDLE(self):
      con = sqlite3.connect(database='DatabaseProject.db')
      cur = con.cursor()
      try:
        for row in self.cart_list:
            # pid, name, price, qty, stock
            pid = row[0]
            name = row[1]
            qty = int(row[4]) - int(row[3])
            status = 'Active' if qty > 0 else 'Inactive'
            price = float(row[2]) * int(row[3])
            price = str(price)
            self.txt_bill_area.insert(END, "\n " + name + "\t\t" + row[3] + "\tRs." + price)

            # Update quantity and status in the product table
            cur.execute('UPDATE product SET qty=?, status=? WHERE pid=?', (qty, status, pid))
            con.commit()

        con.close()
        self.show()  # Refresh the product table after updating quantities and status
      except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear_CART(self):
        self.var_pid.set('')
        self.var_p_name.set('')
        self.var_p_price.set('')
        self.var_p_qty.set('')
        self.lbl_p_instock.config(text= f"In Stock")
        self.var_stock.set('')

    def clear_ALL(self):
        del self.cart_list[:]
        self.var_name.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config( text= f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.chk_print = 0
        self.clear_CART()
        self.show()
        self.show_cart()
    
    def update_DATE_TIME(self):
        TIME_ = time.strftime("%I:%M:%S")
        DATE_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config( text=f"Welcome to Inventory Management System\t\t Date: {str(DATE_)}\t\t Time: {str(TIME_)}")
        self.lbl_clock.after(200, self.update_DATE_TIME)
    
    def print_BILL(self):
        if self.chk_print == 1:
            messagebox.showinfo('Print', "Please wait while printing", parent = self.root)
            new_FILE = tempfile.mktemp('.txt')
            open(new_FILE, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_FILE, 'print')
        else:
            messagebox.showerror('Error', "Please generate bill to print receipt", parent = self.root)

    
    def logout(self):
        self.root.destroy()
        os.system("python Login.py")
            

if __name__ == "__main__":
    root = Tk()
    obj = billingClass(root)
    root.mainloop()
