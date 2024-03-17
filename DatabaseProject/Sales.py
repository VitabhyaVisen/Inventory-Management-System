import os
import sqlite3
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x500+200+130")
        self.root.title("Inventory Management System | Developed by Student")
        self.root.config(bg="white")
        self.root.focus_force()

        #---------VARIABLES---------------
        self.var_invoice = StringVar()
        self.bill_list = []

        #-------------TITLE---------------
        lbl_title = Label(self.root, text= "View Customer Bills", font= ("Times New Roman", 30,), bg= "#184a45", fg= "white").pack(side=TOP, fill=X, padx=10, pady=2)

        lbl_title = Label(self.root, text= "Invoice No.", font= ("Times New Roman", 15,), bg= "white").place(x=50, y= 100)
        txt_title = Entry(self.root, textvariable=self.var_invoice, font= ("Times New Roman", 15,), bg= "lightyellow").place(x=160, y= 100, width=180, height= 28)
        
        #--------BUTTONS----------
        btn_search = Button(self.root, text= "Search", command=self.search, font=("times new roman", 15, "bold"), bg= "#2196f3", fg= "white", cursor= "hand2").place(x=360, y=100, width=120, height=28)
        btn_clear = Button(self.root, text= "Clear", command=self.clear, font=("times new roman", 15, "bold"), bg= "lightgray", fg= "black", cursor= "hand2").place(x=490, y=100, width=120, height=28)

        #-------------SALES FRAME----------------
        sales_FRAME = Frame(self.root, bd=3, relief=RIDGE)
        sales_FRAME.place(x=50, y= 140, width=200, height=330)
        
        #-----------LIST-------------------
        scrolly = Scrollbar(sales_FRAME, orient= VERTICAL)
        self.sales_List = Listbox(sales_FRAME, font= ("goudy old style", 15), bg= "white", yscrollcommand=scrolly.set)
        scrolly.config(command=self.sales_List.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.sales_List.pack(fill=BOTH, expand=1)
        self.sales_List.bind("<ButtonRelease-1>", self.get_DATA)

        #----------BILL AREA-----------------
        bill_FRAME = Frame(self.root, bd=3, relief=RIDGE)
        bill_FRAME.place(x=280, y= 140, width=330, height=330)

        #-----------BILL-TITLE-----------------
        lbl_title = Label(bill_FRAME, text= "Customer Bill Area", font= ("Goudy old style", 20,), bg= "orange").pack(side=TOP, fill=X)


        scrolly2 = Scrollbar(bill_FRAME, orient= VERTICAL)
        self.bill_Area =Text(bill_FRAME, bg= "lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.config(command=self.bill_Area.yview)
        scrolly2.pack(side=RIGHT, fill=Y)
        self.bill_Area.pack(fill=BOTH, expand=1)

        #---------IMAGE-----------------

        self.bill_photo = Image.open("images/images/cat2.jpg")
        self.bill_photo = self.bill_photo.resize((400, 300),  Image.Resampling.LANCZOS)
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        lbl_image = Label(self.root, image= self.bill_photo, bd= 0)
        lbl_image.place(x=620, y=110)
         
        self.show()
#--------------------------------------------------------------------------------------------------
        
    def show(self):
        del self.bill_list[:]
        self.sales_List.delete(0, END)
        for i in os.listdir('bill'):
            if i.split('.')[-1] == 'txt':
                self.sales_List.insert(END, i)
                self.bill_list.append(i.split('.')[0])

    def get_DATA(self, ev):
        index_ = self.sales_List.curselection()
        file_name = self.sales_List.get(index_)
        # print(file_name)
        self.bill_Area.delete('1.0',END)
        fp = open(f'bill/{file_name}', 'r')
        for i in fp:
            self.bill_Area.insert(END,i)
        fp.close()

    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Invoice No. should be required", parent = self.root)    
        else:
            if self.var_invoice.get() in self.bill_list:
                fp = open(f'bill/{self.var_invoice.get()}.txt', 'r')
                self.bill_Area.delete('1.0',END)
                for i in fp:
                    self.bill_Area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error", "Invalid Invoice No.", parent = self.root) 
    
    def clear(self):
        self.show()
        self.bill_Area.delete('1.0', END)


if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
