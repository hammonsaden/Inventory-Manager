import sqlite3
import customtkinter
import csv
from tkinter import messagebox

class InvoApp: 
    def __init__(self):
        self.app = customtkinter.CTk()
        self.conn = sqlite3.connect('inventory.db')
        self.error_label = None
    def GUI(self):
        # CTk Setup
        customtkinter.set_appearance_mode("dark")
        self.app.title('Inventory Manager')
        self.app.geometry('1600x700')
        
        # Overhead GUI
        self.checkboxFrame = customtkinter.CTkFrame(self.app)
        self.checkboxFrame.grid(row=1, column=1, padx=0, pady=0)
        label = customtkinter.CTkLabel(self.checkboxFrame, text="Item Search: ")
        label.grid(row=1, column=1, padx=10, pady=10)
        self.text_input = customtkinter.CTkEntry(self.checkboxFrame, placeholder_text="Enter Item Name Here!", width=1000)
        self.text_input.grid(row=1, column=2, padx=10, pady=10)

        # Search Button
        button = customtkinter.CTkButton(self.checkboxFrame, text="Enter", command=self.SearchDB)
        button.grid(row=1, column=3, padx=10, pady=10)

        # Search by Dept
        self.sbd_combobox = customtkinter.CTkComboBox(self.checkboxFrame, values=["Produce", "Meat", "Grocery", "Dairy"], command=self.SBD_DB)
        self.sbd_combobox.grid(row=1, column=4, padx=10, pady=10)

        # EXPORT AS CSV
        csv_button = customtkinter.CTkButton(self.checkboxFrame, text='EXPORT CSV', command=self.CSVExport)
        csv_button.grid(row=1, column=5, padx=10, pady=0)

        # Generate Order Button
        gen_order_button = customtkinter.CTkButton(self.checkboxFrame, text='Generate Order', command=self.AutomaticOrder)
        gen_order_button.grid(row=2, column=5, padx=10, pady=0)
        # Search Frame
        self.searchFrame = customtkinter.CTkScrollableFrame(self.app, width=1550, height=600)
        self.searchFrame.grid(row=2, column=1, padx=10, pady=10)
        # Search Headers
        name_header = customtkinter.CTkLabel(self.searchFrame, text='Item')
        name_header.grid(row=1, column=1, padx=40, pady=10, sticky='nw')
        BOH_header = customtkinter.CTkLabel(self.searchFrame, text='Balance On Hand')
        BOH_header.grid(row=1, column=2, padx=50, pady=10, sticky='nw')
        cost_header = customtkinter.CTkLabel(self.searchFrame, text='Item Cost')
        cost_header.grid(row=1, column=3, padx=50, pady=10, sticky='nw')
        sale_price_header = customtkinter.CTkLabel(self.searchFrame, text='Sale Price')
        sale_price_header.grid(row=1, column=4, padx=50, pady=10, sticky='nw')
        profit_header = customtkinter.CTkLabel(self.searchFrame, text='Profit')
        profit_header.grid(row=1, column=5, padx=50, pady=10, sticky='nw')
        sold_header = customtkinter.CTkLabel(self.searchFrame, text='Sold Yesterday')
        sold_header.grid(row=1, column=6, padx=50, pady=10, sticky='nw')
        on_order_header = customtkinter.CTkLabel(self.searchFrame, text='Amount On Order')
        on_order_header.grid(row=1, column=7, padx=50, pady=10, sticky='nw')
        on_display_header = customtkinter.CTkLabel(self.searchFrame, text='Amount on Display')
        on_display_header.grid(row=1, column=8, padx=50, pady=10, sticky='nw')
        allocation_header = customtkinter.CTkLabel(self.searchFrame, text='Total Shelf Allocation')
        allocation_header.grid(row=1, column=9, padx=50, pady=10, sticky='nw')

    def SearchDB(self):
        # Deletes all widgets except the headers (row 1)
        for widget in self.searchFrame.winfo_children():
            if int(widget.grid_info()['row']) > 1:
                widget.destroy()

        # Search Handler
        search_val = self.text_input.get()
        print("User Searched: ", search_val)
        if search_val == "":
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM inventory")
            r = cur.fetchall()
            if r:
                val = 0
                for row in r:
                    val +=1
                    item, BOH, cost, sale_price, profit, sold, on_order, on_display, allocation, department = row 
                    item_label = customtkinter.CTkLabel(self.searchFrame, text=item)
                    item_label.grid(row=val+2, column=1, padx=10, pady=10)
                    BOH_label = customtkinter.CTkLabel(self.searchFrame, text=BOH)
                    BOH_label.grid(row=val+2, column=2, padx=40, pady=10)
                    cost_label = customtkinter.CTkLabel(self.searchFrame, text="$ " + str(cost))
                    cost_label.grid(row=val+2, column=3, padx=40, pady=10)
                    sale_price_label = customtkinter.CTkLabel(self.searchFrame, text="$ " + str(sale_price))
                    sale_price_label.grid(row=val+2, column=4, padx=40, pady=10)
                    profit_label = customtkinter.CTkLabel(self.searchFrame, text="$ " + str(profit))
                    profit_label.grid(row=val+2, column=5, padx=40, pady=10)
                    sold_label = customtkinter.CTkLabel(self.searchFrame, text=sold)
                    sold_label.grid(row=val+2, column=6, padx=40, pady=10)
                    on_order_label = customtkinter.CTkLabel(self.searchFrame, text=on_order)
                    on_order_label.grid(row=val+2, column=7, padx=40, pady=10)
                    on_display_label = customtkinter.CTkLabel(self.searchFrame, text=on_display)
                    on_display_label.grid(row=val+2, column=8, padx=40, pady=10)
                    allocation_label = customtkinter.CTkLabel(self.searchFrame, text=allocation)
                    allocation_label.grid(row=val+2, column=9, padx=40, pady=10)
            else:
                self.error_label = customtkinter.CTkLabel(self.searchFrame, text="No Results Found, Try Again.")
                self.error_label.grid(row=2, column=1, padx=0, pady=0, sticky="nsew")
        else:
            formatted_sv = search_val.capitalize()
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM inventory WHERE item LIKE ?", (formatted_sv,))
            r = cur.fetchall()
            if r:
                val = 0
                for row in r:
                    val += 1
                    item, BOH, cost, sale_price, profit, sold, on_order, on_display, allocation, department = row 
                    item_label = customtkinter.CTkLabel(self.searchFrame, text=item)
                    item_label.grid(row=val+2, column=1, padx=10, pady=10)
                    BOH_label = customtkinter.CTkLabel(self.searchFrame, text=BOH)
                    BOH_label.grid(row=val+2, column=2, padx=40, pady=10)
                    cost_label = customtkinter.CTkLabel(self.searchFrame, text="$ " + str(cost))
                    cost_label.grid(row=val+2, column=3, padx=40, pady=10)
                    sale_price_label = customtkinter.CTkLabel(self.searchFrame, text="$ " + str(sale_price))
                    sale_price_label.grid(row=val+2, column=4, padx=40, pady=10)
                    profit_label = customtkinter.CTkLabel(self.searchFrame, text="$ " + str(profit))
                    profit_label.grid(row=val+2, column=5, padx=40, pady=10)
                    sold_label = customtkinter.CTkLabel(self.searchFrame, text=sold)
                    sold_label.grid(row=val+2, column=6, padx=40, pady=10)
                    on_order_label = customtkinter.CTkLabel(self.searchFrame, text=on_order)
                    on_order_label.grid(row=val+2, column=7, padx=40, pady=10)
                    on_display_label = customtkinter.CTkLabel(self.searchFrame, text=on_display)
                    on_display_label.grid(row=val+2, column=8, padx=40, pady=10)
                    allocation_label = customtkinter.CTkLabel(self.searchFrame, text=allocation)
                    allocation_label.grid(row=val+2, column=9, padx=40, pady=10)
            else:
                self.error_label = customtkinter.CTkLabel(self.searchFrame, text="No Results Found, Try Again.")
                self.error_label.grid(row=2, column=1, padx=0, pady=0, sticky="nsew")
            
    def SBD_DB(self, event=None):
        for widget in self.searchFrame.winfo_children():
            if int(widget.grid_info()['row']) > 1:
                widget.destroy()

        dept = self.sbd_combobox.get()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE department = ?", (dept,))
        r = cur.fetchall()
        if r:
            val = 0
            for row in r:
                val +=1
                item, BOH, cost, sale_price, profit, sold, on_order, on_display, allocation, department = row 
                item_label = customtkinter.CTkLabel(self.searchFrame, text=item)
                item_label.grid(row=val+2, column=1, padx=10, pady=10)
                BOH_label = customtkinter.CTkLabel(self.searchFrame, text=BOH)
                BOH_label.grid(row=val+2, column=2, padx=40, pady=10)
                cost_label = customtkinter.CTkLabel(self.searchFrame, text=cost)
                cost_label.grid(row=val+2, column=3, padx=40, pady=10)
                sale_price_label = customtkinter.CTkLabel(self.searchFrame, text=sale_price)
                sale_price_label.grid(row=val+2, column=4, padx=40, pady=10)
                profit_label = customtkinter.CTkLabel(self.searchFrame, text=profit)
                profit_label.grid(row=val+2, column=5, padx=40, pady=10)
                sold_label = customtkinter.CTkLabel(self.searchFrame, text=sold)
                sold_label.grid(row=val+2, column=6, padx=40, pady=10)
                on_order_label = customtkinter.CTkLabel(self.searchFrame, text=on_order)
                on_order_label.grid(row=val+2, column=7, padx=40, pady=10)
                on_display_label = customtkinter.CTkLabel(self.searchFrame, text=on_display)
                on_display_label.grid(row=val+2, column=8, padx=40, pady=10)
                allocation_label = customtkinter.CTkLabel(self.searchFrame, text=allocation)
                allocation_label.grid(row=val+2, column=9, padx=40, pady=10)
        else:
            self.error_label = customtkinter.CTkLabel(self.searchFrame, text="No Results Found, Try Again.")
            self.error_label.grid(row=2, column=1, padx=0, pady=0, sticky="nsew")
    
    def CSVExport(self):
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        with open('invo_export.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
            writer.writerows(rows)
        
        messagebox.showinfo("Export Successful", "Data Exported to CSV Successfully!")
    
    def AutomaticOrder(self):
        # Order Generation
        cur = self.conn.cursor()

        cur.execute("SELECT item, BOH, allocation, on_order FROM inventory WHERE BOH < (1.25 * allocation)")
        
        low_stock_items = cur.fetchall()
        # CSV Generator
        with open('order_list.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Item Name', "Current BOH", "Allocation", "Reorder Quantity"])

            for it in low_stock_items:

                item, BOH, allocation, on_order = it
                reorder_quantity = round((1.25 * allocation)) - BOH

                if reorder_quantity > 0:
                    print(f"Low stock detected: {item} (Current BOH: {BOH}, Allocation: {allocation})")
                    print(f"Ordering {reorder_quantity} more units of {item}.")

                    writer.writerow([item, BOH, allocation, reorder_quantity])

                    cur.execute("UPDATE inventory SET on_order = ? WHERE item = ?", (reorder_quantity, item))

        self.conn.commit()

        messagebox.showinfo("Export Successful", "Order Exported to CSV Successfully!")

    def run(self):
        self.GUI()
        self.app.mainloop()





app = InvoApp()
app.run()