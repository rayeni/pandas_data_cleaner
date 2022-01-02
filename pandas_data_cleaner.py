# library for numerical analysis
#from tkinter.constants import W
import numpy as np
# library for data management
import pandas as pd

# libraries for gui development
import tkinter as tk
import tkinter.font as font
from tkinter import ttk, END, StringVar, IntVar, \
messagebox, filedialog, messagebox

# library to assist in finding files on windows machines
from pathlib import Path

# -- Windows only configuration --
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
# -- End Windows only configuration --

# variables
df = pd.DataFrame() # create empty dataframe
my_dir = Path(__file__).parent # needed to address .ico file not found error

# functions
def import_from_csv():
    csv_file = filedialog.askopenfilename(
        initialdir="./", 
        title="Open CSV", 
        filetypes=(("CSV Files", "*.csv"),("All Files","*.*")))
    
    global df 
    df = pd.read_csv(csv_file)
    print(df.head())

def export_to_csv():
    csv_name = filedialog.asksaveasfilename(
        initialdir="./", 
        title="Export to CSV", 
        filetypes=(("CSV Files","*.csv"),("All Files","*.*")))
    
    global df
    df.to_csv(csv_name, index=False)

def close_app():
    #Use messagebox to ask to close note
    question = messagebox.askyesno("Close Pandas Data Cleaner", "Are you sure you want to exit?")
    if question == 1:
        root.destroy()

def drop_all_nulls():
    global df
    num_of_nulls = int(df.isnull().sum().sum())
    question = messagebox.askyesno("Drop Nulls", f"Drop {num_of_nulls} nulls?")
    if question == 1:
        df.dropna(inplace = True)

def open_drop_cols_window():
    def drop_columns():
        col_list = [col_listbox.get(i) for i in col_listbox.curselection()]
        df.drop(columns=col_list, inplace=True)

    global df

    # create window
    dc_window = tk.Toplevel(root)
    dc_window.geometry('500x500')
    try:
        dc_window.iconbitmap('./images/panda.ico')
    except:
        dc_window.iconbitmap(my_dir / './images/panda.ico')
    dc_window.resizable(0,0)
    dc_window.title('Drop Columns')

    # create frame for window
    dc_frame = tk.Frame(dc_window, bg='#0000ff', width=500, height=500)
    dc_frame.columnconfigure((0,1), weight=1)
    dc_frame.rowconfigure(0, weight=1)
    dc_frame.pack(padx=5, pady=5)
    dc_frame.grid_propagate(0)

    # create buttons and display in frame
    dc_dropcols_btn = ttk.Button(dc_frame, text='Drop Columns', width=15, command=drop_columns)
    dc_dropcols_btn.grid(row=0, column=1, padx=5, pady=5, sticky='NE')

    dc_close_btn = ttk.Button(dc_frame, text='Close', width=15, command=dc_window.destroy)
    dc_close_btn.grid(row=0, column=1, padx=5, pady=5, sticky='E')

    # create list box
    col_idxs = df.columns # get column indexes
    cols = tuple(col_idxs) # convert index to tuple
    col_list_var = tk.StringVar(value=cols) # listbox String Variable
    col_listbox = tk.Listbox(dc_frame, listvariable=col_list_var, selectmode='extended') # listbox
    col_listbox.grid(row=0, column=0, padx=5, pady=5, sticky='NS')

    dc_window.grab_set()





# create main window
root = tk.Tk()
root.title('Pandas Data Cleaner')
try:
    root.iconbitmap('./images/panda.ico')
except:
    root.iconbitmap(my_dir / './images/panda.ico')
root.geometry("800x600")
root.resizable(False, False)

# Set global font.  Doesn't apply to fields.  
font.nametofont('TkDefaultFont').configure(size=15)

# create top level frame
top_frame = tk.Frame(root, bg='#0000ff', width=800, height=70)
top_frame.columnconfigure((0,1,2), weight=1)
top_frame.pack(padx=5, pady=5)
top_frame.grid_propagate(0)

# create functionality frame, func_frame_1
func_frame_1 = tk.Frame(root, bg='#0000ff', width=800, height=70)
func_frame_1.columnconfigure((0,1,2), weight=1)
func_frame_1.pack(padx=5, pady=5)
func_frame_1.grid_propagate(0)


# layout for top_frame
import_data = tk.Button(top_frame, text='Import from CSV', width=16, command=import_from_csv)
import_data.grid(row=0, column=0, padx=5, pady=5, sticky='W')
export_data = tk.Button(top_frame, text='Export to CSV', width=16, command=export_to_csv)
export_data.grid(row=0, column=1, padx=5, pady=5)
close_root = tk.Button(top_frame, text='Close App', width=16, command=close_app)
close_root.grid(row=0, column=2, padx=5, pady=5, sticky='E')


# layout for functionality frame, func_frame_1
# Missing data menu button
mb_missing_data = ttk.Menubutton(func_frame_1, text='Missing Data', width=15) 
menu_missing_data = tk.Menu(mb_missing_data, tearoff=False) # Missing data menu
menu_missing_data.add_command(label='Drop nulls (All)', font=("Segoe UI", 15), command=drop_all_nulls) # Drop nulls menu option
mb_missing_data["menu"] = menu_missing_data # associate menu with menu button
mb_missing_data.grid(row=0, column=0, padx=5, pady=5, sticky='W') # display menu button in frame

# Dataframe tasks menu button
mb_df_tasks = ttk.Menubutton(func_frame_1, text='DF Tasks', width=15) 
menu_df_tasks = tk.Menu(mb_df_tasks, tearoff=False) # Missing data menu
menu_df_tasks.add_command(label='Drop Columns', font=("Segoe UI", 15), command=open_drop_cols_window) # Drop columns menu option
mb_df_tasks["menu"] = menu_df_tasks # associate menu with menu button
mb_df_tasks.grid(row=0, column=1, padx=5, pady=5) # display menu button in frame

# Clean numeric data menu button
mb_clean_numeric = ttk.Menubutton(func_frame_1, text='Clean Numeric', width=15) 
menu_clean_numeric = tk.Menu(mb_clean_numeric, tearoff=False) # Missing data menu
menu_clean_numeric.add_command(label='') # add command
mb_clean_numeric["menu"] = menu_clean_numeric # associate menu with menu button
mb_clean_numeric.grid(row=0, column=2, padx=5, pady=5, sticky='E') # display menu button in frame

root.mainloop()
