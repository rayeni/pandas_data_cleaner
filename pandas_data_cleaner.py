# Library for numerical analysis
import numpy as np
# Library for data management
import pandas as pd

# Libraries for gui development
import tkinter as tk
import tkinter.font as font
from tkinter import ttk, END, StringVar, IntVar, \
messagebox, filedialog, messagebox

# Library to create image
from PIL import ImageTk, Image

# Library to assist in finding files on windows machines
from pathlib import Path

# -- Windows only configuration --
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
# -- End Windows only configuration --

# Variables
df = pd.DataFrame() # create empty dataframe
my_dir = Path(__file__).parent # needed to address .ico file not found error

####################################
#         FUNCTIONS BEGIN          #
####################################
def import_from_csv():
    '''Import csv file into dataframe'''

    # Get path/location of csv file to import
    csv_file = filedialog.askopenfilename(
        initialdir="./", 
        title="Open CSV", 
        filetypes=(("CSV Files", "*.csv"),("All Files","*.*")))
    
    # Set df variable as global variable to enable functions to modify it
    global df 

    # Read csv into global df variable
    df = pd.read_csv(csv_file)

    # Give user confirmation that csv file was imported.
    if len(df) > 0:
        messagebox.showinfo(title="Load CSV", message='CSV file loaded successfully.')
    else:
        messagebox.showerror(title='Error', message='Error loading CSV file.')
    print(df.head())
    print()
    print(df.dtypes)

def export_to_csv():
    '''Export dataframe to csv file'''

    # Get name of csv file and where it should be exported
    csv_name = filedialog.asksaveasfilename(
        initialdir="./", 
        title="Export to CSV", 
        filetypes=(("CSV Files","*.csv"),("All Files","*.*")))
    
    # Set df variable as global variable to enable functions to modify it
    global df

    # Export dataframe to csv file
    df.to_csv(csv_name, index=False)

    # Confirmation of export to csv file
    messagebox.showinfo(title="CSV Export", message='DataFrame exported to CSV.')

def close_app():
    '''Close application'''

    # Use messagebox to ask to close application
    question = messagebox.askyesno("Close Pandas Data Cleaner", "Are you sure you want to exit?")
    if question == 1:
        root.destroy()

def drop_all_nulls():
    global df
    if len(df) == 0: # check if dataframe is loaded
        messagebox.showerror(title="No Data Present", message='Please load CSV file.')
    else:
        num_of_nulls = int(df.isnull().sum().sum())
        question = messagebox.askyesno("Drop Nulls", f"Drop {num_of_nulls} nulls?")
        if question == 1:
            df.dropna(inplace = True)
            messagebox.showinfo(title="Drop Nulls", message=f'{num_of_nulls} nulls dropped.')

def fill_all_nulls(value):
    global df
    num_of_nulls = int(df.isnull().sum().sum())
    question = messagebox.askyesno(
        "Impute Nulls", 
        f"Impute {num_of_nulls} nulls with {value}?")
    if question == 1:
        df.fillna(value, inplace=True)
        messagebox.showinfo(title="Impute Nulls", message=f'{num_of_nulls} nulls imputed.')

