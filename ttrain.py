import tkinter as tk
from tkinter import ttk, messagebox
from modules.manager import InvetoryManager
from modules.models import User, Item

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.manager = InvetoryManager()

        self.root.title("LOGIN")
        self.root.geometry("800x600")

        frame = ttk.Frame(root, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        self.username_label = ttk.Label(frame, text="Username:")
        self.username_label.grid(row=0, column=0, sticky=tk.W, pady=2)

        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=2)

        self.password_label = ttk.Label(frame, text="Password:")
        self.password_label.grid(row=1, column=0, sticky=tk.W, pady=2)

        self.password_entry = ttk.Entry(frame, width=30)
        self.password_entry.grid(row=1, column=1, pady=2)

        self.login_button = ttk.Button(frame, text="LOGIN", command=self.login)
        self.login_button.grid(row=2, column=1, pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user = self.manager.authenticate(username, password)
        if user:
            self.root.destroy()
            self.on_success(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


class MainApp:
    def __init__(self, user):
        self.user = user
        self.manager = InvetoryManager()

        self.root = tk.Tk()
        self.root.title(f"Inventoy System - {user.username} ({user.role})")
        self.root.geometry("1600x1200")

        self.create_widgets()
        self.root.mainloop()

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def create_widgets(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        top = ttk.Frame(self.root)
        top.grid(row=0, column=0, sticky="we", pady=5)

        self.logged_in_label = ttk.Label(top, text=f"Logged in as {self.user.username} ({self.user.role})", font=("TkDefaultFont", 12, "bold"))
        self.logged_in_label.pack(side=tk.LEFT, padx=20)

        self.logout_button = ttk.Button(top, text="LOGOUT", command=self.logout)
        self.logout_button.pack(side=tk.RIGHT, padx=20)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=20)

        self.items_frame = ttk.Frame(self.notebook, relief="sunken")
        self.items_frame.grid(row=0, column=0)

        self.notebook.add(self.items_frame, text="Items")
        self.create_items_tab()

        if self.user.role == "admin":
            self.users_frame = ttk.Frame(self.notebook, relief="sunken")
            self.notebook.add(self.users_frame, text="users")

    def create_items_tab(self):

        self.items_frame.grid_columnconfigure(0, weight=1)
        self.items_frame.grid_rowconfigure(0, weight=1)
        self.items_frame.grid_rowconfigure(1, weight=8)

        top = ttk.Frame(self.items_frame)
        top.grid(row=0, column=0, sticky="ew", padx=5)

        self.add_item_button = ttk.Button(top, text="Add Item", command=self.add_item)
        self.add_item_button.pack(side=tk.RIGHT, padx=20)

        self.delete_item_button = ttk.Button(top, text="Delete Item", command=self.delete_item)
        self.delete_item_button.pack(side=tk.RIGHT, padx=20)

        tree_frame = ttk.Frame(self.items_frame)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        columns = ("Name", "Qunatity", "Price", "Category")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Name": self.tree.column(col, width=200, anchor="center")
            elif col == "Qunatity": self.tree.column(col, width=80, anchor="center")
            elif col == "Price": self.tree.column(col, width=80, anchor="center")
            elif col == "Category": self.tree.column(col, width=200, anchor="center")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree.grid(row=0, column=0, sticky="nsew")

        self.refresh_items()

    def refresh_items(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.manager.get_all_items():
            self.tree.insert("", tk.END, iid=item["id"], values=(item["name"], item["quantity"], item["price"], item["category"]))

    def logout(self):
        self.manager.close()
        self.root.destroy()
        loging_root = tk.Tk()
        LoginWindow(loging_root, lambda u : MainApp(u))
        loging_root.mainloop()

    def add_item(self):
        AddItemDialog(self.root, self.manager, self.refresh_items)

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item first!")
            return
        item_id = int(selected[0])
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
            self.manager.delete_item(item_id)
            self.refresh_items()


class AddItemDialog:
    def __init__(self, parent, manager, refresh_callback):
        self.manager = manager
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Add Item")
        self.window.geometry("480x360")

        frame = ttk.Frame(self.window, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)

        name_label = ttk.Label(frame, text="Name:")
        name_label.grid(row=0, column=0, sticky="w", pady=5)

        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        qunatity_label = ttk.Label(frame, text="Qunatity:")
        qunatity_label.grid(row=1, column=0, sticky="w", pady=5)

        self.qunatity_entry = ttk.Entry(frame, width=30)
        self.qunatity_entry.grid(row=1, column=1, pady=5)

        price_label = ttk.Label(frame, text="Price:")
        price_label.grid(row=2, column=0, sticky="w", pady=5)

        self.price_entry = ttk.Entry(frame, width=30)
        self.price_entry.grid(row=2, column=1, pady=5)

        category_label = ttk.Label(frame, text="Category:")
        category_label.grid(row=3, column=0, sticky="w", pady=5)

        self.category_entry = ttk.Entry(frame, width=30)
        self.category_entry.grid(row=3, column=1, pady=5)

        self.save_button = ttk.Button(frame, text="Save", command=self.save_item)
        self.save_button.grid(row=4, column=1, pady=10)

    def save_item(self):
        name = self.name_entry.get().strip()
        quantity = self.qunatity_entry.get().strip()
        price = self.price_entry.get().strip()
        category = self.category_entry.get().strip()

        if not name:
            messagebox.showerror("required error", "The name is required!")
            return
        try:
            quantity = float(quantity) if quantity else 0
            price = float(price) if price else 0
        except ValueError:
            messagebox.showerror("Convert Error", "The qunatity and price should be numbers!")
            return

        item = Item(name, quantity, price, category)
        self.manager.add_item(item)
        self.refresh_callback()
        self.window.destroy()

class EditItemDialog:
    def __init__(self, parent, manager, item_data, refresh_callback):

        self.manager = manager
        self.refresh_callback = refresh_callback
        self.item_data = item_data

        self.window = tk.Toplevel(parent)
        self.window.title("Add Item")
        self.window.geometry("480x360")

        frame = ttk.Frame(self.window, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)


        name_label = ttk.Label(frame, text="Name:")
        name_label.grid(row=0, column=0, sticky="w", pady=5)

        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)
        self.name_entry.stringvar(Value=item_data["name"])

        qunatity_label = ttk.Label(frame, text="Qunatity:")
        qunatity_label.grid(row=1, column=0, sticky="w", pady=5)

        self.qunatity_entry = ttk.Entry(frame, width=30)
        self.qunatity_entry.grid(row=1, column=1, pady=5)
        self.qunatity_entry.stringvar(Value=item_data["quantity"])

        price_label = ttk.Label(frame, text="Price:")
        price_label.grid(row=2, column=0, sticky="w", pady=5)

        self.price_entry = ttk.Entry(frame, width=30)
        self.price_entry.grid(row=2, column=1, pady=5)
        self.price_entry.stringvar(Value=item_data["price"])

        category_label = ttk.Label(frame, text="Category:")
        category_label.grid(row=3, column=0, sticky="w", pady=5)
        

        self.category_entry = ttk.Entry(frame, width=30)
        self.category_entry.grid(row=3, column=1, pady=5)
        self.category_entry.stringvar(Value=item_data["category"])

        self.save_button = ttk.Button(frame, text="Save", command=self.save)
        self.save_button.grid(row=4, column=1, pady=10)

        
    def save(self):
        name = self.name_entry.get().strip()
        quantity = self.qunatity_entry.get().strip()
        price = self.price_entry.get().strip()
        category = self.category_entry.get().strip()

        if not name:
            messagebox.showerror("required error", "The name is required!")
            return
        try:
            quantity = float(quantity) if quantity else 0
            price = float(price) if price else 0
        except ValueError:
            messagebox.showerror("Convert Error", "The qunatity and price should be numbers!")
            return

        item = Item(name, quantity, price, category)
        self.manager.update_item(self.item_data["id"], name, quantity, price, category).
        self.refresh_callback()
        self.window.destroy()

    
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root, lambda u: MainApp(u))
    root.mainloop()