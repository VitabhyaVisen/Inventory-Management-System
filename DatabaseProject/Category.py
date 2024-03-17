import sqlite3
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x500+200+130")
        self.root.title("Inventory Management System | Developed by Student")
        self.root.config(bg="white")
        self.root.focus_force()

        #-----------------VARIALES---------------
        self.var_cat_id = StringVar()
        self.var_cat_name = StringVar()
        
        #-----------------TITLE------------------
        lbl_title = Label(self.root, text= "Manage Product Category", font= ("Times New Roman", 30,), bg= "#184a45", fg= "white").pack(side=TOP, fill=X, padx=10, pady=2)

        lbl_name = Label(self.root, text= "Enter Category Name", font= ("Times New Roman", 30), bg= "white").place(x=10, y=100)
        txt_name = Entry(self.root, textvariable= self.var_cat_name, font= ("Times New Roman", 18), bg= "lightyellow").place(x=10, y=170, width=300)

        btn_add = Button(self.root, text= "ADD", command=self.add, font= ("Times New Roman", 15), bg= "#4caf50", fg= "white", cursor= "hand2").place(x=320, y=170, width=130, height=30)
        btn_delete = Button(self.root, text= "Delete", command= self.delete, font= ("Times New Roman", 15), bg= "red", fg= "white", cursor= "hand2").place(x=480, y=170, width=130, height=30)


        #-------------CATEGORY DETAILS-----------------

        cat_FRAME = Frame(self.root, bd=3, relief=RIDGE)
        cat_FRAME.place(x=640, y=100, width=340, height=100)

        scrolly = Scrollbar(cat_FRAME, orient= VERTICAL)
        scrollx = Scrollbar(cat_FRAME, orient= HORIZONTAL)

        self.CateoryTable = ttk.Treeview(cat_FRAME, columns= ("cid", "name"), yscrollcommand= scrolly.set, xscrollcommand= scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CateoryTable.xview)
        scrolly.config(command=self.CateoryTable.yview)

        self.CateoryTable.heading("cid", text= "Category Id")
        self.CateoryTable.heading("name", text= "Name")
        

        self.CateoryTable["show"] = "headings"

        self.CateoryTable.column("cid", width= 90)
        self.CateoryTable.column("name", width= 100)

        self.CateoryTable.pack(fill=BOTH, expand=1)
        self.CateoryTable.bind("<ButtonRelease-1>", self.get_DATA)

        #------------------IMAGES-------------------------
        self.im1 = Image.open("images/images/cat.jpg")
        self.im1 = self.im1.resize((500, 250), resample=Image.Resampling.LANCZOS)
        self.im1 = ImageTk.PhotoImage(self.im1)

        self.lbl_im1 = Label(self.root, image= self.im1, bd= 2, relief=RAISED)
        self.lbl_im1.place(x=10, y=220, width=490)

        self.im2 = Image.open("images/images/category.jpg")
        self.im2 = self.im2.resize((500, 250), resample=Image.Resampling.LANCZOS)
        self.im2 = ImageTk.PhotoImage(self.im2)

        self.lbl_im1 = Label(self.root, image= self.im2, bd= 2, relief=RAISED)
        self.lbl_im1.place(x=510, y=220, width=480)
        self.show()

#-------------FUNCTIONS------------------
    def add(self):
      con = sqlite3.connect(database='DatabaseProject.db')
      cur = con.cursor()
      try:
          if self.var_cat_name.get() == "":
              messagebox.showerror("Error","Category Name should be required", parent= self.root)
          else:
              cur.execute("Select * from category where name=?",(self.var_cat_name.get(),))
              row = cur.fetchone()
              if row != None:
                  messagebox.showerror("Error", "Category already present, try different", parent= self.root)
              else:
                  cur.execute("Insert into category (name) values(?)",(
                      self.var_cat_name.get(),
                  ))
                  con.commit()
                  messagebox.showinfo("Success", "Category added successfully", parent= self.root)
                  self.show()
      except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)

    def show(self):
        con = sqlite3.connect(database='DatabaseProject.db')
        cur = con.cursor()
        try:
            cur.execute("select * from category")
            rows = cur.fetchall()
            self.CateoryTable.delete(*self.CateoryTable.get_children())
            for row in rows:
                self.CateoryTable.insert('', END, values=row)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)

    def get_DATA(self, ev):
        try:
         f = self.CateoryTable.focus()
         content = self.CateoryTable.item(f)
         row = content['values']
         if row:
          self.var_cat_id.set(row[0])
          self.var_cat_name.set(row[1])
         else:
            messagebox.showerror("Error", "No data selected", parent=self.root)
        except Exception as ex:
         messagebox.showerror("Error", f"Error during data retrieval: {str(ex)}", parent=self.root)

    def delete(self):
         con = sqlite3.connect(database='DatabaseProject.db')
         cur = con.cursor()
         try:
            if self.var_cat_id.get() == "":
               messagebox.showerror("Error","Please select Category Name", parent= self.root)
            else:
               cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
               row = cur.fetchone()
               if row == None:
                  messagebox.showerror("Error", "Category Not Found", parent= self.root)
               else:
                  op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent = self.root)
                  if op == True:
                    cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                    con.commit()
                    messagebox.showinfo("Delete", "Category Deleted Successfully", parent= self.root)
                    self.show() 
                    self.var_cat_id.set("")   
                    self.var_cat_name.set("")     
         except Exception as ex:
             messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)     


if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