def open_fill_all_nulls_window():
    global df
    if len(df) == 0: # check if dataframe is loaded
        messagebox.showerror(title="No Data Present", message='Please load CSV file.')
    else:       
        # Create variable to hold fillna value
        fillna_all_value = tk.StringVar()

        # Create window
        fillna_all_window = tk.Toplevel(root)
        fillna_all_window.geometry('600x120')
        try:
            fillna_all_window.iconbitmap('./images/panda.ico')
        except:
            fillna_all_window.iconbitmap(my_dir / './images/panda.ico')
        fillna_all_window.resizable(0,0)
        fillna_all_window.title('Fill All Nulls in DataFrame')
        #fillna_all_window.columnconfigure(0, weight=1)

        # Create frame for window
        fillna_all_frame = tk.Frame(fillna_all_window, bg='#1ac6ff', width=600, height=120)
        fillna_all_frame.columnconfigure((0,1), weight=1)
        #fillna_all_frame.rowconfigure(0, weight=1)
        fillna_all_frame.pack(padx=5, pady=5)
        fillna_all_frame.grid_propagate(0)

        # Create label and display in frame
        fillna_all_label = ttk.Label(
            fillna_all_frame, 
            background='#1ac6ff',
            width=20,
            text='Enter value to fill nulls:'
            )
        fillna_all_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create entry widget and display in frame
        fillna_all_input = ttk.Entry(
            fillna_all_frame, 
            textvariable=fillna_all_value,
            justify='center',
            #width=5,
            font=('Segoe UI', 15)
            )
        fillna_all_input.grid(row=0, column=1, padx=5, pady=5, sticky='EW')
        fillna_all_input.focus()

        # Create button widget to fill nulls
        fillna_all_btn = ttk.Button(
            fillna_all_frame,
            text='FillNA',
            command=lambda: fill_all_nulls(fillna_all_value.get())
            )
        fillna_all_btn.grid(row=1, column=0, padx=5, pady=5)

        # Create button widget to fill nulls
        fillna_all_close_btn = ttk.Button(
            fillna_all_frame,
            text='Close',
            command=fillna_all_window.destroy
            )
        fillna_all_close_btn.grid(row=1, column=1, padx=5, pady=5)

        fillna_all_window.grab_set()

def open_drop_cols_window():
    global df
    # Check if dataframe is loaded.  If it's not loaded, notify user and exit function
    if len(df) == 0: 
        messagebox.showerror(title="No Data Present", message='Please load CSV file.')
    else:
        # Inner function that accesses same variables as parent function-- open_drop_cols_window
        def drop_columns():
            col_list = [col_listbox.get(i) for i in col_listbox.curselection()]
            df.drop(columns=col_list, inplace=True)

        # Create window
        dc_window = tk.Toplevel(root, bg='#1ac6ff')
        dc_window.geometry('550x500')
        try:
            dc_window.iconbitmap('./images/panda.ico')
        except:
            dc_window.iconbitmap(my_dir / './images/panda.ico')
        dc_window.resizable(0,0)
        dc_window.title('Drop Columns')

        # Create left frame for label and listbox
        left_frame = tk.Frame(dc_window, bg='#1ac6ff', width=300, height=500)
        #left_frame.columnconfigure((0,1), weight=1)
        #left_frame.rowconfigure(0, weight=1)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)

        # Create right frame for buttons
        right_frame = tk.Frame(dc_window, bg='#1ac6ff', width=250, height=500)
        #right_frame.columnconfigure((0,1), weight=1)
        #right_frame.rowconfigure(0, weight=1)
        right_frame.grid(row=0, column=1, padx=5, pady=5)
        right_frame.grid_propagate(0)

        # Create list box to place at top of left frame
        # Get column indexes
        col_idxs = df.columns
        # convert index to tuple
        cols = tuple(col_idxs)
        # listbox String Variable
        col_list_var = tk.StringVar(value=cols)
        # listbox
        col_listbox = tk.Listbox(left_frame, listvariable=col_list_var, selectmode='extended')
        # Display listbox in frame
        col_listbox.grid(row=0, column=0, padx=0, pady=5, sticky='NS')

        # Create scrollbar for listbox
        lb_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=col_listbox.yview)
        lb_scroll.grid(row=0, column=1, pady=5, sticky='NS')
        col_listbox['yscrollcommand'] = lb_scroll.set
        
        # Create a label to place at bottom of left frame 
        # indicating multiple columns can be selected
        listbox_label = ttk.Label(
            left_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 12),
            text='To select multiple columns,\nhold the Ctrl button'
            )
        listbox_label.grid(row=1, column=0, padx=0, pady=5, sticky='W')

        # Create buttons and display in frame
        dc_dropcols_btn = ttk.Button(right_frame, text='Drop Columns', width=15, command=drop_columns)
        dc_dropcols_btn.grid(row=0, column=0, padx=5, pady=5, sticky='E')

        dc_close_btn = ttk.Button(right_frame, text='Close', width=15, command=dc_window.destroy)
        dc_close_btn.grid(row=1, column=0, padx=5, pady=5, sticky='E')

        # Disable root window
        dc_window.grab_set()

