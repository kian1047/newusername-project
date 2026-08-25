import tkinter as tk
from tkinter import ttk,messagebox
from manager import InventoryManager


class Loginwindow:
    def __init__(self,root,on_success):
        self.root = root
        self.on_success = on_success
        self.manager = InventoryManager()


        self.root.title("-_-_LOGIN_-_-")
        self.root.geometry("800x600")

        frame = ttk.Frame(root,padding=20)
        frame.grid(row=0,column=0,sticky="nsew")

        self.username_L = ttk.Label(frame,text="Username:",font=("Tempus Sans ITC",11,"bold"))
        self.username_L.grid(row=0,column=0,sticky=tk.W,pady=5)

        self.username_E = ttk.Entry (frame,width=30)
        self.username_E.grid(row=0,column=1,pady=5)

        self.password_L = ttk.Label(frame,text="Password:",font=("Tempus Sans ITC",11,"bold"))
        self.password_L.grid(row=1,column=0,sticky=tk.W,pady=5)

        self.password_E = ttk.Entry (frame,width=30)
        self.password_E.grid(row=1,column=1,pady=5)

        self.login_B = ttk.Button(frame,text="LOGIN",command=self.login)
        self.login_B.grid(row=2,column=1,pady=8)

    def login(self):
        username = self.username_E.get().strip()
        password = self.password_E.get().strip()
        user = self.manager.authen(username,password)
        if user:
            self.root.destroy()
            self.on_success(user)
        else:
            messagebox.showerror("LOGIN 💥ERROR💥","INVALID USERNAME OR PASSWORD🔒")

class MainApp:
    def __init__(self,user):
        self.user = user
        self.manager = InventoryManager()

        self.root = tk.Tk()
        self.root.title(f"Inventory System - {user.username} ({user.role})")
        self.root.geometry("1600x1200")

        self.create_widgets()
        self.root.mainloop()



    def create_widgets(self):
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_rowconfigure(1,weight=1)

        top = ttk.Frame(self.root)
        top.grid(row=0,column=0,sticky="we" , padx=11)


        self.loggin_label = ttk.Label(top, text=f"logged in as {self.user.username}({self.user.role})", font=("Tempus Sans ITC",11,"bold"))
        self.loggin_label.pack(side="left",padx=11)

        self.log_button = ttk.Button(top,text="LOGOUT👍",command=self.logout, )
        self.log_button.pack(side="right",padx=11)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1,column=0, sticky="nsew",padx=11,pady=5)

        self.item_frame = ttk.Frame(self.notebook, relief="sunken")
        self.item_frame.grid(row=0,column=0)

        self.notebook.add(self.item_frame,text="item")
        self.Create_items()

        if self.user.role == "admin":
            self.user_frame = ttk.Frame(self.notebook, relief="sunken")
            self.notebook.add(self.user_frame, text="User")

    def Create_items(self):
        self.item_frame.grid_columnconfigure(0,weight=1)
        self.item_frame.grid_rowconfigure(0,weight=1)

        tree_frame = ttk.Frame(self.item_frame)
        tree_frame.grid(row=0,column=0,sticky="nsew",padx=5,pady=5)

        columns= ("Name","Quantity","Price","category")
        self.tree = ttk.Treeview(tree_frame,columns=columns,show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Name": self.tree.column(col,width=200)
            elif col == "Quantity": self.tree.column(col,width=80)
            elif col == "Price": self.tree.column(col,width=80)
            elif col == "Category": self.tree.column(col,width=200)
        tree_frame.grid_columnconfigure(0,weight=1)
        tree_frame.grid_rowconfigure(0,weight=1)
        self.tree.grid(row=0,column=0,sticky="nsew")

        self.refresh_items()
    def refresh_items(self):
        for row in self.tree.get_children():
            self.tree.delete()
        for item in self.manager.get_items():
            self.tree.insert("",tk.END , values=[item["Name"],item["Quantity"],item["Price"],item["Category"]])
def logout(self):
        self.manager.close()
        self.root.destroy()
        log_root = tk.Tk()
        Loginwindow(log_root,lambda u:MainApp(u))
        log_root.mainloop()        
class AddItemDialog:
    def __init__(self,parent,manager,refresh):
        self.manager = manager
        self.refresh = refresh

        self.window = tk.Toplevel(parent)
        self.window.title("Add Item")
        self.window.geometry("480x360")

        freame = ttk.Frame(self.window, padding=15)
        freame.pack(fill=tk.BOTH,expand=True)

        name_label = ttk.Label(freame,text="Name")
        name_label.grid(row=0,column=0,sticky="w",pady=10)

        name_entry = ttk.Entry(freame,width=30)
        name_entry.grid(row=0,column=1,sticky="w",pady=10)

        quantity_label = ttk.Label(freame,text="Quantity")
        quantity_label.grid(row=1,column=1,sticky="w",pady=10)

        quantity_entry = ttk.Entry(freame,width=30)
        quantity_entry.grid(row=1,column=1,sticky="w",pady=10)

        price_label = ttk.Label(freame,text="Price")
        price_label.grid(row=2,column=1,sticky="w",pady=10)

        price_entry = ttk.Entry(freame,width=30)
        price_entry.grid(row=2,column=1,sticky="w",pady=10)

        category_label = ttk.Label(freame,text="Category")
        category_label.grid(row=3,column=1,sticky="w",pady=10)

        category_entry = ttk.Entry(freame,width=30)
        category_entry.grid(row=3,column=1,sticky="w",pady=10)

        self.add_button = ttk.Button(freame,text="ADD ITEM",command=self.add_item)
        self.add_button.pack(side="right",padx=11)
if __name__=="__main__":
    root = tk.Tk()
    Loginwindow(root,lambda u:MainApp(u))
    root.mainloop()