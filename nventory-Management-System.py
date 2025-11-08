import tkinter as tk
from tkinter import messagebox, simpledialog

class InventorySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.users = {"admin": "admin123"}                           
        self.logged_in = False
        self.inventory = {}  
        self.low_stock_limit = 5 
        self.login_screen() 

    def login_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        tk.Button(self.root, text="Login", command=self.check_login).pack()
        self.username_entry.focus_set()

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username] == password:
            self.logged_in = True
            self.main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def main_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Product Name").pack()
        self.product_entry = tk.Entry(self.root)
        self.product_entry.pack()
        tk.Label(self.root, text="Quantity").pack()
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.pack()

        tk.Button(self.root, text="Add Product", command=self.add_product).pack()
        tk.Button(self.root, text="Edit Product", command=self.edit_product).pack()
        tk.Button(self.root, text="Delete Product", command=self.delete_product).pack()
        tk.Button(self.root, text="Show Report", command=self.show_report).pack()
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=5)

        self.product_listbox = tk.Listbox(self.root)
        self.product_listbox.pack(fill=tk.BOTH, expand=True)
        self.update_listbox()
        self.product_entry.focus_set()

    def add_product(self):
        name = self.product_entry.get()
        quantity = self.quantity_entry.get()
        if not name or not quantity.isdigit():
            messagebox.showerror("Error", "Enter valid name and quantity")
            return
        self.inventory[name] = int(quantity)
        self.update_listbox()
        self.product_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.product_entry.focus_set()

    def edit_product(self):
        selected = self.product_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a product")
            return
        name = self.product_listbox.get(selected[0]).split(":")[0]
        new_quantity = simpledialog.askinteger("Edit Quantity", f"Enter new quantity for '{name}':")
        if new_quantity is not None:
            self.inventory[name] = new_quantity
            self.update_listbox()

    def delete_product(self):
        selected = self.product_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a product")
            return
        name = self.product_listbox.get(selected[0]).split(":")[0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?")
        if confirm:
            del self.inventory[name]
            self.update_listbox()

    def show_report(self):
        report = ""
        for name, qty in self.inventory.items():
            status = "Low Stock" if qty < self.low_stock_limit else "OK"
            report += f"{name}: {qty} ({status})\n"
        if not report:
            report = "No products"
        messagebox.showinfo("Inventory Report", report)

    def update_listbox(self):
        self.product_listbox.delete(0, tk.END)
        for name, qty in self.inventory.items():
            self.product_listbox.insert(tk.END, f"{name}: {qty}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


root = tk.Tk()
app = InventorySystem(root)
root.mainloop()
