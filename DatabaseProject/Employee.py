import sqlite3
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox

class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x500+200+130")
        self.root.title("Inventory Management System | Developed by Student")
        self.root.config(bg="white")
        self.root.focus_force()

        #------------------ALL VARIABLE---------------
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_emp_name = StringVar()
        self.var_emp_contact = StringVar()
        self.var_emp_gender = StringVar()
        self.var_emp_dob = StringVar()
        self.var_emp_doj = StringVar()
        self.var_emp_email = StringVar()
        self.var_emp_pass = StringVar()
        self.var_emp_utype = StringVar()
        self.var_emp_salary = StringVar()

        # -----------------SEARCH FRAME---------------
        SearchFrame = LabelFrame(self.root, text="Search Employee", font=("Helvetica", 12, "bold"), bg="white", fg="black")
        SearchFrame.place(x=200, y=20, width=600, height=70)

        #--------------------OPTIONS------------------
        cmb_search = ttk.Combobox(SearchFrame, textvariable= self.var_searchby, values=("Select", "Email", "Name", "eid"), state="readonly", justify=CENTER, font=("TkDefaultFont", 10))
        cmb_search.place(x=10, y=10, width=180,)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable= self.var_searchtxt, font=("Helvetica", 11), bg="light yellow").place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", command= self.search, font=("Helvetica", 10),bg="#98FB98", fg="#36454F", cursor="hand2").place(x=370, y=8, width=150, height=25)

        #------------------TITLE------------------------
        title = Label(self.root, text= "Employee Details", font=("Palatino Linotype", 16, "bold"), bg="teal", fg="#FFFDD0").place(x=50, y=100, width=900)

        #------------------CONTENT----------------------

        #------------------ROW-1------------------------
        lbl_empid = Label(self.root, text= "Employee Id", font=("Trebuchet MS", 12), bg="white").place(x=50, y=150) 
        lbl_gender = Label(self.root, text= "Gender", font=("Trebuchet MS", 12), bg="white").place(x=350, y=150)
        lbl_contact = Label(self.root, text= "Contact", font=("Trebuchet MS", 12), bg="white").place(x=650, y=150)

        txt_empid = Entry(self.root, textvariable= self.var_emp_id, font=("calibri", 12), bg="lightyellow").place(x=175, y=150, width=160) 
        cmb_gender = ttk.Combobox(self.root, textvariable= self.var_emp_gender, values=("Select", "Male", "Female", "Others"), state="readonly", justify=CENTER, font=("TkDefaultFont", 10))
        cmb_gender.place(x=430, y=150, width=160)
        cmb_gender.current(0)
        txt_contact = Entry(self.root, textvariable= self.var_emp_contact , font=("calibri", 12), bg="lightyellow").place(x=735, y=150, width=150)

        #------------------ROW-2-----------------------
        lbl_name = Label(self.root, text= "Name", font=("Trebuchet MS", 12), bg="white").place(x=50, y=190) 
        lbl_dob = Label(self.root, text= "D.O.B", font=("Trebuchet MS", 12), bg="white").place(x=350, y=190)
        lbl_doj = Label(self.root, text= "D.O.J", font=("Trebuchet MS", 12), bg="white").place(x=650, y=190)

        txt_name = Entry(self.root, textvariable= self.var_emp_name, font=("calibri", 12), bg="lightyellow").place(x=175, y=190, width=160) 
        txt_dob = Entry(self.root, textvariable= self.var_emp_dob, font=("calibri", 12), bg="lightyellow").place(x=430, y=190, width=160)
        txt_doj = Entry(self.root, textvariable= self.var_emp_doj, font=("calibri", 12), bg="lightyellow").place(x=735, y=190, width=150)

        #------------------ROW-3-----------------------
        lbl_email = Label(self.root, text= "Email", font=("Trebuchet MS", 12), bg="white").place(x=50, y=230) 
        lbl_pass = Label(self.root, text= "Password", font=("Trebuchet MS", 12), bg="white").place(x=350, y=230)
        lbl_utype = Label(self.root, text= "User Type", font=("Trebuchet MS", 12), bg="white").place(x=650, y=230)

        txt_email = Entry(self.root, textvariable= self.var_emp_email, font=("calibri", 12), bg="lightyellow").place(x=175, y=230, width=160) 
        txt_pass = Entry(self.root, textvariable= self.var_emp_pass, font=("calibri", 12), bg="lightyellow").place(x=430, y=230, width=160)
        cmb_utype = ttk.Combobox(self.root, textvariable= self.var_emp_utype, values=("Select","Admin", "Employee"), state="readonly", justify=CENTER, font=("TkDefaultFont", 10))
        cmb_utype.place(x=735, y=230, width=150)
        cmb_utype.current(0)

        #-----------------ROW-4------------------------
        lbl_address = Label(self.root, text= "Address", font=("Trebuchet MS", 12), bg="white").place(x=50, y=270) 
        lbl_salary = Label(self.root, text= "Salary", font=("Trebuchet MS", 12), bg="white").place(x=500, y=270)

        self.txt_address = Text(self.root, font=("calibri", 12), bg="lightyellow")
        self.txt_address.place(x=175, y=270, width=300, height=60) 
        txt_salary = Entry(self.root, textvariable= self.var_emp_salary, font=("calibri", 12), bg="lightyellow").place(x=600, y=270, width=160)

        #-----------------BUTTONS---------------------
        btn_save = Button(self.root, text="Save", command=self.add, font=("Helvetica", 10),bg="#4682B4", fg="#FFFFFF", cursor="hand2").place(x=500, y=305, width=110, height=28)
        btn_update = Button(self.root, text="Update", command= self.update, font=("Helvetica", 10),bg="#4caf50", fg="#FFFFFF", cursor="hand2").place(x=620, y=305, width=110, height=28)        
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("Helvetica", 10),bg="#FF4500", fg="#FFFFFF", cursor="hand2").place(x=740, y=305, width=110, height=28) 
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("Helvetica", 10),bg="#607d8b", fg="#FFFFFF", cursor="hand2").place(x=860, y=305, width=110, height=28)        

        #----------------EMPLOYEE DETAILS FRAME-------------
        emp_FRAME = Frame(self.root, bd=3, relief=RIDGE)
        emp_FRAME.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(emp_FRAME, orient= VERTICAL)
        scrollx = Scrollbar(emp_FRAME, orient= HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_FRAME, columns= ("eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"), yscrollcommand= scrolly.set, xscrollcommand= scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid", text= "Employee Id")
        self.EmployeeTable.heading("name", text= "Name")
        self.EmployeeTable.heading("email", text= "Email")
        self.EmployeeTable.heading("gender", text= "Gender")
        self.EmployeeTable.heading("contact", text= "Contact")
        self.EmployeeTable.heading("dob", text= "D.O.B")
        self.EmployeeTable.heading("doj", text= "D.O.J")
        self.EmployeeTable.heading("pass", text= "Password")
        self.EmployeeTable.heading("utype", text= "User Type")
        self.EmployeeTable.heading("address", text= "Address")
        self.EmployeeTable.heading("salary", text= "Salary")

        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.column("eid", width= 90)
        self.EmployeeTable.column("name", width= 100)
        self.EmployeeTable.column("email", width= 100)
        self.EmployeeTable.column("gender", width= 100)
        self.EmployeeTable.column("contact", width= 100)
        self.EmployeeTable.column("dob", width= 100)
        self.EmployeeTable.column("doj", width= 100)
        self.EmployeeTable.column("pass", width= 100)
        self.EmployeeTable.column("utype", width= 100)
        self.EmployeeTable.column("address", width= 100)
        self.EmployeeTable.column("salary", width= 100)

        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_DATA)
        self.show()
