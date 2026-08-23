import tkinter as tk
from tkinter import ttk,messagebox
from manager import InventoryManager


class Loginwindow:
    def init(self,root,on_success):
        self.root = root
        self.on_success = on_success
        self.manager = InventoryManager()

        self.root.title("__LOGIN__")
        self.root.geometry("800x600")

        frame = ttk.Frame(root,padding=20)
        frame.grid(row=0,column=0,sticky="nsew")

        self.username_L = ttk.Label(frame,text="Username:")
        self.username_L.grid(row=0,column=0,sticky=tk.W,pady=5)

        self.username_E = ttk.Entry(frame,width=30)
        self.username_E.grid(row=0,column=1,pady=5)

        self.password_L = ttk.Label(frame,text="Password:")
        self.password_L.grid(row=1,column=0,sticky=tk.W,pady=5)

        self.password_E = ttk.Entry(frame,width=30)
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
            messagebox.showerror("LOGIN 💥ERROR💥","INVALID USERNAME OR PASSWORD❌")


class MainApp:
    def init(self,user):
        self.user = user
        self.manager = InventoryManager()

        self.root = tk.Tk()
        self.root.title(f"Inventory System - {user.username} ({user.role})")
        self.root.geometry("1600x1200")


if __name__ == "__main__":
    root = tk.Tk()
    Loginwindow(root,lambda u:MainApp(u))
    root.mainloop