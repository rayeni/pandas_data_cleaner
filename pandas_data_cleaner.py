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
            # Get the selected listbox items and put in a list
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
    global df
    # Check if dataframe is loaded.  If it's not loaded, notify user and exit function
    if len(df) == 0: 
        messagebox.showerror(title="No Data Present", message='Please load CSV file.')
    else:
        # Inner function that accesses same variables as parent function-- open_drop_cols_window
        def impute_with_mmm(impute_method):
            # Get the selected listbox items and put in a list
            col_list = [col_listbox.get(i) for i in col_listbox.curselection()]
            col_str = ', '.join(col_list)
            # Loop through col_list to impute each column with selected value (i.e., mean, mode, median)
            for col in col_list:
                if impute_method == 'mean':
                    col_mean = round(df[col].mean(), 1)
                    df[col].fillna(col_mean, inplace=True)
                elif impute_method == 'mode':
                    col_mode = round(df[col].mode(), 1)
                    df[col].fillna(col_mode, inplace=True)
                else:
                    col_median = round(df[col].median(), 1)
                    df[col].fillna(col_median, inplace=True)

            messagebox.showinfo(title="Impute with MMM", 
            message=f'Column(s) {col_str} imputed with {impute_method}.')

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
        # Create series to find numeric columns with nulls: https://stackoverflow.com/a/36226137
        s = df.select_dtypes(include=['float64', 'int64']).isnull().any()
        # The series comprises of True and False values.  Use boolean indexing to get the
        # indexes (i.e., the column names): https://stackoverflow.com/a/52173171
        # convert the index to a list.
        cols_list = s[s].index.to_list()
        # convert list to tuple
        cols_tuple = tuple(cols_list)
        # listbox String Variable
        col_list_var = tk.StringVar(value=cols_tuple)
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
        impute_with_mean_btn = ttk.Button(
            right_frame,
            text='Impute w/Mean',
            width=16, command=lambda: impute_with_mmm('mean')
            )
        impute_with_mean_btn.grid(row=0, column=0, padx=5, pady=5, sticky='E')

        impute_with_mode_btn = ttk.Button(
            right_frame,
            text='Impute w/Mode',
            width=16, 
            command=lambda: impute_with_mmm('mode')
            )
        impute_with_mode_btn.grid(row=1, column=0, padx=5, pady=5, sticky='E')

        impute_with_median_btn = ttk.Button(
            right_frame, 
            text='Impute w/Median', 
            width=16, command=lambda: impute_with_mmm('median')
            )
        impute_with_median_btn.grid(row=2, column=0, padx=5, pady=5, sticky='E')

        close_btn = ttk.Button(
            right_frame, 
            text='Close', 
            width=16, 
            command=impute_null_mean_window.destroy
            )
        close_btn.grid(row=3, column=0, padx=5, pady=5, sticky='E')

        # Disable root window
        impute_null_mean_window.grab_set()