# -------------------------------------------------------------------------------------------------------------------
    def add(self):
      con = sqlite3.connect(database='DatabaseProject.db')
      cur = con.cursor()
      try:
          if self.var_emp_id.get() == "":
              messagebox.showerror("Error","Employee Id must be required", parent= self.root)
          else:
              cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
              row = cur.fetchone()
              if row != None:
                  messagebox.showerror("Error", "This Employee Id is already assigned, try different", parent= self.root)
              else:
                  cur.execute("Insert into employee (eid, name, email, gender, contact, dob, doj, pass, utype, address, salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                      self.var_emp_id.get(),
                      self.var_emp_name.get(),
                      self.var_emp_email.get(),
                      self.var_emp_gender.get(),
                      self.var_emp_contact.get(),
                      self.var_emp_dob.get(),
                      self.var_emp_doj.get(),
                      self.var_emp_pass.get(),
                      self.var_emp_utype.get(),
                      self.txt_address.get('1.0',END),
                      self.var_emp_salary.get()
                  ))
                  con.commit()
                  messagebox.showinfo("Success", "Employee added successfully", parent= self.root)
                  self.show()
      except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)

    def show(self):
        con = sqlite3.connect(database='DatabaseProject.db')
        cur = con.cursor()
        try:
            cur.execute("select * from employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)


    def get_DATA(self, ev):
     try:
        f = self.EmployeeTable.focus()
        content = self.EmployeeTable.item(f)
        row = content['values']
        if row:
            self.var_emp_id.set(row[0])
            self.var_emp_name.set(row[1])
            self.var_emp_email.set(row[2])
            self.var_emp_gender.set(row[3])
            self.var_emp_contact.set(row[4])
            self.var_emp_dob.set(row[5])
            self.var_emp_doj.set(row[6])
            self.var_emp_pass.set(row[7])
            self.var_emp_utype.set(row[8])
            self.txt_address.delete('1.0', END)
            self.txt_address.insert(END, row[9])
            self.var_emp_salary.set(row[10])
        else:
            messagebox.showerror("Error", "No data selected", parent=self.root)
     except Exception as ex:
        messagebox.showerror("Error", f"Error during data retrieval: {str(ex)}", parent=self.root)




    def update(self):
      con = sqlite3.connect(database='DatabaseProject.db')
      cur = con.cursor()
      try:
          if self.var_emp_id.get() == "":
              messagebox.showerror("Error","Employee Id must be required", parent= self.root)
          else:
              cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
              row = cur.fetchone()
              if row == None:
                  messagebox.showerror("Error", "Invalid Employee Id", parent= self.root)
              else:
                  cur.execute("Update employee set name=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?, utype=?, address=?, salary=? where eid=?",(
                      self.var_emp_name.get(),
                      self.var_emp_email.get(),
                      self.var_emp_gender.get(),
                      self.var_emp_contact.get(),
                      self.var_emp_dob.get(),
                      self.var_emp_doj.get(),
                      self.var_emp_pass.get(),
                      self.var_emp_utype.get(),
                      self.txt_address.get('1.0',END),
                      self.var_emp_salary.get(),
                      self.var_emp_id.get()
                  ))
                  con.commit()
                  messagebox.showinfo("Success", "Employee updated successfully", parent= self.root)
                  self.show()
      except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)        
    

    def delete(self):
         con = sqlite3.connect(database='DatabaseProject.db')
         cur = con.cursor()
         try:
              if self.var_emp_id.get() == "":
               messagebox.showerror("Error","Employee Id must be required", parent= self.root)
              else:
               cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
              row = cur.fetchone()
              if row == None:
                  messagebox.showerror("Error", "Invalid Employee Id", parent= self.root)
              else:
                  op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent = self.root)
                  if op == True:
                    cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                    con.commit()
                    messagebox.showinfo("Delete", "Employee Deleted Successfully", parent= self.root)
                  self.clear()         
         except Exception as ex:
             messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)
    

    def clear(self):
        self.var_emp_id.set("")
        self.var_emp_name.set("")
        self.var_emp_email.set("")
        self.var_emp_gender.set("Select")
        self.var_emp_contact.set("")
        self.var_emp_dob.set("")
        self.var_emp_doj.set("")
        self.var_emp_pass.set("")
        self.var_emp_utype.set("Admin")
        self.txt_address.delete('1.0', END)
        self.var_emp_salary.set("")
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
             cur.execute("select * from employee where " + self.var_searchby.get()+" LIKE '%" + self.var_searchtxt.get()+"%'")
             rows = cur.fetchall()
             if len(rows) != 0:
               self.EmployeeTable.delete(*self.EmployeeTable.get_children())
               for row in rows:
                 self.EmployeeTable.insert('', END, values=row)
             else:
                messagebox.showerror("Error", "No Record Found", parent= self.root)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)



if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()
