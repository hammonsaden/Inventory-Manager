# Inventory-Manager


This is a program for my resume. It's a Inventory Manager built using the Python(CustomTkinter, Sqlite3, Tkinter packages), and SQL programming languages.


~ Features ~
You can view the full inventory of the store by pressing the enter button with the input blank, and it will pull up all the data on all of the items in the store.
You can filter by department for items in the store.
You can search by name of item in the input.
You can export all of the items in the inventory as a csv file, using the "EXPORT AS CSV" button.
You can Generate a Order and it will auto export as a csv file, it looks for items that have BOH < Allocation, orders 125% of the allocation, and puts it into a table to export as a csv file.