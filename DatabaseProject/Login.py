from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
# import random
import time

class login_SYSTEM:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System | Developed by Students")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg= "#fafafa")

        self.OTP = ''
        self.cur = None
        

        #------------------IMAGES-------------------

        self.phone_IMAGE = ImageTk.PhotoImage(file= "images/images/phone.png")
        self.lbl_pHONE_IMAGE = Label(self.root, image= self.phone_IMAGE, bd=0).place(x=200, y=10)

        #----------------LOGIN FRAME---------------
        self.employeeID = StringVar()
        self.password = StringVar()

        login_FRAME = Frame(self.root, bd=2, relief=RIDGE, bg= "white")
        login_FRAME.place(x=650, y=50, width=350, height=460)

        title = Label(login_FRAME, text= "Login System", font= ("Times", 30, "bold"), bg= "white").place(x=0, y=30, relwidth=1)

        lbl_USER = Label(login_FRAME, text= "Employee Id:", font= ("Andulas", 15), bg= "white", fg= "#767171").place(x=50, y=100)
        

        txt_EMPLOYEE_ID = Entry(login_FRAME, textvariable= self.employeeID, font= ("times new roman", 15), bg= "#ECECEC").place(x=50, y=140, width=250)

        lbl_PASSWORD = Label(login_FRAME, text= "Password:", font= ("Andulas", 15), bg= "white", fg= "#767171").place(x=50, y=200)

        txt_PASSWORD = Entry(login_FRAME,  textvariable= self.password, show="*", font= ("times new roman", 15), bg= "#ECECEC").place(x=50, y=240, width=250)

        btn_LOGIN = Button(login_FRAME, text= "Log In", command= self.login, font= ("Arial Rounded MT Bold", 15), bg= "#00B0F0", cursor="hand2", activebackground="#00B0F0", fg="white", activeforeground="white").place(x=50, y=300, width=250, height=35)

        hr = Label(login_FRAME, bg= "lightgray").place(x=50, y=370, width=250, height=2)
        OR_ = Label(login_FRAME, text="OR", font=("times new roman", 15, "bold"), bg= "white", fg="lightgray").place(x=150, y=356)

        btn_forget_PASS = Button(login_FRAME, text= "Forget Password?", command=self.forget_window, font= ("times new roman", 13), bg= "white", cursor="hand2", fg="#00759E", bd=0, activebackground="white", activeforeground="#00759E" ).place(x=100, y=390)

        #----------------FRAME2-----------------

        register_FRAME = Frame(self.root, bd=2, relief=RIDGE, bg= "white")
        register_FRAME.place(x=650, y=530, width=350, height=60)

        lbl_REGISTER = Label(register_FRAME, text= "Don't have an account?", font= ("times new roman", 13), bg= "white").place(x=40, y=20)

        # btn_SIGN_UP = Button(register_FRAME, text= "Sign Up", font= ("times new roman", 13, "bold"), bg= "white", cursor="hand2", fg="#00759E", bd=0, activebackground="white", activeforeground="#00759E" ).place(x=200, y=17)

        #-----------------ANIMATION IMAGES-----------------

        self.im1 = ImageTk.PhotoImage(file="images/images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/images/im3.png")

        self.lbl_change_IMAGE = Label(self.root, bg="white")
        self.lbl_change_IMAGE.place(x=367, y=113, width=240, height=428)

        self.animate()
        


