import sqlalchemy as db
import tkinter as tk


root = tk.Tk()
root.title(" Phone Book ")
root.geometry("800x500")
root.configure(bg = 'black', padx = 100)
root.resizable(0,0)
frame1 = tk.LabelFrame(root ,height = 200 ,width = 100 ,bd = 0 ,text = "MANAGE CONTACTS", bg = "black", fg = "green", font=("Helvetica", 18, "bold"))
frame2 = tk.LabelFrame(root ,height = 200 ,width = 100, bd = 0 ,text = "LIST OF CONTACTS", bg = "black", fg = "green", font=("Helvetica", 18, "bold"))

engine = db.create_engine('sqlite:///app.db')
connection = engine.connect()
metadata = db.MetaData()
phnbook = db.Table('phnbook', metadata, autoload=True, autoload_with=engine)


def insert_contact(name, contact):    
    connection.execute(phnbook.insert().values(name = name, contact = contact))

def delete_contact(name):
    connection.execute(phnbook.delete().where(phnbook.c.name == name))

def fetch_contact_list(): 
    return connection.execute(db.select([phnbook])).fetchall()


class UserInterface():
    
    def __init__(self):

        self.add_contact_button = tk.Button(frame1, text = "INSERT", bg = "green", fg = "white", font = ("Helvetica", 14, "bold"), command = self.on_add_button_click)                                                                                
        self.name_box = tk.Entry(frame1, fg = "green", bg = "black", font = ("Helvetica", 12, "bold"))
        self.contact_box = tk.Entry(frame1, fg = "green", bg = "black", font = ("Helvetica", 12, "bold"))
        self.name_label = tk.Label(frame1, text = "Name", fg = "white", bg = "black")
        self.contact_label = tk.Label(frame1, text = "Contact Number", fg = "white", bg = "black")
        self.search_box = tk.Entry(frame1, fg = "green", bg = "black", font = ("Helvetica", 12, "bold"))
        self.search_result = tk.Entry(frame1, fg = "green", bg = "black", font = ("Helvetica", 12, "bold"))
        self.find_contact_button = tk.Button(frame1, text = "Search",bg = "green", fg = "white", font = ("Helvetica", 14, "bold"), command = self.find_contact)
        self.search_label = tk.Label(frame1, text = "Enter name", fg = "white", bg = "black")
        self.listbox = tk.Listbox(frame2, bg = "black", fg = "green", font = ("Helvetica", 12, "bold"))
        self.delete_button = tk.Button(frame2, text = "DELETE", bg = "red", fg = "white", font = ("Helvetica", 12, "bold"), command = self.on_del_button_click)
        self.list_result = tk.Entry(frame2, fg = "green", bg = "black", font = ("Helvetica", 12, "bold"))
        self.show_contact_button = tk.Button(frame2, text = " SHOW ", bg = "blue", fg = "white", font = ("Helvetica", 14, "bold"), command = self.show_contact)
        self._name_label = tk.Label(frame1, text = "Name", fg = "white", bg = "black")
        self.result_label = tk.Label(frame1, text = "Search Result", fg = "white", bg = "black")

        
    def pack_widgets(self):

        self.add_contact_button.pack(padx = 40, pady = 15)
        self.name_label.pack(padx = 40, pady = 5)
        self.name_box.pack(padx = 40, pady = 5)
        self.contact_label.pack(padx = 40, pady = 5)
        self.contact_box.pack(padx = 40, pady = 5)
        self.find_contact_button.pack(padx = 40, pady = 5)
        self._name_label.pack(padx = 40, pady = 5)
        self.search_box.pack(padx = 40, pady = 5)
        self.result_label.pack(padx = 40, pady = 5)
        self.search_result.pack(padx = 40, pady = 5)
        self.update_list()
        self.listbox.pack(padx = 20, pady = 20)
        self.show_contact_button.pack(padx = 20, pady = 5)
        self.list_result.pack(padx = 20, pady = 5)
        self.delete_button.pack(padx = 20, pady = 5)
        frame2.pack(side = tk.LEFT)
        frame1.pack(side = tk.RIGHT)
        root.mainloop()


    def on_add_button_click(self):
        insert_contact(self.name_box.get(), self.contact_box.get())
        data = str(self.name_box.get())
        self.listbox.insert('end' ,data)
        self.name_box.delete(0, 'end')
        self.contact_box.delete(0, 'end')


    def on_del_button_click(self):
        data = self.listbox.get(self.listbox.curselection())
        delete_contact(data)
        self.listbox.delete(tk.ACTIVE)
        self.list_result.delete(0, 'end')
            

    def find_contact(self):
        contact_list = fetch_contact_list()
        name = str(self.search_box.get())
        for contact in contact_list:
            if name == str(contact[0]):
                self.search_result.delete(0, 'end')
                self.search_result.insert('end', str(contact[1]))

        
    def update_list(self):
        contact_list = fetch_contact_list()
        for contact in contact_list:
            data = str(contact[0]) 
            self.listbox.insert('end' , data)

    def show_contact(self):
        name = self.listbox.get(self.listbox.curselection())
        contact_list = fetch_contact_list()
        for contact in contact_list:
            if name == str(contact[0]):
                self.list_result.delete(0, 'end')
                self.list_result.insert('end', str(contact[1]))


def main():
    ui = UserInterface()
    ui.pack_widgets()
    
    
if __name__ == '__main__':
    main()

 
