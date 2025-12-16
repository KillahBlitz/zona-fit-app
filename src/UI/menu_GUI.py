import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from src.models.DAOClass import ClienteDAO
from src.scripts.utils import add_client, delete_client, clean_form

class App(tk.Tk):
    COLOR_BG = "#1D2D44"
    
    def __init__(self):
        super().__init__()
        self.client_id = None
        self.window_configure()
        self.grid_configure()
        self.show_title()
        self.show_form()
        self.show_table()
        self.show_buttons()
    
    def window_configure(self):
        self.geometry("900x600")
        self.title("ZONA FIT Application")
        self.configure(bg=self.COLOR_BG)

        self.style_apply = ttk.Style()
        self.style_apply.theme_use("clam")
        self.style_apply.configure(self,
                             background=self.COLOR_BG,
                             foreground="white",
                             font=("Helvetica", 12))

    def grid_configure(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
    
    def show_title(self):
        ticket = ttk.Label(self, text="ZONA FIT", 
                           font=("Helvetica", 24, "bold"), 
                           foreground="white", background=self.COLOR_BG)
        ticket.grid(row=0, column=0, columnspan=2, pady=30)

    def show_form(self):
        self.frame_form = tk.Frame(background=self.COLOR_BG)
        name_l = ttk.Label(self.frame_form, text="Nombre: ")
        name_l.grid(row=0, column=0, sticky=tk.W, padx=5, pady=30)
        self.name_e = ttk.Entry(self.frame_form)
        self.name_e.grid(row=0, column=1)
        self.name_e.configure(foreground="black")

        last_name_l = ttk.Label(self.frame_form, text="Apellido: ")
        last_name_l.grid(row=1, column=0, sticky=tk.W, padx=5, pady=30)
        self.last_name_e = ttk.Entry(self.frame_form)
        self.last_name_e.grid(row=1, column=1)
        self.last_name_e.configure(foreground="black")

        membership_l = ttk.Label(self.frame_form, text="Membresia: ")
        membership_l.grid(row=2, column=0, sticky=tk.W, padx=5, pady=30)
        self.membership_e = ttk.Entry(self.frame_form)
        self.membership_e.grid(row=2, column=1)
        self.membership_e.configure(foreground="black")

        self.frame_form.grid(row=1, column=0)

    def show_table(self):
        self.frame_table = tk.Frame(self)
        self.style_apply.configure('Treeview', 
                                   background="black", 
                                   foreground="white", 
                                   fieldbackground="black",
                                   rowheight=20)
        columns = ('Id','Nombre', 'Apellido', 'Membresia')
        self.table = ttk.Treeview(self.frame_table, columns=columns, show='headings')

        self.table.heading('Id', text='Id', anchor=tk.CENTER)
        self.table.heading('Nombre', text='Nombre', anchor=tk.W)
        self.table.heading('Apellido', text='Apellido', anchor=tk.W)
        self.table.heading('Membresia', text='Membresia', anchor=tk.W)

        self.table.column('Id', width=50, anchor=tk.CENTER)
        self.table.column('Nombre', width=100, anchor=tk.W)
        self.table.column('Apellido', width=100, anchor=tk.W)
        self.table.column('Membresia', width=100, anchor=tk.W)

        cients = ClienteDAO.seleccionar()
        for client in cients:
            self.table.insert(parent='', index=tk.END, values=(client.id, client.nombre, 
                                                               client.apellido, client.membresia))
            
        scroll_bar = ttk.Scrollbar(self.frame_table, orient=tk.VERTICAL, 
                                   command=self.table.yview)
        self.table.configure(yscroll=scroll_bar.set)
        scroll_bar.grid(row=0, column=1, sticky='ns')

        self.table.bind("<<TreeviewSelect>>", self.load_client)

        self.table.grid(row=0, column=0)
        self.frame_table.grid(row=1, column=1, padx=20)

    def show_buttons(self):
        self.frame_buttons = tk.Frame(background=self.COLOR_BG)

        add_button = ttk.Button(self.frame_buttons, text="Guardar", command=lambda: self.methods("add"))
        add_button.grid(row=0, column=0, padx=30)
        delete_button = ttk.Button(self.frame_buttons, text="Eliminar", command=lambda: self.methods("delete"))
        delete_button.grid(row=0, column=1, padx=30)
        clean_button = ttk.Button(self.frame_buttons, text="Limpiar", command=self.reload_data)
        clean_button.grid(row=0, column=2, padx=30)

        self.style_apply.configure('TButton', background="#005F73")
        self.style_apply.map('TButton', background=[('active', "#0A9396")])
        self.frame_buttons.grid(row=2, column=0, columnspan=2, pady=20)

    def methods(self, method=None):
        result = False
        data = {
            "id": self.client_id,
            "name": self.name_e.get(),
            "last_name": self.last_name_e.get(),
            "membership": self.membership_e.get()
        }
        init_methods = {
            "add": add_client,
            "delete": delete_client,
            "clean": clean_form
        }

        if(self.name_e.get() and self.last_name_e.get() and self.membership_e.get()):
            if self.membership_validator():
                result, type_action = init_methods[method](data)
            else:
                showerror("Error", "Membresia No numerica")
                self.membership_e.delete(0, tk.END)
                self.membership_e.focus_set()
        else:
            showerror("Warning", "SE DEBEN LLENAR TODOS LOS CAMPOS")
            self.name_e.focus_set()
        
        if result and type_action == "add":
            showinfo(title="Exito", message="Cliente Agregado Correctamente")
        elif result and type_action == "update":
            showinfo(title="Exito", message="Cliente Actualizado Correctamente")
        elif result and type_action == "delete":
            showinfo(title="Exito", message="Cliente Eliminado Correctamente")
        else:
            if type_action == "delete":
                showinfo(title="WARNING", message="Seleccione un cliente para eliminar")
            else:
                showerror(title="ERROR", message="Ocurrio un error al procesar la solicitud")
        
        self.reload_data()

    def load_client(self, event):
        element_select = self.table.selection()[0]
        element = self.table.item(element_select)
        client_e = element['values']
        self.client_id = client_e[0]
        name = client_e[1]
        last_name = client_e[2]
        membership = client_e[3]
        self.clean_form()
        self.name_e.insert(0, name)
        self.last_name_e.insert(0, last_name)
        self.membership_e.insert(0, membership)

    def membership_validator(self):
        try:
            int(self.membership_e.get())
            return True
        except:
            return False
        
    def reload_data(self):
        self.show_table()
        self.clean_form()
        self.client_id = None

    def clean_form(self):
        self.name_e.delete(0, tk.END)
        self.last_name_e.delete(0, tk.END)
        self.membership_e.delete(0, tk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()