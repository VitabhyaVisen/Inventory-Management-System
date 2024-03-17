import sqlite3
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x500+200+130")
        self.root.title("Inventory Management System | Developed by Student")
        self.root.config(bg="white")
        self.root.focus_force()

        #---------VARIABLES----------------------
        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.var_cat_list = []
        self.var_sup_list = []
        self.fetch_cat_sup()
        self.var_name= StringVar()
        
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        #---------------PRODUCT FRAME--------------------

        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

       
        #--------------TITLE-----------------
        title = Label(product_Frame, text= "Manage Product Details", font=("Palatino Linotype", 18, "bold"), bg="teal", fg="#FFFDD0").pack(side=TOP,fill=X)

        lbl_category = Label(product_Frame, text= "Category", font=("Palatino Linotype", 18, ""), bg="white").place(x=30, y=60)
        lbl_supplier = Label(product_Frame, text= "Supplier", font=("Palatino Linotype", 18, ""), bg="white").place(x=30, y=110)
        lbl_product_detail = Label(product_Frame, text= "Name", font=("Palatino Linotype", 18, ""), bg="white").place(x=30, y=160)
        lbl_price = Label(product_Frame, text= "Price", font=("Palatino Linotype", 18, ""), bg="white").place(x=30, y=210)
        lbl_quantity = Label(product_Frame, text= "Quantity", font=("Palatino Linotype", 18, ""), bg="white").place(x=30, y=260)
        lbl_status = Label(product_Frame, text= "Status", font=("Palatino Linotype", 18, ""), bg="white").place(x=30, y=310)
        
       
        #--------------------COLUMN2------------------
        cmb_cat = ttk.Combobox(product_Frame, textvariable= self.var_cat, values=self.var_cat_list, state="readonly", justify=CENTER, font=("calibri", 15))
        cmb_cat.place(x=150, y=67, width=200)
        cmb_cat.current(0)

        cmb_sup = ttk.Combobox(product_Frame, textvariable= self.var_sup, values=self.var_sup_list, state="readonly", justify=CENTER, font=("calibri", 15))
        cmb_sup.place(x=150, y=117, width=200)
        cmb_sup.current(0)

        txt_name = Entry(product_Frame, textvariable= self.var_name, font=("calibri", 15), bg="lightyellow").place(x=150, y=167, width=200)
        txt_price = Entry(product_Frame, textvariable= self.var_price, font=("calibri", 15), bg="lightyellow").place(x=150, y=217, width=200)
        txt_quantity = Entry(product_Frame, textvariable= self.var_qty, font=("calibri", 15), bg="lightyellow").place(x=150, y=267, width=200)
        
        cmb_status = ttk.Combobox(product_Frame, textvariable= self.var_status, values=("Active", "Inactive"), state="readonly", justify=CENTER, font=("calibri", 15))
        cmb_status.place(x=150, y=317, width=200)
        cmb_status.current(0)

        #----------BUTTONS--------------

        btn_save = Button(product_Frame, text="Save", command=self.add, font=("Helvetica", 10),bg="#4682B4", fg="#FFFFFF", cursor="hand2").place(x=10, y=400, width=100, height=40)
        btn_update = Button(product_Frame, text="Update", command= self.update, font=("Helvetica", 10),bg="#4caf50", fg="#FFFFFF", cursor="hand2").place(x=120, y=400, width=100, height=40)        
        btn_delete = Button(product_Frame, text="Delete", command=self.delete, font=("Helvetica", 10),bg="#FF4500", fg="#FFFFFF", cursor="hand2").place(x=230, y=400, width=100, height=40) 
        btn_clear = Button(product_Frame, text="Clear", command=self.clear, font=("Helvetica", 10),bg="#607d8b", fg="#FFFFFF", cursor="hand2").place(x=340, y=400, width=100, height=40)

         #---------------SEARCH FRAME----------------------

        SearchFrame = LabelFrame(self.root, text="Search Employee", font=("Helvetica", 12, "bold"), bg="white", fg="black")
        SearchFrame.place(x=480, y=10, width=510, height=80)

        #--------------------OPTIONS------------------
        cmb_search = ttk.Combobox(SearchFrame, textvariable= self.var_searchby, values=("Select","Category", "Supplier", "Name"), state="readonly", justify=CENTER, font=("TkDefaultFont", 10))
        cmb_search.place(x=10, y=10, width=180,)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable= self.var_searchtxt, font=("Helvetica", 11), bg="light yellow").place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", command= self.search, font=("Helvetica", 10),bg="#98FB98", fg="#36454F", cursor="hand2").place(x=370, y=8, width=120, height=25)

        #----------------PRODUCTS DETAILS FRAME-------------


        pro_FRAME = Frame(self.root, bd=3, relief=RIDGE)
        pro_FRAME.place(x=480, y=100, width=510, height=390)

        scrolly = Scrollbar(pro_FRAME, orient= VERTICAL)
        scrollx = Scrollbar(pro_FRAME, orient= HORIZONTAL)

        self.ProductTable = ttk.Treeview(pro_FRAME, columns= ("pid", "Category", "Supplier", "name", "price", "qty", "status"), yscrollcommand= scrolly.set, xscrollcommand= scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid", text= "Product Id")
        self.ProductTable.heading("Category", text= "Category")
        self.ProductTable.heading("Supplier", text= "Supplier")
        self.ProductTable.heading("name", text= "Name")
        self.ProductTable.heading("price", text= "Price")
        self.ProductTable.heading("qty", text= "Quantity")
        self.ProductTable.heading("status", text= "Status")
       
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width= 90)
        self.ProductTable.column("Category", width= 100)
        self.ProductTable.column("Supplier", width= 100)
        self.ProductTable.column("name", width= 100)
        self.ProductTable.column("price", width= 100)
        self.ProductTable.column("qty", width= 100)
        self.ProductTable.column("status", width= 100)
       
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_DATA)
        self.show()
        
    