def open_impute_nulls_window_mean():
    '''impute nulls with mean, median, or mode'''

    # Create window
    impute_null_mean_window = tk.Toplevel(root, bg='#1ac6ff')
    impute_null_mean_window.geometry('550x500')
    try:
        impute_null_mean_window.iconbitmap('./images/panda.ico')
    except:
        impute_null_mean_window.iconbitmap(my_dir / './images/panda.ico')
    impute_null_mean_window.resizable(0,0)
    impute_null_mean_window.title('Impute Nulls with Mean')

    # Create left frame for label and listbox
    left_frame = tk.Frame(impute_null_mean_window, bg='#1ac6ff', width=300, height=500)
    #left_frame.columnconfigure((0,1), weight=1)
    #left_frame.rowconfigure(0, weight=1)
    left_frame.grid(row=0, column=0, padx=5, pady=5)
    left_frame.grid_propagate(0)

    # Create right frame for buttons
    right_frame = tk.Frame(impute_null_mean_window, bg='#1ac6ff', width=250, height=500)
    #right_frame.columnconfigure((0,1), weight=1)
    #right_frame.rowconfigure(0, weight=1)
    right_frame.grid(row=0, column=1, padx=5, pady=5)
    right_frame.grid_propagate(0)

    # Create listbox and put in left frame
    # Get column indexes
    col_idxs = df.columns
    # convert index to tuple
    cols = tuple(col_idxs)
    # listbox String Variable
    col_list_var = tk.StringVar(value=cols)
    # listbox
    col_listbox = tk.Listbox(left_frame, listvariable=col_list_var, selectmode='extended')
    # Display listbox in frame
    col_listbox.grid(row=0, column=0, padx=0, pady=5, sticky='NS')

    # Create scrollbar for listbox
    lb_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=col_listbox.yview)
    lb_scroll.grid(row=0, column=1, pady=5, sticky='NS')
    col_listbox['yscrollcommand'] = lb_scroll.set

    # Create a label to place at bottom of left frame 
    # indicating multiple columns can be selected
    listbox_label = ttk.Label(
        left_frame, 
        background='#1ac6ff',
        font = ('Segoe UI', 12),
        text='To select multiple columns,\nhold the Ctrl button'
        )
    listbox_label.grid(row=1, column=0, padx=0, pady=5, sticky='W')

    # Create buttons and put in right frame
    impute_with_mean_btn = ttk.Button(right_frame, text='Impute w/Mean', width=16, command='')
    impute_with_mean_btn.grid(row=0, column=0, padx=5, pady=5, sticky='E')

    impute_with_mode_btn = ttk.Button(right_frame, text='Impute w/Mode', width=16, command='')
    impute_with_mode_btn.grid(row=1, column=0, padx=5, pady=5, sticky='E')

    impute_with_median_btn = ttk.Button(right_frame, text='Impute w/Median', width=16, command='')
    impute_with_median_btn.grid(row=2, column=0, padx=5, pady=5, sticky='E')

    close_btn = ttk.Button(right_frame, text='Close', width=16, command='')
    close_btn.grid(row=3, column=0, padx=5, pady=5, sticky='E')

    # Disable root window
    impute_null_mean_window.grab_set()

    
####################################
#           FUNCTIONS END          #
####################################


####################################
#           ROOT WINDOW            #
####################################
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

####################################
#            ROOT FRAMES           #
####################################
# Create logo frame
logo_frame = tk.Frame(root, bg='#1ac6ff', width=800, height=70)
logo_frame.columnconfigure(0, weight=1)
logo_frame.pack(padx=5, pady=0)
logo_frame.pack_propagate(0)

# Create top level frame
top_frame = tk.Frame(root, bg='#1ac6ff', width=800, height=70)
top_frame.columnconfigure((0,1,2), weight=1)
top_frame.pack(padx=5, pady=0)
top_frame.grid_propagate(0)