#-----------------------ALL FUNCTIONS-----------------------------
        
    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_IMAGE.config(image=self.im)
        self.lbl_change_IMAGE.after(2000, self.animate)


    def login(self):
         con = sqlite3.connect(database='DatabaseProject.db')
         cur = con.cursor()
         try:
            if self.employeeID.get()=="" or self.password.get()=="":
                messagebox.showerror('Error', "All fields are required", parent = self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?", (self.employeeID.get(), self.password.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror('Error', "Invalid Username or Password")
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python Dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python Billing.py")
         except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)

    def forget_window(self):
        con = sqlite3.connect(database='DatabaseProject.db')
        self.cur = con.cursor()
        try:
         if self.employeeID.get()=="":
            messagebox.showerror('Error', "Employee ID is required", parent = self.root)
         else:
             self.cur.execute("select email from employee where eid=? ", (self.employeeID.get(),))
             email = self.cur.fetchone()
             if email == None:
                messagebox.showerror('Error', "Invalid Employee ID\nTry Again")
             else:
                #------------FORGET WINDOW----------------
                 self.var_OTP = StringVar()
                 self.var_new_PASSWORD = StringVar()
                 self.var_conf_PASSWORD = StringVar()
                #  call_send_email_functions
                 
                 chk = self.send_EMAIL(email[0])
                 if chk == 'f':
                     messagebox.showerror('Error', "Connection Error, Try Again", parent = self.root)

                 else:
                     self.forget_win = Toplevel(self.root)
                     self.forget_win.title('RESET PASSWORD')
                     self.forget_win.geometry('400x350+500+100')
                     self.forget_win.focus_force()

                     title = Label(self.forget_win, text="Reset Pasword", font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white").pack(side=TOP,fill=X)

                     lbl_RESET = Label(self.forget_win, text="Enter OTP sent on registered email", font=("times new roman",15)).place(x=20,y=60)

                     txt_RESET = Entry(self.forget_win, textvariable= self.var_OTP, font=("times new roman",15), bg='lightyellow').place(x=20,y=100, width=250, height=30)

                     self.btn_RESET = Button(self.forget_win, text="SUBMIT", command= self.validate_OTP, font=("times new roman",15), bg='lightblue')
                     self.btn_RESET.place(x=280,y=100, width=100, height=30)

                     new_PASS = Label(self.forget_win, text="New Password", font=("times new roman",15)).place(x=20, y=160)
                     txt_new_PASS = Entry(self.forget_win, textvariable=self.var_new_PASSWORD, font=("times new roman",15), bg='lightyellow').place(x=20,y=190, width=250, height=30)

                     conf_PASS = Label(self.forget_win, text= "Confirm Pasword", font=("times new roman",15)).place(x=20, y=225)
                     txt_conf_PASS = Entry(self.forget_win, textvariable=self.var_conf_PASSWORD, font=("times new roman",15), bg='lightyellow').place(x=20,y=255, width=250, height=30)

                     self.btn_UPDATE = Button(self.forget_win, text="UPDATE", command= self.update_PASSWORD, font=("times new roman",15), bg='lightblue', state=DISABLED)
                     self.btn_UPDATE.place(x=150,y=300, width=100, height=30)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)

    def update_PASSWORD(self):
        if self.var_new_PASSWORD.get()=="" or self.var_conf_PASSWORD.get()=="":
            messagebox.showerror('Error', "Password is required", parent = self.forget_win)

        elif self.var_new_PASSWORD.get() != self.var_conf_PASSWORD.get():
            messagebox.showerror('Error', "New Password and Confirm Password should be same", parent = self.forget_win)

        else:
            self.con = sqlite3.connect(database='DatabaseProject.db')
            self.cur = self.con.cursor()
        try:
            self.cur.execute("Update employee SET pass=? where eid=?", (self.var_new_PASSWORD.get(), self.employeeID.get()))
            self.con.commit()
            messagebox.showinfo('Success', "Password Updated Successfully", parent = self.forget_win)
            self.forget_win.destroy()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent= self.root)
             
    def validate_OTP(self):
      try:
          user_input = self.var_OTP.get()
          if user_input == "":
             messagebox.showerror('Error', "Please enter the OTP first", parent=self.forget_win)
             return
          if int(self.OTP) == int(user_input):
             self.btn_UPDATE.config(state=NORMAL)
             self.btn_RESET.config(state=DISABLED)
          else:
             messagebox.showerror('Error', "Invalid OTP, Try Again", parent=self.forget_win)
      except ValueError:
             messagebox.showerror('Error', "Invalid OTP format, please enter digits only", parent=self.forget_win)

    def send_EMAIL(self,TO_):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        email_ = email_pass.email
        pass_ = email_pass.password

        s.login(email_, pass_)

        self.OTP = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))
        
        subj = 'IMS- Reset Password'
        msg_ = f'Dear Sir/Madam,\n\nYour Reset OTP is {str(self.OTP)}.\n\nWith Regards,\nIMS Team'
        msg = "Subject: {}\n\n{}".format(subj,msg_)
        s.sendmail(email_,TO_, msg)
        chk = s.ehlo()
        if chk[0] == 250:
            return 's'
        else:
            return 'f'


root = Tk()
obj = login_SYSTEM(root)
root.mainloop()