#----------------------------------------------------------------------------
        

    def fetch_cat_sup(self):
       con = sqlite3.connect(database='DatabaseProject.db')
       cur = con.cursor()
       self.var_cat_list.append("Empty")
       self.var_sup_list.append("Empty")
       try: 
          cur.execute("Select name from category") 
          cat = cur.fetchall()
          if len(cat) > 0:
            del self.var_cat_list[:]
            self.var_cat_list.append("Select")
            for i in cat:
                self.var_cat_list.append(i[0])
          cur.execute("Select name from supplier") 
          sup = cur.fetchall()
          del self.var_sup_list[:]
          if len(sup) > 0:
            self.var_sup_list.append("Select")
            for i in sup:
                self.var_sup_list.append(i[0])
       except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)
    

    
    def add(self):
      con = sqlite3.connect(database='DatabaseProject.db')
      cur = con.cursor()
      try:
          if self.var_cat.get() == "Select" or self.var_cat.get() == "Select" or self.var_name.get() == "Select":
              messagebox.showerror("Error","All fields are required", parent= self.root)
          else:
              cur.execute("Select * from product where name=?",(self.var_name.get(),))
              row = cur.fetchone()
              if row != None:
                  messagebox.showerror("Error", "Product Already Available, try Different", parent= self.root)
              else:
                  cur.execute("Insert into product ( Category, Supplier, name, price, qty, status) values(?,?,?,?,?,?)",(
                      self.var_cat.get(),
                      self.var_sup.get(),
                      self.var_name.get(),
                      self.var_price.get(),
                      self.var_qty.get(),
                      self.var_status.get()
                  ))
                  con.commit()
                  messagebox.showinfo("Success", "Product added successfully", parent= self.root)
                  self.show()
      except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)

    def show(self):
        con = sqlite3.connect(database='DatabaseProject.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
               self.ProductTable.insert('', END, values=row)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)


    def get_DATA(self, ev):
     try:
        f =self.ProductTable.focus()
        content =self.ProductTable.item(f)
        row = content['values']
        if row:
             self.var_pid.set(row[0])
             self.var_cat.set(row[1]),
             self.var_sup.set(row[2]),
             self.var_name.set(row[3]),
             self.var_price.set(row[4]),
             self.var_qty.set(row[5]),
             self.var_status.set(row[6])
            
        else:
            messagebox.showerror("Error", "No data selected", parent=self.root)
     except Exception as ex:
        messagebox.showerror("Error", f"Error during data retrieval: {str(ex)}", parent=self.root)




    def update(self):
      con = sqlite3.connect(database='DatabaseProject.db')
      cur = con.cursor()
      try:
          if self.var_pid.get() == "":
              messagebox.showerror("Error","Please select product from list", parent= self.root)
          else:
              cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
              row = cur.fetchone()
              if row == None:
                  messagebox.showerror("Error", "Invalid Product", parent= self.root)
              else:
                  cur.execute("Update product set Category=?,Supplier=?, name=?, price=?, qty=?, status=? where pid=?",(
                      self.var_cat.get(),
                      self.var_sup.get(),
                      self.var_name.get(),
                      self.var_price.get(),
                      self.var_qty.get(),
                      self.var_status.get(),
                      self.var_pid.get()
                  ))
                  con.commit()
                  messagebox.showinfo("Success", "Product updated successfully", parent= self.root)
                  self.show()
      except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)        
    

    def delete(self):
         con = sqlite3.connect(database='DatabaseProject.db')
         cur = con.cursor()
         try:
              if self.var_pid.get() == "":
               messagebox.showerror("Error","Select product from the list", parent= self.root)
              else:
               cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
              row = cur.fetchone()
              if row == None:
                  messagebox.showerror("Error", "Invalid Product", parent= self.root)
              else:
                  op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent = self.root)
                  if op == True:
                    cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                    con.commit()
                    messagebox.showinfo("Delete", "Product Deleted Successfully", parent= self.root)
                    self.clear()
                    self.show()       
         except Exception as ex:
             messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)
    

    def clear(self):
       self.var_cat.set("Select"),
       self.var_sup.set("Select"),
       self.var_name.set(""),
       self.var_price.set(""),
       self.var_qty.set(""),
       self.var_status.set("Active"),
       self.var_pid.set("")
       self.var_searchtxt.set("")
       self.var_searchby.set("Select")
       self.show()

    def search(self):
        con = sqlite3.connect(database='DatabaseProject.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error", "Select search by option", parent= self.root)
            elif self.var_searchtxt.get()=="":
                 messagebox.showerror("Error", "Selected criteria should be required", parent= self.root)
            else:               
             cur.execute("select * from product where " + self.var_searchby.get()+" LIKE '%" + self.var_searchtxt.get()+"%'")
             rows = cur.fetchall()
             if len(rows) != 0:
              self.ProductTable.delete(*self.ProductTable.get_children())
              for row in rows:
                self.ProductTable.insert('', END, values=row)
             else:
                messagebox.showerror("Error", "No Record Found", parent= self.root)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)



if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()