# Create functionality frame, func_frame_1
func_frame_1 = tk.Frame(root, bg='#1ac6ff', width=800, height=70)
func_frame_1.columnconfigure((0,1,2), weight=1)
func_frame_1.pack(padx=5, pady=0)
func_frame_1.grid_propagate(0)

####################################
#   WIDGETS TO GO IN ROOT FRAMES   #
####################################

'''
Logo label is created here and
goes in the frame, logo_frame
'''
try:
    logo = ImageTk.PhotoImage(Image.open('./images/logo.png'))
except:
    logo = ImageTk.PhotoImage(Image.open(my_dir / './images/logo.png'))
logo_label = tk.Label(logo_frame, bg='#1ac6ff', image=logo)
logo_label.pack()

'''
The buttons to import csv, export dataframe, 
and to close the app are created here and added
to the frame, top_frame
'''
# Create import button to import CSV file
import_data = ttk.Button(top_frame, text='Import from CSV', width=17, command=import_from_csv)
# Add import button to frame
import_data.grid(row=0, column=0, padx=5, pady=5, sticky='W')
# Create export button to export Dataframe to CSV file
export_data = ttk.Button(top_frame, text='Export to CSV', width=17, command=export_to_csv)
# Add export button to frame
export_data.grid(row=0, column=1, padx=5, pady=5)
# Create close button to close application
close_root = ttk.Button(top_frame, text='Close App', width=17, command=close_app)
# Add close button to frame
close_root.grid(row=0, column=2, padx=5, pady=5, sticky='E')

'''
The remaining widgets are menu buttons that present the user with
data cleaning options.  The menu buttons are added to the frame,
func_frame_1
'''
# ---FIRST MENU BUTTON--- #

# Create "Missing Data" menu button
mb_missing_data = ttk.Menubutton(func_frame_1, text='Missing Data', width=15)
# Create "Missing Data" menu
menu_missing_data = tk.Menu(mb_missing_data, tearoff=False) 
# Create "Drop nulls" menu option
menu_missing_data.add_command(
    label='Drop Nulls (All)', 
    font=("Segoe UI", 15), 
    command=drop_all_nulls)
# Create "Fill NA (All)" menu option
menu_missing_data.add_command(
    label='Fill Nulls (All)', 
    font=("Segoe UI", 15), 
    command=open_fill_all_nulls_window)

# Create "Impute Nulls with Mean" menu option
menu_missing_data.add_command(
    label='Impute Nulls w/Mean', 
    font=("Segoe UI", 15), 
    command=open_impute_nulls_window_mean)

# Associate menu with menu button
mb_missing_data["menu"] = menu_missing_data

# Display menu button in frame
mb_missing_data.grid(row=0, column=0, padx=5, pady=5, sticky='W')

# ---NEXT MENU BUTTON--- #

# Create DataFrame Tasks menu button
mb_df_tasks = ttk.Menubutton(func_frame_1, text='DataFrame Tasks', width=15)
# Create DataFrame Tasks menu
menu_df_tasks = tk.Menu(mb_df_tasks, tearoff=False)
# Create Drop Columns menu option
menu_df_tasks.add_command(
    label='Drop Columns', 
    font=("Segoe UI", 15), 
    command=open_drop_cols_window)

# Associate menu with menu button
mb_df_tasks["menu"] = menu_df_tasks
# Display menu button in frame
mb_df_tasks.grid(row=0, column=1, padx=5, pady=5) 

# ---NEXT MENU BUTTON--- #

# Create Clean Numerics data menu button
mb_clean_numeric = ttk.Menubutton(func_frame_1, text='Clean Numerics', width=15)
# Create Clean Numerics menu
menu_clean_numeric = tk.Menu(mb_clean_numeric, tearoff=False)
# Create _________ menu option
menu_clean_numeric.add_command(
    label='') # add command

# Associate menu with menu button
mb_clean_numeric["menu"] = menu_clean_numeric 
# Display menu button in frame
mb_clean_numeric.grid(row=0, column=2, padx=5, pady=5, sticky='E') 

root.mainloop()
