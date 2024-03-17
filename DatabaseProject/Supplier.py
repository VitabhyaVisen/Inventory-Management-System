import sqlite3
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x500+200+130")
        self.root.title("Inventory Management System | Developed by Student")
        self.root.config(bg="white")
        self.root.focus_force()

        #------------------ALL VARIABLE---------------
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_sup_invoice = StringVar()
        self.var_sup_name = StringVar()
        self.var_sup_contact = StringVar()
        

        # -----------------SEARCH FRAME---------------
        #--------------------OPTIONS------------------
        lbl_search = Label(self.root, text= "Invoice No", bg= "white" ,font=("TkDefaultFont", 12, ""))
        lbl_search.place(x=670, y=80,)

        txt_search = Entry(self.root, textvariable= self.var_searchtxt, font=("Helvetica", 11), bg="light yellow").place(x=750, y=80, width=100)
        btn_search = Button(self.root, text="Search", command= self.search, font=("Helvetica", 10),bg="#98FB98", fg="#36454F", cursor="hand2").place(x=860, y=79, width=100, height=28)

        #------------------TITLE------------------------
        title = Label(self.root, text= "Supplier's Details", font=("Palatino Linotype", 20, "bold"), bg="teal", fg="#FFFDD0").place(x=50, y=10, width=923, height=40)

        #------------------CONTENT----------------------

        #------------------ROW-1------------------------
        lbl_sup_invoice = Label(self.root, text= "Invoice No. ", font=("Trebuchet MS", 16), bg="white").place(x=50, y=80) 
        txt_sup_invoice = Entry(self.root, textvariable= self.var_sup_invoice, font=("calibri", 16), bg="lightyellow").place(x=180, y=80, width=160) 

        #------------------ROW-2-----------------------
        lbl_name = Label(self.root, text= "Name", font=("Trebuchet MS", 16), bg="white").place(x=50, y=120) 
        txt_name = Entry(self.root, textvariable= self.var_sup_name, font=("calibri", 12), bg="lightyellow").place(x=180, y=120, width=160) 


        #------------------ROW-3-----------------------
        lbl_contact = Label(self.root, text= "Contact", font=("Trebuchet MS", 16), bg="white").place(x=50, y=160) 

        txt_contact = Entry(self.root, textvariable= self.var_sup_contact, font=("calibri", 16), bg="lightyellow").place(x=180, y=160, width=160) 
       
        #-----------------ROW-4------------------------
        lbl_desc = Label(self.root, text= "Description", font=("Trebuchet MS", 16), bg="white").place(x=50, y=200) 

        self.txt_desc = Text(self.root, font=("calibri", 16), bg="lightyellow")
        self.txt_desc.place(x=180, y=200, width=470, height=120) 
        
        #-----------------BUTTONS---------------------
        btn_save = Button(self.root, text="Save", command=self.add, font=("Helvetica", 10),bg="#4682B4", fg="#FFFFFF", cursor="hand2").place(x=180, y=350, width=110, height=35)
        btn_update = Button(self.root, text="Update", command= self.update, font=("Helvetica", 10),bg="#4caf50", fg="#FFFFFF", cursor="hand2").place(x=300, y=350, width=110, height=35)        
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("Helvetica", 10),bg="#FF4500", fg="#FFFFFF", cursor="hand2").place(x=420, y=350, width=110, height=35) 
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Helvetica", 10),bg="#607d8b", fg="#FFFFFF", cursor="hand2").place(x=540, y=350, width=110, height=35)        

        #----------------SUPPLIER'S DETAILS FRAME-------------
        sup_FRAME = Frame(self.root, bd=3, relief=RIDGE)
        sup_FRAME.place(x=670, y=120, width=300, height=350)

        scrolly = Scrollbar(sup_FRAME, orient= VERTICAL)
        scrollx = Scrollbar(sup_FRAME, orient= HORIZONTAL)

        self.SupplierTable = ttk.Treeview(sup_FRAME, columns= ("invoice", "name", "contact", "desc"), yscrollcommand= scrolly.set, xscrollcommand= scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("invoice", text= "Invoice No.")
        self.SupplierTable.heading("name", text= "Name")
        self.SupplierTable.heading("contact", text= "Contact")
        self.SupplierTable.heading("desc", text= "Description")

        self.SupplierTable["show"] = "headings"

        self.SupplierTable.column("invoice", width= 90)
        self.SupplierTable.column("name", width= 100)
        self.SupplierTable.column("contact", width= 100)
        self.SupplierTable.column("desc", width= 100)

        self.SupplierTable.pack(fill=BOTH, expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_DATA)
        self.show()
# -------------------------------------------------------------------------------------------------------------------
    def add(self):
      con = sqlite3.connect(database='DatabaseProject.db')
      cur = con.cursor()
      try:
          if self.var_sup_invoice.get() == "":
              messagebox.showerror("Error","Invoice No. must be required", parent= self.root)
          else:
              cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
              row = cur.fetchone()
              if row != None:
                  messagebox.showerror("Error", "Invoice No. is already assigned, try different", parent= self.root)
              else:
                  cur.execute("Insert into supplier (invoice, name, contact, desc) values(?,?,?,?)",(
                      self.var_sup_invoice.get(),
                      self.var_sup_name.get(),
                      self.var_sup_contact.get(),
                      self.txt_desc.get('1.0',END)
                  ,))
                  con.commit()
                  messagebox.showinfo("Success", "Supplier added successfully", parent= self.root)
                  self.show()
      except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)

    def show(self):
        con = sqlite3.connect(database='DatabaseProject.db')
        cur = con.cursor()
        try:
            cur.execute("select * from supplier")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('', END, values=row)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)


    def get_DATA(self, ev):
     try:
        f = self.SupplierTable.focus()
        content = self.SupplierTable.item(f)
        row = content['values']
        if row:
            self.var_sup_invoice.set(row[0])
            self.var_sup_name.set(row[1])
            self.var_sup_contact.set(row[2])
            self.txt_desc.delete('1.0', END)
            self.txt_desc.insert(END, row[3])
        else:
            messagebox.showerror("Error", "No data selected", parent=self.root)
     except Exception as ex:
        messagebox.showerror("Error", f"Error during data retrieval: {str(ex)}", parent=self.root)




    def update(self):
      con = sqlite3.connect(database='DatabaseProject.db')
      cur = con.cursor()
      try:
          if self.var_sup_invoice.get() == "":
              messagebox.showerror("Error","Invoice No. must be required", parent= self.root)
          else:
              cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
              row = cur.fetchone()
              if row == None:
                  messagebox.showerror("Error", "Invalid Invoice No.", parent= self.root)
              else:
                  cur.execute("Update supplier set name=?, contact=?, desc=?, where invoice=?",(
                      self.var_sup_name.get(),
                      self.var_sup_contact.get(),
                      self.txt_desc.get('1.0',END),
                      self.var_sup_invoice.get()
                  ))
                  con.commit()
                  messagebox.showinfo("Success", "Supplier updated successfully", parent= self.root)
                  self.show()
      except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)        
    

   
    def delete(self):
         con = sqlite3.connect(database='DatabaseProject.db')
         cur = con.cursor()
         try:
              if self.var_sup_invoice.get() == "":
               messagebox.showerror("Error","Invoice No. must be required", parent= self.root)
              else:
               cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))

              row = cur.fetchone()
              if row == None:
                  messagebox.showerror("Error", "Invalid Invoice No.", parent= self.root)
              else:
                  op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent = self.root)
                  if op==True:
                    cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                    con.commit()
                    messagebox.showinfo("Delete", "Supplier Deleted Successfully", parent= self.root)
                    self.clear()  
         except Exception as ex:
             messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)


    

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_sup_name.set("")
        self.var_sup_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(database='DatabaseProject.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                 messagebox.showerror("Error", "Invoice No. should be required", parent= self.root)
            else:               
             cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
             row = cur.fetchone()
             if row != None:
               self.SupplierTable.delete(*self.SupplierTable.get_children())
               self.SupplierTable.insert('', END, values=row)
             else:
                messagebox.showerror("Error", "No Record Found", parent= self.root)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)



if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()
