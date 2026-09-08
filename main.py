import tkinter as tk
from tkinter import ttk,messagebox
from manager import InventoryManager
from .models import Item , User


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

        self.log_button = ttk.Button(top,text="LOGOUT👍",command=self.logout )
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
            self.Create_users()

    def Create_items(self):
        self.item_frame.grid_columnconfigure(0,weight=1)
        self.item_frame.grid_rowconfigure(0,weight=1)
        self.item_frame.grid_rowconfigure(1,weight=5)

        top_frame= ttk.Frame(self.item_frame,relief="sunken")
        top_frame.grid(row=0,column=0,sticky="ew",padx=5,pady=5)

        self.item_button = ttk.Button(top_frame,text="ADD ITEM🖊",command=self.add_item )
        self.item_button.pack(side="right",padx=11,pady=11)

        self.edit_item = ttk.Button(top_frame,text="EDIT ITEM🎬",command=self.edit_item )
        self.edit_item.pack(side="right",padx=11,pady=11)

        self.delete_item_button = ttk.Button(top_frame,text="DELETE ITEM 🗑",command=self.delete_item )
        self.delete_item_button.pack(side="right",padx=11,pady=11)

        self.search_label = ttk.Label(top_frame,text="SEARCH📂")
        self.search_label.pack(side=tk.LEFT,padx=2)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write",lambda *args : self.on_item_search())
        search_entry =ttk.Entry(top_frame,textvariable=self.search_var,)
        search_entry.pack(side=tk.LEFT,padx=3)

        tree_frame = ttk.Frame(self.item_frame)
        tree_frame.grid(row=1,column=0,sticky="nsew",padx=5,pady=5)

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
    def refresh_items(self,items=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if items is None:
            items = self.manager.get_items()
        for item in items:
            self.tree.insert("",tk.END ,iid= item["id"] ,values=[item["name"],item["quantity"],item["price"],item["category"]])
        
    def logout(self):
        self.manager.close()
        self.root.destroy()
        log_root = tk.Tk()
        Loginwindow(log_root,lambda u:MainApp(u))
        log_root.mainloop()   

    def add_item(self):
        AddItemDialog(self.root,self.manager,self.refresh_items)  
    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("no selection📌","please select an item first🎬")
            return
        item_id= int(selected[0].replace("I","0"))
        if messagebox.askyesno("confrim delete👓","R U sure🗿?"):
            self.manager.delete_item(item_id)
            self.refresh_items()

    def edit_item(self):
        selected  = self.tree.selection()
        if not selected:
            messagebox.showerror("no selection📌","please select an item first🎬")
            return
        item_id= int(selected[0])
        all_items=self.manager.get_items()
        item = next((i for i in all_items if i["id"]== item_id), None)
        if item:
            UpdateItem(self.root,self.manager,item,self.refresh_items)

    def on_item_search(self):
        keyword = self.search_var.get().strip().lower()
        if not keyword:
            self.refresh_items
        else:
            all_items =self.manager.get_items()
            filtered = [i for i in all_items if keyword in i["name"].lower() or keyword in i["category"].lower()] 
            self.refresh_items(filtered)
    def Create_users(self):
        self.user_frame.grid_columnconfigure(0,weight=1)
        self.user_frame.grid_rowconfigure(0,weight=1)
        self.user_frame.grid_rowconfigure(1,weight=5)

        top_frame= ttk.Frame(self.user_frame,relief="sunken")
        top_frame.grid(row=0,column=0,sticky="ew",padx=5,pady=5)

        self.user_button = ttk.Button(top_frame,text="ADD USER🖊",command=self.add_user )
        self.item_button.pack(side="right",padx=11,pady=11)

        self.edit_user = ttk.Button(top_frame,text="EDIT USER🎬",command=self.edit_user )
        self.edit_user.pack(side="right",padx=11,pady=11)

        self.delete_user_button = ttk.Button(top_frame,text="DELETE USER🗑",command=self.delete_user )
        self.delete_user_button.pack(side="right",padx=11,pady=11)

        self.search_label = ttk.Label(top_frame,text="SEARCH📂")
        self.search_label.pack(side=tk.LEFT,padx=2)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write",lambda *args : self.on_user_search())
        search_entry = ttk.Entry(top_frame,textvariable=self.search_var,width=25)
        search_entry.pack(side=tk.LEFT,padx=3)

        tree_frame = ttk.Frame(self.user_frame)
        tree_frame.grid(row=1,column=0,sticky="nsew",padx=5,pady=5)

        columns= ("ID","UserName","Role")
        self.tree = ttk.Treeview(tree_frame,columns=columns,show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID": self.tree.column(col,width=200)
            elif col == "Username": self.tree.column(col,width=80)
            elif col == "Role": self.tree.column(col,width=80)
        tree_frame.grid_columnconfigure(0,weight=1)
        tree_frame.grid_rowconfigure(0,weight=1)
        self.tree.grid(row=0,column=0,sticky="nsew")

        self.refresh_users()
    def refresh_users(self,users=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if users is None:
            users = self.manager.get_users()
        for item in users:
            self.tree.insert("",tk.END ,iid= users["id"] ,values=[users["id"],users["username"],users["role"]])
        
    # def logout(self):
    #     self.manager.close()
    #     self.root.destroy()
    #     log_root = tk.Tk()
    #     Loginwindow(log_root,lambda u:MainApp(u))
    #     log_root.mainloop()   

    def add_user(self):
        AddUserDialog(self.root,self.manager,self.refresh_users)  
    def delete_users(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("no selection📌","please select an user first🎬")
            return
        user_id= int(selected[0].replace("I","0"))
        if messagebox.askyesno("confrim delete👓","R U sure🗿?"):
            self.manager.delete_item(user_id)
            self.refresh_users()

    def edit_user(self):
        selected  = self.tree.selection()
        if not selected:
            messagebox.showerror("no selection📌","please select an user first🎬")
            return
        user_id= int(selected[0])
        all_user=self.manager.get_users()
        user = next((i for i in all_user if i["id"]== user_id), None)
        if user:
            AddItemDialog(self.root,self.manager,user,self.refresh_users)

    def on_user_search(self):
        keyword = self.search_var.get().strip().lower()
        if not keyword:
            self.refresh_users()
        else:
            all_users =self.manager.get_users()
            filtered = [i for i in all_users if keyword in i["username"].lower() or keyword in i["role"].lower()] 
            self.refresh_users(filtered)
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

        self.name_entry = ttk.Entry(freame,width=30)
        self.name_entry.grid(row=0,column=1,sticky="w",pady=10)

        quantity_label = ttk.Label(freame,text="Quantity")
        quantity_label.grid(row=1,column=0,sticky="w",pady=10)

        self.quantity_entry = ttk.Entry(freame,width=30)
        self.quantity_entry.grid(row=1,column=1,sticky="w",pady=10)

        price_label = ttk.Label(freame,text="Price")
        price_label.grid(row=2,column=0,sticky="w",pady=10)

        self.price_entry = ttk.Entry(freame,width=30)
        self.price_entry.grid(row=2,column=1,sticky="w",pady=10)

        category_label = ttk.Label(freame,text="Category")
        category_label.grid(row=3,column=0,sticky="w",pady=10)

        self.category_entry = ttk.Entry(freame,width=30)
        self.category_entry.grid(row=3,column=1,sticky="w",pady=10)

        self.save_botton = ttk.Button(freame,text="Save🖱🗓",command=self.save)
        self.save_botton.grid(row=4,column=1,pady=10)

    def save(self):
        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()
        category = self.category_entry.get().strip()

        if not name:
            messagebox.showerror("Required 💥ERROR💥","the name is required🙀")
            return
        try:
            quantity=float(quantity)if quantity else 0
            price = float(price)if price else 0
        except ValueError:
            messagebox.showerror("convert 💥ERROR💥","the quantity and price should be number🔢")
            
        item = Item(name,quantity,price,category)
        self.manager.add_item(item)
        self.refresh()
        self.window.destroy()

class UpdateItem:
    def __init__(self,parent,manager,item_data,refresh):
        self.manager = manager
        self.refresh = refresh
        self.item_data = item_data

        self.window = tk.Toplevel(parent)
        self.window.title("Edit Item")
        self.window.geometry("480x360")


        frame = ttk.Frame(self.window,padding=15)
        frame.pack(fill=tk.BOTH, expand=True)


        name_label = ttk.Label(frame,text="Name")
        name_label.grid(row=0,column=0,sticky="w",pady=10)
        self.name_var= tk.StringVar(value=item_data["name"])

        self.name_entry = ttk.Entry(frame,textvariable=self.name_var,width=30)
        self.name_entry.grid(row=0,column=1,sticky="w",pady=10)

        quantity_label = ttk.Label(frame,text="Quantity")
        quantity_label.grid(row=1,column=0,sticky="w",pady=10)
        self.quantity_var= tk.StringVar(value=item_data["quantity"])
        

        self.quantity_entry = ttk.Entry(frame,textvariable=self.quantity_var,width=30)
        self.quantity_entry.grid(row=1,column=1,sticky="w",pady=10)

        price_label = ttk.Label(frame,text="Price")
        price_label.grid(row=2,column=0,sticky="w",pady=10)
        self.price_var= tk.StringVar(value=item_data["price"])
        

        self.price_entry = ttk.Entry(frame,textvariable=self.price_var,width=30)
        self.price_entry.grid(row=2,column=1,sticky="w",pady=10)

        category_label = ttk.Label(frame,text="Category")
        category_label.grid(row=3,column=0,sticky="w",pady=10)
        self.category_var= tk.StringVar(value=item_data["category"])
        

        self.category_entry = ttk.Entry(frame,textvariable=self.category_var,width=30)
        self.category_entry.grid(row=3,column=1,sticky="w",pady=10)

        self.save_edit = ttk.Button(frame,text="♻SAVE EDITING♻" ,command=self.save)
        self.save_edit.grid(row=4,column=1,pady=15,sticky="news")

        self.edit = ttk.Button(frame,text="🚭EDIT ITEM🚭" ,command=self.edit_item)
        self.edit.grid(row=5,column=1,pady=5,sticky="news")

    def save(self):
        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()
        category = self.category_entry.get().strip()
        if not name:
            messagebox.showerror("Required 💥ERROR💥","the name is required🙀")
            return
        try:
            quantity=float(quantity)if quantity else 0
            price = float(price)if price else 0
        except ValueError:
            messagebox.showerror("convert 💥ERROR💥","the quantity and price should be number🔢")
            
        self.manager.update_item(self.item_data["id"],name,quantity,price,category)
        self.refresh()
        self.window.destroy()

class AddUserDialog:
    def __init__(self,parent,manager,refresh):
        self.manager = manager
        self.refresh = refresh

        self.window = tk.Toplevel(parent)
        self.window.title("Add User")
        self.window.geometry("480x360")

        freame = ttk.Frame(self.window, padding=15)
        freame.pack(fill=tk.BOTH,expand=True)

        username_label = ttk.Label(freame,text="UserName🎃")
        username_label.grid(row=0,column=0,sticky="w",pady=10)

        self.username_entry = ttk.Entry(freame,width=30)
        self.username_entry.grid(row=0,column=1,sticky="w",pady=10)

        password_label = ttk.Label(freame,text="Password🗝🔒")
        password_label.grid(row=1,column=0,sticky="w",pady=10)

        self.password_entry = ttk.Entry(freame,width=30)
        self.password_entry.grid(row=1,column=1,sticky="w",pady=10)

        role_label = ttk.Label(freame,text="Role🎭")
        role_label.grid(row=2,column=0,sticky="w",pady=10)

        self.role_entry = ttk.Entry(freame,width=30)
        self.role_entry.grid(row=2,column=1,sticky="w",pady=10)


        self.save_botton = ttk.Button(freame,text="Save🖱🗓",command=self.save)
        self.save_botton.grid(row=4,column=1,pady=10)

    def save(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Required 💥ERROR💥","the username or password are required🙀")
            return
        try:
            self.manager.add_user(username,password,role)
            self.refresh()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("💥ERROR💥",e)
            
        user = User(username,password,role)
        self.manager.add_user(user)
        self.refresh()
        self.window.destroy()

class UpdateUser:
    def __init__(self,parent,manager,user_data,refresh):
        self.manager = manager
        self.refresh = refresh
        self.user_data = user_data

        self.window = tk.Toplevel(parent)
        self.window.title("Edit User")
        self.window.geometry("480x360")


        frame = ttk.Frame(self.window,padding=15)
        frame.pack(fill=tk.BOTH, expand=True)


        username_label = ttk.Label(frame,text="UserName👓")
        username_label.grid(row=0,column=0,sticky="w",pady=10)
        self.usename_var= tk.StringVar(value=user_data["username"])

        self.name_entry = ttk.Entry(frame,textvariable=self.usename_var,width=30)
        self.name_entry.grid(row=0,column=1,sticky="w",pady=10)

        quantity_label = ttk.Label(frame,text="Quantity")
        quantity_label.grid(row=1,column=0,sticky="w",pady=10)
        self.quantity_var= tk.StringVar(value=user_data["quantity"])
        

        self.quantity_entry = ttk.Entry(frame,textvariable=self.quantity_var,width=30)
        self.quantity_entry.grid(row=1,column=1,sticky="w",pady=10)

        price_label = ttk.Label(frame,text="Price")
        price_label.grid(row=2,column=0,sticky="w",pady=10)
        self.price_var= tk.StringVar(value=user_data["price"])
        

        self.price_entry = ttk.Entry(frame,textvariable=self.price_var,width=30)
        self.price_entry.grid(row=2,column=1,sticky="w",pady=10)

        category_label = ttk.Label(frame,text="Category")
        category_label.grid(row=3,column=0,sticky="w",pady=10)
        self.category_var= tk.StringVar(value=user_data["category"])
        

        self.category_entry = ttk.Entry(frame,textvariable=self.category_var,width=30)
        self.category_entry.grid(row=3,column=1,sticky="w",pady=10)

        self.save_edit = ttk.Button(frame,text="♻SAVE EDITING♻" ,command=self.save)
        self.save_edit.grid(row=4,column=1,pady=15,sticky="news")

        self.edit = ttk.Button(frame,text="🚭EDIT ITEM🚭" ,command=self.edit_item)
        self.edit.grid(row=5,column=1,pady=5,sticky="news")

    def save(self):
        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()
        category = self.category_entry.get().strip()
        if not name:
            messagebox.showerror("Required 💥ERROR💥","the name is required🙀")
            return
        try:
            quantity=float(quantity)if quantity else 0
            price = float(price)if price else 0
        except ValueError:
            messagebox.showerror("convert 💥ERROR💥","the quantity and price should be number🔢")
            self.manager.update_item(self.item_data["id"],name,quantity,price,category)
            self.refresh()
            self.window.destroy()



if __name__=="__main__":
    root = tk.Tk()
    Loginwindow(root,lambda u:MainApp(u))
    root.mainloop()