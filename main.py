import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import string
import random


# --------------- PASSWORD GENERATOR -------------------------------------
# Función para generar la contraseña aleatoria
def generate_password():
    try:
        length = int(entry_length.get())
        if length < 1:
            raise ValueError("Length must be greater than 0")
        
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for the password length.")

# Función que abre la pantalla de generación de contraseñas

# --------------- TEXT EDITOR -------------------------------------
def open_password_generator():
    password_window = tk.Toplevel(root)
    password_window.title("Password Generator")
    password_window.geometry("300x200")
    
    tk.Label(password_window, text="Password Length:").pack(pady=5)
    global entry_length
    entry_length = tk.Entry(password_window)
    entry_length.pack(pady=5)
    
    tk.Label(password_window, text="Generated Password:").pack(pady=5)
    global password_entry
    password_entry = tk.Entry(password_window, width=30)
    password_entry.pack(pady=5)
    
    tk.Button(password_window, text="Generate Password", command=generate_password).pack(pady=10)

# Función para abrir el editor de texto
def open_text_editor():
    editor_window = tk.Toplevel(root)
    editor_window.title("Text Editor")
    editor_window.geometry("500x400")
    
    global text_area
    text_area = tk.Text(editor_window, wrap="word")
    text_area.pack(expand=True, fill="both")
    
    menu_bar = tk.Menu(editor_window)
    editor_window.config(menu=menu_bar)
    
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_command(label="Save As...", command=save_as_file)
    menu_bar.add_cascade(label="File", menu=file_menu)

# Función para abrir un archivo de texto
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                content = file.read()
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, content)
            global current_file_path
            current_file_path = file_path
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

# Función para guardar el archivo de texto
def save_file():
    global current_file_path
    if current_file_path:
        try:
            with open(current_file_path, "w") as file:
                content = text_area.get(1.0, tk.END)
                file.write(content)
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
    else:
        save_as_file()

# Función para guardar como un nuevo archivo
def save_as_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                content = text_area.get(1.0, tk.END)
                file.write(content)
            global current_file_path
            current_file_path = file_path
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
            
            
                
# --------------- JSON READER AND EDITOR-------------------------------------
# Función para abrir el lector de archivos JSON
def open_json_reader():
    reader_window = tk.Toplevel(root)
    reader_window.title("JSON File Reader")
    reader_window.geometry("600x400")
    
     # Etiqueta para el encabezado (inicialmente vacío)
    global header_label
    header_label = tk.Label(reader_window, text="", font=("Helvetica", 16))
    header_label.pack(pady=10)

    # Configura la tabla Treeview
    global tree
    tree = ttk.Treeview(reader_window, show="headings")
    tree.pack(expand=True, fill="both")

    # Botones para abrir y guardar archivos JSON
    open_button = tk.Button(reader_window, text="Open JSON File", command=open_json_file)
    open_button.pack(pady=5)

    save_button = tk.Button(reader_window, text="Save JSON File", command=save_json_file)
    save_button.pack(pady=5)
    # Asigna el evento de doble clic para editar celdas
    tree.bind("<Double-1>", on_item_double_click)

# Función para abrir un archivo JSON
def open_json_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
            load_data_to_table(data)
            global current_json_path
            current_json_path = file_path
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

# Cargar datos en la tabla
def load_data_to_table(data):
    tree.delete(*tree.get_children())  # Limpia la tabla antes de cargar nuevos datos

    # Determina el título dinámicamente
    if isinstance(data, dict):
        if len(data) == 1:
            title = list(data.keys())[0]
            header_label.config(text=title)
            products = data[title]
        else:
            title = "Data"
            header_label.config(text=title)
            products = list(data.values())
    elif isinstance(data, list):
        title = "Items"
        header_label.config(text=title)
        products = data
    else:
        messagebox.showerror("Error", "Invalid JSON structure.")
        return

    # Limpia las columnas existentes
    tree["columns"] = []
    tree["show"] = "headings"  # Muestra solo encabezados

    # Carga dinámicamente los encabezados
    if products:
        if isinstance(products, list) and isinstance(products[0], dict):
            headers = products[0].keys()
            tree["columns"] = list(headers)  # Asigna las claves como columnas
            for header in headers:
                tree.heading(header, text=header)  # Configura el encabezado de la columna

            # Inserta los productos en la tabla
            for product in products:
                if isinstance(product, dict):
                    values = [product.get(header, "") for header in headers]  # Obtiene los valores según los encabezados
                    tree.insert("", "end", values=values)  # Inserta los valores
        else:
            messagebox.showerror("Error", "Expected a list of dictionaries.")

# Función para manejar el evento de doble clic en un ítem de la tabla
def on_item_double_click(event):
    item = tree.selection()[0]  # Obtiene el ítem seleccionado
    column = tree.identify_column(event.x)  # Identifica la columna
    column_index = int(column.replace("#", "")) - 1  # Convierte a índice 0

    # Obtiene el valor actual
    current_value = tree.item(item, "values")[column_index]

    # Crea una ventana de entrada para editar el valor
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Value")

    entry = tk.Entry(edit_window)
    entry.insert(0, current_value)
    entry.pack(pady=10)

    def save_edit():
        new_value = entry .get()
        tree.item(item, values=list(tree.item(item, "values")[:column_index]) + [new_value] + list(tree.item(item, "values")[column_index + 1:]))
        edit_window.destroy()

    save_button = tk.Button(edit_window, text="Save", command=save_edit)
    save_button.pack(pady=5)

# Guardar los datos de la tabla en el archivo JSON

def save_json_file():
    if current_json_path:
        try:
            # Crea una lista de diccionarios a partir de los datos en la tabla
            data = []
            for child in tree.get_children():
                values = tree.item(child, "values")
                data.append(dict(zip(tree["columns"], values)))

            # Guarda los datos en el archivo JSON
            with open(current_json_path, "w", encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)  # Asegura que se guarden caracteres especiales
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
    else:
        # Si no hay un archivo abierto, permite al usuario seleccionar uno nuevo
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                   filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                # Crea una lista de diccionarios a partir de los datos en la tabla
                data = []
                for child in tree.get_children():
                    values = tree.item(child, "values")
                    data.append(dict(zip(tree["columns"], values)))

                # Guarda los datos en el nuevo archivo JSON
                with open(file_path, "w", encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)  # Asegura que se guarden caracteres especiales
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
                
                
# Configuración de la ventana principal
root = tk.Tk()
root.title("Program with Functionalities")
root.geometry("300x200")

current_file_path = None
text_area = None
current_json_path = None
tree = None

# Botones principales
button1 = tk.Button(root, text="Password Generator", command=open_password_generator)
button1.pack(pady=10)

button2 = tk.Button(root, text="Text Editor", command=open_text_editor)
button2.pack(pady=10)

button3 = tk.Button(root, text="JSON File Reader", command=open_json_reader)
button3.pack(pady=10)

root.mainloop()
