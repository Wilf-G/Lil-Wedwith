import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

class KitchenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Inc. Kitchen Management")
        self.root.geometry("1000x600")
        
        # UI Styling
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=('Arial', 10))
        
        # MAIN LAYOUT
        self.notebook = ttk.Notebook(root)
        self.order_tab = ttk.Frame(self.notebook)
        self.stock_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.order_tab, text="Live Orders")
        self.notebook.add(self.stock_tab, text="Stock Monitor")
        self.notebook.pack(expand=1, fill="both")
        
        self.setup_order_tab()
        self.setup_stock_tab()
        self.refresh_data()

    def setup_order_tab(self):
        # Search Section
        search_frame = tk.Frame(self.order_tab, pady=10)
        search_frame.pack(fill="x")
        
        tk.Label(search_frame, text="Search Order ID / Name:").pack(side="left", padx=10)
        self.search_ent = tk.Entry(search_frame)
        self.search_ent.pack(side="left", padx=10)
        
        tk.Button(search_frame, text="Search", command=self.search_order, bg="#ff6b6b", fg="white").pack(side="left", padx=5)
        tk.Button(search_frame, text="Refresh All", command=self.refresh_data, bg="#000b3d", fg="white").pack(side="left", padx=5)

        # Order List (Treeview)
        cols = ("ID", "Customer", "Type", "Location", "Total", "Status")
        self.tree = ttk.Treeview(self.order_tab, columns=cols, show="headings")
        for col in cols: 
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
            
        self.tree.pack(side="left", fill="both", expand=1)
        self.tree.bind("<<TreeviewSelect>>", self.show_receipt)

        # Visual Receipt Area
        self.receipt_text = tk.Text(self.order_tab, width=40, font=("Courier", 12), bg="#fffde7", padx=10, pady=10)
        self.receipt_text.pack(side="right", fill="both", padx=10)

    def setup_stock_tab(self):
        self.stock_tree = ttk.Treeview(self.stock_tab, columns=("Item", "Remaining"), show="headings")
        self.stock_tree.heading("Item", text="Item Name")
        self.stock_tree.heading("Remaining", text="Units in Stock")
        self.stock_tree.pack(fill="both", expand=1, padx=20, pady=20)

    def refresh_data(self):
        if not os.path.exists('food_inc.db'):
            return

        # Refresh Orders
        for item in self.tree.get_children(): self.tree.delete(item)
        conn = sqlite3.connect('food_inc.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, customer_name, service_type, location, total_price, status FROM orders ORDER BY id DESC")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        
        # Refresh Stock
        for item in self.stock_tree.get_children(): self.stock_tree.delete(item)
        cursor.execute("SELECT item_name, quantity FROM stock")
        for row in cursor.fetchall():
            self.stock_tree.insert("", "end", values=row)
        conn.close()

    def show_receipt(self, event):
        selected = self.tree.selection()
        if not selected: return
        order_values = self.tree.item(selected[0])['values']
        order_id = order_values[0]
        cust_name = order_values[1]
        
        conn = sqlite3.connect('food_inc.db')
        cursor = conn.cursor()
        cursor.execute("SELECT item_name, quantity FROM order_items WHERE order_id=?", (order_id,))
        items = cursor.fetchall()
        
        self.receipt_text.delete('1.0', tk.END)
        self.receipt_text.insert(tk.END, f"       FOOD INC. KITCHEN\n")
        self.receipt_text.insert(tk.END, f"       RECEIPT FOR #{order_id}\n")
        self.receipt_text.insert(tk.END, "="*30 + "\n")
        self.receipt_text.insert(tk.END, f" CUSTOMER: {cust_name}\n")
        self.receipt_text.insert(tk.END, f" TYPE: {order_values[2]}\n")
        self.receipt_text.insert(tk.END, f" AT: {order_values[3]}\n")
        self.receipt_text.insert(tk.END, "-"*30 + "\n")
        for name, qty in items:
            self.receipt_text.insert(tk.END, f" {qty}x {name}\n")
        self.receipt_text.insert(tk.END, "="*30 + "\n")
        self.receipt_text.insert(tk.END, f" TOTAL PAID: £{order_values[4]}\n")
        conn.close()

    def search_order(self):
        query = self.search_ent.get()
        if not query:
            self.refresh_data()
            return
            
        for item in self.tree.get_children(): self.tree.delete(item)
        conn = sqlite3.connect('food_inc.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, customer_name, service_type, location, total_price, status FROM orders WHERE id=? OR customer_name LIKE ?", (query, f"%{query}%"))
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = KitchenApp(root)
    root.mainloop()