def open_binary_class_window():
    global df

    # Check if dataframe is loaded.  If it's not loaded, notify user and exit function
    if len(df) == 0: 
        messagebox.showerror(title="No Data Present", message='Please load CSV file.')
    else:
        def column_selection(event):
            # Get the index of the listbox item (i.e. column name)
            selected_index = col_listbox.curselection()
            # Use index to get listbox item (i.e., column name)
            column_name = (col_listbox.get(selected_index))
            # Update the labels with the column values
            col_val_1.set(a_dict[column_name][0])
            col_val_2.set(a_dict[column_name][1])
        
        def category_selection_0(event):
            if selected_category_0.get() == 0:
                selected_category_1.set(1)
            elif selected_category_0.get() == 1:
                selected_category_1.set(0)

        def category_selection_1(event):
            if selected_category_1.get() == 0:
                selected_category_0.set(1)
            elif selected_category_1.get() == 1:
                selected_category_0.set(0)

        def categorize_target(target_col, value_1, category_1, value_2, category_2):
            global df
            df[target_col] = df[target_col].map({value_1: category_1, value_2: category_2})

                
        # Create window
        binary_class_window = tk.Toplevel(root, bg='#1ac6ff')
        binary_class_window.geometry('650x500')
        try:
            binary_class_window.iconbitmap('./images/panda.ico')
        except:
            binary_class_window.iconbitmap(my_dir / './images/panda.ico')
        binary_class_window.resizable(0,0)
        binary_class_window.title('Binary Classification of Target')

        # Set combobox font for the window.  
        # https://stackoverflow.com/a/28940421
        cb_font = font.Font(family="Segoe UI",size=13)
        binary_class_window.option_add("*Font", cb_font)     

        # Create left frame for label and listbox
        left_frame = tk.Frame(binary_class_window, bg='#1ac6ff', width=300, height=500)
        #left_frame.columnconfigure((0,1), weight=1)
        #left_frame.rowconfigure(0, weight=1)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)

        # Create right frame for buttons
        right_frame = tk.Frame(binary_class_window, bg='#1ac6ff', width=350, height=500)
        #right_frame.columnconfigure((0,1), weight=1)
        #right_frame.rowconfigure(0, weight=1)
        right_frame.grid(row=0, column=1, padx=5, pady=5)
        right_frame.grid_propagate(0)

        # The following creates a listbox and puts it in the left frame
        # - Get columns that are strings
        str_cols = df.select_dtypes(include=['object']).columns.to_list()

        # - From the columns that are strings, 
        #   get the ones that have only two values
        #   and put in a list, bin_cols
        bin_cols = [col for col in str_cols if len(df[col].unique()) == 2]

        # - Convert list to a tuple
        cols_tuple = tuple(bin_cols)

        # - Create listbox String variable
        col_list_var = tk.StringVar(value=cols_tuple)

        # - Create listbox, and set select mode to browse (single selection only)
        col_listbox = tk.Listbox(
            left_frame, 
            listvariable=col_list_var, 
            selectmode='browse',
            exportselection=False
            )

        # - Display listbox in frame
        col_listbox.grid(row=0, column=0, padx=0, pady=5, sticky='NS')

        # - Bind listbox to column_selection function.  The enables the listbox to monitor
        #   column selection and to change to label accordingly.
        col_listbox.bind('<<ListboxSelect>>', column_selection)

        # Create scrollbar for listbox
        lb_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=col_listbox.yview)
        lb_scroll.grid(row=0, column=1, pady=5, sticky='NS')
        col_listbox['yscrollcommand'] = lb_scroll.set

        # Create dictionary for columns and their unique values (e.g., 'yes' and 'no')
        # This dictionary is needed to dynamically populate the labels as 
        # the user selects a column from the listbox
        a_dict = {}
        for col in bin_cols:
            a_dict[col] = df[col].unique().tolist()
                
        # The following creates labels to display column values
        #
        # - Create string variables for value #1 and value #2
        col_val_1 = tk.StringVar()
        col_val_2 = tk.StringVar()

        # - Create labels and display in right frame
        value1_label = ttk.Label(
            right_frame,
            background='#ffffff',
            font = ('Segoe UI', 12),
            textvariable=col_val_1,
            width=15
            )
        value1_label.grid(row=0, column=0, padx=5, pady=5)

        value2_label = ttk.Label(
            right_frame,
            background='#ffffff',
            font = ('Segoe UI', 12),
            textvariable=col_val_2,
            width=15
            )
        value2_label.grid(row=1, column=0, padx=5, pady=5)

        # The following creates comboboxes to hold binary values for target column
        #
        # - Refernce the following variables that were created outside of this function
        #   immediately after the creation of the root window.

        global selected_category_0 # references the global IntVar
        global selected_category_1 # references the global IntVar
        
        # - Create first combobox to hold category and display it in right_frame
        cb_category_0 = ttk.Combobox(
            right_frame,
            textvariable=selected_category_0,
            values=(0, 1),
            state='readonly',
            width=2,
            exportselection=False
            )
        cb_category_0.current(0)
        cb_category_0.grid(row=0, column=1, padx=5, pady=5)

        # - Create second combobox to hold category and display in right_frame
        cb_category_1 = ttk.Combobox(
            right_frame,
            textvariable=selected_category_1,
            values=(0, 1),
            state='readonly',
            width=2,
            exportselection=False
            )
        cb_category_1.current(1)
        cb_category_1.grid(row=1, column=1, padx=5, pady=5)

        # - Bind clickboxes to functions
        cb_category_0.bind('<<ComboboxSelected>>', category_selection_0)
        cb_category_1.bind('<<ComboboxSelected>>', category_selection_1)

        # The following creates a button to categorize target values
        categorize_btn = ttk.Button(
            right_frame,
            text='Categorize Target',
            width=16,
            command=lambda: categorize_target(
                col_listbox.get(col_listbox.curselection()),
                col_val_1.get(), 
                selected_category_0.get(), 
                col_val_2.get(),
                selected_category_1.get())
                )

        categorize_btn.grid(row=2, column=0, padx=5, pady=5)
        # Disable root window
        binary_class_window.grab_set()

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

# Set the following global variable to hold iniital values 
# in the comboboxes that are created in the 
# open_binary_class_window function. 
# Normally, these IntVars would be defined in the
# aforementioned function.  However, due to 
# garbage collection, the default values are
# erased program exits the function when these variables
# are defined in the function.
# Explnation can be found at: https://stackoverflow.com/a/6879450

selected_category_0 = tk.IntVar() # referenced in open_binary_class_window function
selected_category_1 = tk.IntVar() # referenced in open_binary_class_window function


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
func_frame_1 = tk.Frame(root, bg='#1ac6ff', width=800, height=150)
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
# ---FIRST MENU BUTTON (MISSING DATA) --- #

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

# ---SECOND MENU BUTTON (DATAFRAME TASKS) --- #

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

# ---THIRD MENU BUTTON (CLEAN NUMERICS) --- #

# Create Clean Numerics menu button
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

# ---FOURTH MENU BUTTON (CATEGORIZE DATA) --- #

# Create Categorize Data menu button
mb_categorize_data = ttk.Menubutton(func_frame_1, text='Categorize Data', width=15)
# Create Categorize Data menu
menu_categorize_data = tk.Menu(mb_categorize_data, tearoff=False)
# Create Target Classfication (Binary) menu option
menu_categorize_data.add_command(
    label='Target Classification (Binary)', 
    font=("Segoe UI", 15), 
    command=open_binary_class_window)

# Associate menu with menu button
mb_categorize_data["menu"] = menu_categorize_data 
# Display menu button in frame
mb_categorize_data.grid(row=1, column=0, padx=5, pady=10, sticky='W') 

root.mainloop()
