# Library for numerical analysis
from tkinter.constants import WORD
import numpy as np
# Library for data management
import pandas as pd

# Libraries for gui development
import tkinter as tk
import tkinter.font as font
from tkinter import ttk, END, StringVar, IntVar, \
messagebox, filedialog

# Library to create images
from PIL import ImageTk, Image

# Library to assist in finding files on windows machines
from pathlib import Path

# Windows only configuration to improve font resolution
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# Variables
# Variable for dataframe to be accessed globally
df = pd.DataFrame()
# Variable for parent directory to address .ico file not found error
my_dir = Path(__file__).parent

class PandaDataCleaner(tk.Tk):
    def __init__(self):
        super().__init__()

        # Change window title
        self.title('Pandas Data Cleaner')
        try:
            # Set window icon
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        # Set window dimensions
        self.geometry("800x600")
        # Disable resizing window
        self.resizable(False, False)
        self.configure(bg='#1ac6ff')

        # Create logo frame
        logo_frame = tk.Frame(self, bg='#1ac6ff', width=800, height=70)
        logo_frame.columnconfigure(0, weight=1)
        logo_frame.pack(padx=5, pady=0)
        logo_frame.pack_propagate(0)

        # Create top level frame
        top_frame = tk.Frame(self, bg='#1ac6ff', width=800, height=70)
        top_frame.columnconfigure((0,1,2), weight=1)
        top_frame.pack(padx=5, pady=0)
        top_frame.grid_propagate(0)

        # Create functionality frame, func_frame_1
        func_frame_1 = tk.Frame(self, bg='#1ac6ff', width=800, height=150)
        func_frame_1.columnconfigure((0,1,2), weight=1)
        func_frame_1.pack(padx=5, pady=0)
        func_frame_1.grid_propagate(0)

        # Menu button font
        menu_option_font = 14

        #--- Add widgets ---#
        '''
        Logo label is created here and
        goes in the frame, logo_frame
        '''
        try:
            self.logo = ImageTk.PhotoImage(Image.open('./images/logo.png'))
        except:
            self.logo = ImageTk.PhotoImage(Image.open(my_dir / './images/logo.png'))
        logo_label = tk.Label(logo_frame, bg='#1ac6ff', image=self.logo)
        logo_label.pack()

        '''
        The buttons to import csv, export dataframe, 
        and to close the app are created here and added
        to the frame, top_frame
        '''
        # Create import button to import CSV file
        import_data = ttk.Button(top_frame, text='Import from CSV', width=17, command=self.import_from_csv)
        # Add import button to frame
        import_data.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        # Create export button to export Dataframe to CSV file
        export_data = ttk.Button(top_frame, text='Export to CSV', width=17, command=self.export_to_csv)
        # Add export button to frame
        export_data.grid(row=0, column=1, padx=5, pady=5)
        # Create close button to close application
        close_root = ttk.Button(top_frame, text='Close App', width=17, command=self.close_app)
        # Add close button to frame
        close_root.grid(row=0, column=2, padx=5, pady=5, sticky='E')

        '''
        The remaining widgets are menu buttons that present the user with
        data cleaning options.  The menu buttons are added to the frame,
        func_frame_1
        '''
        # ---FIRST MENU BUTTON (MISSING DATA), First Row, First Column--- #

        # Create "Missing Data" menu button
        mb_missing_data = ttk.Menubutton(func_frame_1, text='Fix Missing Data', width=15)
        # Create "Missing Data" menu
        menu_missing_data = tk.Menu(mb_missing_data, tearoff=False) 
        # Create "Drop nulls" menu option
        menu_missing_data.add_command(
            label='Drop Nulls (All)', 
            font=("Segoe UI", menu_option_font), 
            command=self.drop_all_nulls)

        # Create "Fill NA (All)" menu option
        menu_missing_data.add_command(
            label='Fill Nulls (All)', 
            font=("Segoe UI", menu_option_font), 
            command=self.open_fill_all_nulls_window)

        # Create "Impute Nulls with Mean" menu option
        menu_missing_data.add_command(
            label='Impute Nulls w/Mean', 
            font=("Segoe UI", menu_option_font), 
            command=self.open_impute_nulls_with_mean_window)

        # Associate menu with menu button
        mb_missing_data["menu"] = menu_missing_data

        # Display menu button in frame
        mb_missing_data.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # ---SECOND MENU BUTTON (DATAFRAME TASKS), First Row, Second Column--- #

        # Create DataFrame Tasks menu button
        mb_df_tasks = ttk.Menubutton(func_frame_1, text='DataFrame Tasks', width=15)
        # Create DataFrame Tasks menu
        menu_df_tasks = tk.Menu(mb_df_tasks, tearoff=False)
        # Create Drop Columns menu option
        menu_df_tasks.add_command(
            label='Drop Columns', 
            font=("Segoe UI", menu_option_font), 
            command=self.open_drop_cols_window)

        # Associate menu with menu button
        mb_df_tasks["menu"] = menu_df_tasks
        # Display menu button in frame
        mb_df_tasks.grid(row=0, column=1, padx=5, pady=5) 

        # ---THIRD MENU BUTTON (CLEAN NUMERICS) First Row, Third Column--- #

        # Create Clean Numerics menu button
        mb_clean_numeric = ttk.Menubutton(func_frame_1, text='Clean Num Data', width=15)
        # Create Clean Numerics menu
        menu_clean_numeric = tk.Menu(mb_clean_numeric, tearoff=False)
        # Create Numeric Text -> Int menu option
        menu_clean_numeric.add_command(
            label='Numeric Text -> Int',
            font=('Segoe UI', menu_option_font),
            command='')
        menu_clean_numeric.add_command(
            label='Remove % Signs',
            font=('Segoe UI', menu_option_font),
            command=self.open_remove_pcts_window) 

        # Associate menu with menu button
        mb_clean_numeric["menu"] = menu_clean_numeric 
        # Display menu button in frame
        mb_clean_numeric.grid(row=0, column=2, padx=5, pady=5, sticky='E')

        # ---FOURTH MENU BUTTON (CATEGORIZE DATA), Second Row, First Column --- #

        # Create Categorize Data menu button
        mb_categorize_data = ttk.Menubutton(func_frame_1, text='Categorize Data', width=15)

        # Create Categorize Data menu
        menu_categorize_data = tk.Menu(mb_categorize_data, tearoff=False)

        # Create Target Classfication (Binary) menu option
        menu_categorize_data.add_command(
            label='Classify Target (0/1)', 
            font=("Segoe UI", menu_option_font), 
            command=self.open_binary_class_window)

        # Create Target Classfication (Binary) menu option
        menu_categorize_data.add_command(
            label='Dummify Columns', 
            font=("Segoe UI", menu_option_font), 
            command=self.open_dummify_columns_window)

        # Associate menu with menu button
        mb_categorize_data["menu"] = menu_categorize_data 
        # Display menu button in frame
        mb_categorize_data.grid(row=1, column=0, padx=5, pady=10, sticky='W')

        # ---FIFTH MENU BUTTON (Clean Strings), Second Row, Second Column--- #

        # Create Clean String Data menu button
        mb_clean_string = ttk.Menubutton(func_frame_1, text='Clean String Data', width=15)
        # Create Clean String Data menu
        menu_clean_string = tk.Menu(mb_clean_string, tearoff=False)
        # Create Remove Trailing/Leading Spaces menu option
        menu_clean_string.add_command(
            label='Remove Trailing/Leading Spaces', 
            font=("Segoe UI", menu_option_font), 
            command=self.remove_trailing_leading_spaces)

        # Associate menu with menu button
        mb_clean_string["menu"] = menu_clean_string
        # Display menu button in frame
        mb_clean_string.grid(row=1, column=1, padx=5, pady=5)
    
    def import_from_csv(self):
        '''Import csv file into dataframe'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Get path/location of csv file to import
        csv_file = filedialog.askopenfilename(
            initialdir="./", 
            title="Open CSV", 
            filetypes=(("CSV Files", "*.csv"),("All Files","*.*")))
        
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

    def export_to_csv(self):
        '''Export dataframe to csv file'''

        # Set df variable as global variable to enable all functions to modify it
        global df
        
        # Get name of csv file and where it should be exported
        csv_name = filedialog.asksaveasfilename(
            initialdir="./", 
            title="Export to CSV", 
            filetypes=(("CSV Files","*.csv"),("All Files","*.*")))
        
        # Export dataframe to csv file
        df.to_csv(csv_name, index=False)

        # Confirmation of export to csv file
        messagebox.showinfo(title="CSV Export", message='DataFrame exported to CSV.')

    def close_app(self):
        '''Close application'''

        # Use messagebox to ask to close application
        question = messagebox.askyesno("Close Pandas Data Cleaner", "Are you sure you want to exit?")
        if question == 1:
            self.destroy()

    def drop_all_nulls(self):
        '''Drop all nulls unconditionally'''

        # Set df variable as global variable to enable all functions to modify it
        global df
        
        # Check if dataframe is loaded. If it's not loaded exit drop operation
        if len(df) == 0: 
            messagebox.showerror(title="No Data Present", message='Please load CSV file.')
        else:
            # Get number of nulls:
            num_of_nulls = int(df.isnull().sum().sum())
            if num_of_nulls == 0:
                messagebox.showinfo(title='No Nulls to Drop', message=f'There are no nulls to drop.')
            else:
                question = messagebox.askyesno("Drop Nulls", f"Drop {num_of_nulls} nulls?")
                if question == 1:
                    df.dropna(inplace = True)
                    messagebox.showinfo(title="Drop Nulls", message=f'{num_of_nulls} nulls dropped.')
    
    def remove_trailing_leading_spaces(self):
        '''Find and remove all trailing and leading spaces from strings'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded exit drop operation
        if len(df) == 0: 
            messagebox.showerror(title="No Data Present", message='Please load CSV file.')
        else:
            # Get all columns of type string/object and place in list
            obj_cols_list = df.select_dtypes(include='object').columns.to_list()
            
            # Get the total number of values before inspection of leading and trailing spaces
            total_before = sum([df[col].value_counts().sum()*df[col].value_counts().count() for col in obj_cols_list])

            # Strip any leading or trailing space from values
            for col in obj_cols_list:
                df[col] = df[col].str.strip()

            # Get the total number of values after the removal of leading and trailing spaces
            total_after = sum([df[col].value_counts().sum()*df[col].value_counts().count() for col in obj_cols_list])

            # Get the difference between number of values before and after
            total_diff = total_before - total_after

            # Notify user of result
            if total_diff == 0:
                messagebox.showinfo(title="Remove Trailing/Leading Spaces", 
                message=f'NO trailing/leading spaces were found.')
            elif total_diff == 1:
                messagebox.showinfo(title="Remove Trailing/Leading Spaces", 
                message=f'{total_diff} trailing/leading space has been removed.')
            else:
                messagebox.showinfo(title="Remove Trailing/Leading Spaces", 
                message=f'{total_diff} trailing/leading spaces have been removed.')

    def open_fill_all_nulls_window(self):
        '''Open Fill All Nulls window'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded exit drop operation
        if len(df) == 0:
            messagebox.showerror(title="No Data Present", message='Please load CSV file.')
        else:
            window = FillAllNullsWindow(self)
            window.grab_set()

    def open_impute_nulls_with_mean_window(self):
        '''Open Impute Nulls with Mean window'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded exit drop operation
        if len(df) == 0:
            messagebox.showerror(title="No Data Present", message='Please load CSV file.')
        else:
            window = ImputeNullsWithMean(self)
            window.grab_set()

    def open_drop_cols_window(self):
        '''Open Drop Columns window'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded exit drop operation
        if len(df) == 0:
            messagebox.showerror(title="No Data Present", message='Please load CSV file.')
        else:
            window = DropColumns(self)
            window.grab_set()

    def open_binary_class_window(self):
        '''Open Binary Classification window'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded exit drop operation
        if len(df) == 0:
            messagebox.showerror(title="No Data Present", message='Please load CSV file.')
        else:
            window = BinaryClassification(self)
            window.grab_set()

    def open_dummify_columns_window(self):
        '''Open Dummify Columns window'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded exit drop operation
        if len(df) == 0:
            messagebox.showerror(title="No Data Present", message='Please load CSV file.')
        else:
            window = DummifyColumns(self)
            window.grab_set()

    def open_remove_pcts_window(self):
        '''Open Remove Percents window'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded exit drop operation
        if len(df) == 0:
            messagebox.showerror(title="No Data Present", message='Please load CSV file.')
        else:
            window = RemovePercents(self)
            window.grab_set()

class RemovePercents(tk.Toplevel):
    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        super().__init__(root)

        # Set window properties
        self.geometry('550x650')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Remove Percent Signs')
        self.configure(bg='#1ac6ff')

        # Create left frame for listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=300, height=650)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)
        left_frame.grid_columnconfigure(0, weight=1)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=250, height=650)
        right_frame.grid(row=0, column=1, padx=5, pady=5)
        right_frame.grid_propagate(0)

        # The following creates a listbox and puts it in left frame
        # 1. Get the list of columns with which to populate listbox
        self.cols_list = self.get_col_list()

        # 2. Convert list to tuple, because tk.StringVar takes a tuple argument.
        cols_tuple = tuple(self.cols_list)
        
        # 3. Create tk.StringVar object for listbox and assign it to the col_list_var variable
        col_list_var = tk.StringVar(value=cols_tuple)

        # 4. Create listbox
        self.col_listbox = tk.Listbox(
            left_frame, 
            listvariable=col_list_var, 
            selectmode='browse',
            exportselection=False)
        
        # 5. Display listbox in frame
        self.col_listbox.grid(row=1, column=0, padx=0, pady=5, sticky='NSEW')

        # 6. Bind listbox to column_selection function.  When a column is selected, in the listbox,
        #    it's unique values are displayed in the text widget.
        self.col_listbox.bind('<<ListboxSelect>>', self.column_selection)

        # Create scrollbar for listbox
        lb_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.col_listbox.yview)
        lb_scroll.grid(row=1, column=1, pady=5, sticky='NSEW')
        self.col_listbox['yscrollcommand'] = lb_scroll.set

        # Create a label to place above the listbox 
        listbox_label = ttk.Label(
            left_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Numeric Cols with % Sign'
            )
        listbox_label.grid(row=0, column=0, padx=0, pady=5, sticky='W')

        # Create dictionary for columns and their unique values (e.g., 'yes' and 'no')
        # This dictionary is needed to dynamically populate the labels as 
        # the user selects a column from the listbox
        self.a_dict = {}

        # Populate the dictionary with columns and values
        self.populate_dict()

        # Create a label to place above the text widget 
        # that indicates that the widget displays values of the selected column
        column_values_label = ttk.Label(
            left_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Column Values'
            )
        column_values_label.grid(row=2, column=0, padx=0, pady=5, sticky='W')

        # Create a text widget to present the values when a column is selected.
        # Displaying values gives the user more insight into which impute method to use.
        self.column_values_text = tk.Text(
            left_frame, 
            font=("Segoe UI", 14), 
            height=4,
            wrap=WORD)
        self.column_values_text.grid(row=3, column=0, padx=0, pady=5, sticky='NSEW')
        
        # Create scrollbar for text widget
        text_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.column_values_text.yview)
        text_scroll.grid(row=3, column=1, pady=5, sticky='NSEW')
        self.column_values_text['yscrollcommand'] = text_scroll.set

        # Create a label to place above the action buttons 
        action_label = ttk.Label(
            right_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Action'
            )
        action_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create buttons and put in right frame
        remove_pct_sign_btn = ttk.Button(
            right_frame,
            text='Remove % Sign',
            width=16, command=lambda: self.remove_pct_sign()
            )
        remove_pct_sign_btn.grid(row=1, column=0, padx=5, pady=5, sticky='E')

        close_btn = ttk.Button(
            right_frame, 
            text='Close', 
            width=16, 
            command=self.destroy
            )
        close_btn.grid(row=4, column=0, padx=5, pady=5, sticky='E')

    def get_col_list(self):
        # get all columns that are of type object
        df1 = df.select_dtypes(include='object')
    
        # make copy of dataframe avoid SettingWithCopyWarning error
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
        df2 = df1.copy(deep=True)
    
        # get columns that contain a percent sign
        # https://thispointer.com/pandas-select-dataframe-columns-containing-string/
        mask = df2.apply(lambda col: col.str.contains('%').any(), axis=0)
        df3 = df2.loc[: , mask]
    
        # drop percent sign from dataframe.
        # this is needed to determine which columns contain majority numeric values
        df4 = df3.copy(deep=True)
        df4.replace('%', '', regex=True, inplace=True)
    
        # The presence of nulls will break the for loop, below
        df4.dropna(inplace=True)
    
        # place the column names in a list
        df4_col_list = df4.columns.to_list()
    
        # get total number of rows in df4.  This number is needed to determine
        # the ratio of numeric values to total values in column
        total_rows = df4.shape[0]
    
        # initialize a list to hold columns that have mostly numeric values and
        # have percent symbol in its values
        pct_cols = []
    
        # loop through df4_col_list to determine which column has a ratio of numeric values
        # to total values greater than 90%.  Chances are that the column is a percent column
        for col in df4_col_list:
            # get the number of column values that are numeric
            num_digits = df4[col].apply(lambda x: x.isnumeric()).sum()
            # if column has a majority of numeric values, add to list
            if num_digits / total_rows > 0.9:
                pct_cols.append(col)

        return pct_cols
    
    def column_selection(self, event):
        # Get the index of the listbox item
        selected_index = self.col_listbox.curselection()
        # Use index to get listbox item (i.e., column name)
        column_name = (self.col_listbox.get(selected_index))
        # Get columns' values
        list_of_values = self.a_dict[column_name]
        # Enable text widget
        self.column_values_text.config(state="normal")
        # Delete any text that may be in text widget
        self.column_values_text.delete("1.0","end")
        # Enter column name into to text widget
        self.column_values_text.insert(END, column_name + ' Values:  ')
        # Enter column's values into text widget
        for value in list_of_values:
            self.column_values_text.insert(END, str(value) + ', ')
        # Delete ending space from text widget
        self.column_values_text.delete("end-2c")
        # Delete ending comma from text widget
        self.column_values_text.delete("end-2c")
        # Disable text widget
        self.column_values_text.config(state="disabled")

    def populate_dict(self):
        # clear dictionary
        self.a_dict = {}
        # populate dictionary with initial or updated keys (i.e., column names) and 
        # values (i.e., list of unique column values)
        for col in self.cols_list:
            self.a_dict[col] = df[col].sort_values(na_position='first').unique().tolist()

    def convert_pct_to_num(self, x):
        x = x.replace('%','')
        return int(x)/100

    def remove_pct_sign(self):
        # Get the selected listbox items and put in a list
        col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
        col_str = ', '.join(col_list)
        # Loop through col_list to remove percent sign
        for col in col_list:
            df[col] = df[col].apply(self.convert_pct_to_num)
        
        # Update dictionary of column's values
        self.populate_dict()
        # Update text widget to show the updated changes
        self.column_selection(None)

        # Send confirmation
        messagebox.showinfo(title="Remove % Sign", 
        message=f'Percent removed from Column(s) {col_str} values.')

class DummifyColumns(tk.Toplevel):

    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        super().__init__(root)

        # Set window properties
        self.geometry('560x500')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Binary Classification of Target')
        self.configure(bg='#1ac6ff')

        # Create left frame for label and listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=300, height=500)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=250, height=500)
        right_frame.grid(row=0, column=1, padx=5, pady=5)
        right_frame.grid_propagate(0)

        # The following creates a listbox and puts it in the left frame
        # 1. Get columns that are strings
        dummy_cols = df.select_dtypes(include=['object']).columns.to_list()

        # 2. Convert list to a tuple
        cols_tuple = tuple(dummy_cols)

        # 3. Create String variable for listbox
        col_list_var = tk.StringVar(value=cols_tuple)

        # 4. Create listbox, and set select mode to browse (single selection only)
        self.col_listbox = tk.Listbox(
            left_frame, 
            listvariable=col_list_var, 
            selectmode='extended',
            exportselection=False
            )

        # 5 Display listbox in frame
        self.col_listbox.grid(row=0, column=0, padx=0, pady=5, sticky='NS')

        # Create scrollbar for listbox
        lb_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.col_listbox.yview)
        lb_scroll.grid(row=0, column=1, pady=5, sticky='NSEW')
        self.col_listbox['yscrollcommand'] = lb_scroll.set
        
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
        dummify_btn = ttk.Button(
            right_frame, 
            text='Dummify', 
            width=17, 
            command=self.dummify_columns)
        dummify_btn.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        dummify_drop_first_btn = ttk.Button(
            right_frame, 
            text='Dummify Drop First', 
            width=17, 
            command=self.dummify_columns_drop_first)
        dummify_drop_first_btn.grid(row=1, column=0, padx=5, pady=5, sticky='W')

        dc_close_btn = ttk.Button(
            right_frame, 
            text='Close', 
            width=17, 
            command=self.destroy)
        dc_close_btn.grid(row=2, column=0, padx=5, pady=5, sticky='W')

    def dummify_columns(self):
        global df
        # Get the selected listbox items and put in a list
        col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
        df = pd.get_dummies(df,columns=col_list, drop_first=True)
        messagebox.showinfo(title="Dummify Columns", message='Columns dummified.')
        
    def dummify_columns_drop_first(self):
        global df 
        # Get the selected listbox items and put in a list
        col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
        df = pd.get_dummies(df,columns=col_list, drop_first=True)
        messagebox.showinfo(title="Dummify Columns", message='Columns dummified.')

class BinaryClassification(tk.Toplevel):

    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        super().__init__(root)

        # Set window properties
        self.geometry('600x500')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Binary Classification of Target')
        self.configure(bg='#1ac6ff')

        # Set combobox font for the window.  
        # https://stackoverflow.com/a/28940421
        cb_font = font.Font(family="Segoe UI",size=12)
        self.option_add("*Font", cb_font)     

        # Create left frame for label and listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=250, height=500)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)

        # Create middle frame for labels (header and target values)
        middle_frame = tk.Frame(self, bg='#1ac6ff', width=175, height=500)
        middle_frame.grid(row=0, column=1, padx=5, pady=5)
        middle_frame.grid_propagate(0)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=125, height=500)
        right_frame.grid(row=0, column=2, padx=5, pady=5)
        right_frame.grid_propagate(0)

        # Header for listbox
        listbox_header_label = ttk.Label(
            left_frame,
            background='#1ac6ff',
            font = ('Segoe UI', 12),
            text='Select Target',
            width=12
            )
        listbox_header_label.grid(row=0, column=0, padx=5, pady=5, sticky='EW')

        # The following creates a listbox and puts it in the left frame
        # 1. Get columns that are strings
        str_cols = df.select_dtypes(include=['object']).columns.to_list()

        # 2. From the columns that are strings, 
        #    get the ones that have only two values
        #    and put in a list, bin_cols
        self.bin_cols = [col for col in str_cols if len(df[col].unique()) == 2]

        # 3. Convert list to a tuple
        cols_tuple = tuple(self.bin_cols)

        # 4. Create String variable for listbox
        col_list_var = tk.StringVar(value=cols_tuple)

        # 5. Create listbox, and set select mode to browse (single selection only)
        self.col_listbox = tk.Listbox(
            left_frame, 
            listvariable=col_list_var, 
            selectmode='browse',
            exportselection=False
            )

        # 6. Display listbox in frame
        self.col_listbox.grid(row=1, column=0, padx=0, pady=5, sticky='NS')

        # 7. Bind listbox to column_selection function.  This enables the listbox to monitor
        #    column selection and to change to label accordingly.
        self.col_listbox.bind('<<ListboxSelect>>', self.column_selection)

        # Create scrollbar for listbox
        lb_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.col_listbox.yview)
        lb_scroll.grid(row=1, column=1, pady=5, sticky='NSEW')
        self.col_listbox['yscrollcommand'] = lb_scroll.set

        # Create dictionary for columns and their unique values (e.g., 'yes' and 'no')
        # This dictionary is needed to dynamically populate the labels as 
        # the user selects a column from the listbox
        self.a_dict = {}

        # Populate the dictionary with columns and values
        self.populate_dict()
                
        # Header for Values
        values_header_label = ttk.Label(
            middle_frame,
            background='#1ac6ff',
            font = ('Segoe UI', 12),
            text='Values',
            width=12
            )
        values_header_label.grid(row=0, column=0, padx=5, pady=5, sticky='EW')

        # The following creates labels to display column values
        #
        # 1. Create string variables for value #1 and value #2
        self.col_val_1 = tk.StringVar()
        self.col_val_2 = tk.StringVar()

        # 2. Create labels and display in middle frame
        value1_label = ttk.Label(
            middle_frame,
            background='#ffffff',
            font = ('Segoe UI', 12),
            textvariable=self.col_val_1,
            width=15
            )
        value1_label.grid(row=1, column=0, padx=5, pady=5)

        value2_label = ttk.Label(
            middle_frame,
            background='#ffffff',
            font = ('Segoe UI', 12),
            textvariable=self.col_val_2,
            width=15
            )
        value2_label.grid(row=2, column=0, padx=5, pady=5)

        # Header for Categories (comboboxes)
        category_header_label = ttk.Label(
            right_frame,
            background='#1ac6ff',
            font = ('Segoe UI', 12),
            text='Category',
            width=12
            )
        category_header_label.grid(row=0, column=0, padx=5, pady=5)

        # The following creates comboboxes to hold binary values for target column
        
        # - Variable for first category (0 or 1)
        self.selected_category_0 = tk.IntVar()
        # - Variable for second category (0 or 1)
        self.selected_category_1 = tk.IntVar()
        
        # - Create first combobox to hold category and display it in right_frame
        cb_category_0 = ttk.Combobox(
            right_frame,
            textvariable=self.selected_category_0,
            values=(0, 1),
            state='readonly',
            width=2,
            exportselection=False
            )
        cb_category_0.current(0)
        cb_category_0.grid(row=1, column=0, padx=5, pady=5, sticky='W')

        # - Create second combobox to hold category and display in right_frame
        cb_category_1 = ttk.Combobox(
            right_frame,
            textvariable=self.selected_category_1,
            values=(0, 1),
            state='readonly',
            width=2,
            exportselection=False
            )
        cb_category_1.current(1)
        cb_category_1.grid(row=2, column=0, padx=5, pady=4, sticky='W')

        # - Bind clickboxes to functions
        cb_category_0.bind('<<ComboboxSelected>>', self.category_selection_0)
        cb_category_1.bind('<<ComboboxSelected>>', self.category_selection_1)

        # The following creates buttons to categorize target values and to close window
        # - Create button style
        btn_style = ttk.Style()
        btn_style.configure('ttk.TButton', font=('Segoe UI', 12))

        # - Create categorize button
        categorize_btn = ttk.Button(
            left_frame,
            text='Categorize Target',
            width=15,
            style='ttk.TButton',
            command=lambda: self.categorize_target(
                self.col_listbox.get(self.col_listbox.curselection()),
                self.col_val_1.get(), 
                self.selected_category_0.get(), 
                self.col_val_2.get(),
                self.selected_category_1.get())
                )
        # - Display categorize button in frame
        categorize_btn.grid(row=2, column=0, padx=5, pady=5, sticky='W')

        # - Create close button
        close_btn = ttk.Button(
            left_frame,
            text='Close',
            width=15,
            style='ttk.TButton',
            command=self.destroy
            )
        # - Display categorize button in frame
        close_btn.grid(row=3, column=0, padx=5, pady=5, sticky='W')        

    def populate_dict(self):
        self.a_dict = {}
        for col in self.bin_cols:
            self.a_dict[col] = df[col].unique().tolist()

    def column_selection(self, event):
        # Get the index of the listbox item (i.e. column name)
        selected_index = self.col_listbox.curselection()
        # Use index to get listbox item (i.e., column name)
        column_name = (self.col_listbox.get(selected_index))
        # Update the labels with the column values
        self.col_val_1.set(self.a_dict[column_name][0])
        self.col_val_2.set(self.a_dict[column_name][1])
                
    def category_selection_0(self, event):
        if self.selected_category_0.get() == 0:
            self.selected_category_1.set(1)
        elif self.selected_category_0.get() == 1:
            self.selected_category_1.set(0)

    def category_selection_1(self, event):
        if self.selected_category_1.get() == 0:
            self.selected_category_0.set(1)
        elif self.selected_category_1.get() == 1:
            self.selected_category_0.set(0)

    def categorize_target(self,target_col, value_1, category_1, value_2, category_2):
        global df
        df[target_col] = df[target_col].map({value_1: category_1, value_2: category_2})

        messagebox.showinfo(title="Categorize Target", 
        message=f'Target {target_col} categorized.')

class DropColumns(tk.Toplevel):
    global df

    def __init__(self, root):
        super().__init__(root)

        # Set window properties
        self.geometry('550x500')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Drop Columns')
        self.configure(bg='#1ac6ff')

        # Create left frame for label and listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=300, height=500)
        #left_frame.columnconfigure((0,1), weight=1)
        #left_frame.rowconfigure(0, weight=1)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=250, height=500)
        #right_frame.columnconfigure((0,1), weight=1)
        #right_frame.rowconfigure(0, weight=1)
        right_frame.grid(row=0, column=1, padx=5, pady=5)
        right_frame.grid_propagate(0)

        # Create list box to place at top of left frame
        # Get column indexes from the dataframe
        col_idxs = df.columns
        # convert the index to a tuple
        cols = tuple(col_idxs)
        # listbox String Variable
        col_list_var = tk.StringVar(value=cols)
        # listbox
        self.col_listbox = tk.Listbox(left_frame, listvariable=col_list_var, selectmode='extended')
        # Display listbox in frame
        self.col_listbox.grid(row=0, column=0, padx=0, pady=5, sticky='NS')

        # Create scrollbar for listbox
        lb_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.col_listbox.yview)
        lb_scroll.grid(row=0, column=1, pady=5, sticky='NSEW')
        self.col_listbox['yscrollcommand'] = lb_scroll.set
        
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
        dc_dropcols_btn = ttk.Button(right_frame, text='Drop Columns', width=15, command=lambda: drop_columns(self))
        dc_dropcols_btn.grid(row=0, column=0, padx=5, pady=5, sticky='E')

        dc_close_btn = ttk.Button(right_frame, text='Close', width=15, command=self.destroy)
        dc_close_btn.grid(row=1, column=0, padx=5, pady=5, sticky='E')

        def drop_columns(self):
            # Get the selected listbox items and put in a list
            col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
            # Drop selected column(s)
            df.drop(columns=col_list, inplace=True)
            # Send confirmation to user that column(s) was/were dropped
            messagebox.showinfo(title="Drop Columns", message=f'Column(s) {col_list} dropped.')

class ImputeNullsWithMean(tk.Toplevel):
    global df

    def __init__(self, root):
        super().__init__(root)

        # Set window properties
        self.geometry('550x650')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Impute Nulls with Mean')
        self.configure(bg='#1ac6ff')

        # Create left frame for listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=300, height=650)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)
        left_frame.grid_columnconfigure(0, weight=1)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=250, height=650)
        right_frame.grid(row=0, column=1, padx=5, pady=5)
        right_frame.grid_propagate(0)

        # The following creates a listbox and puts it in left frame
        # 1. Create series to find numeric columns with nulls: https://stackoverflow.com/a/36226137
        s = df.select_dtypes(include=['float64', 'int64']).isnull().any()

        # The above series (s) comprises of True and False values.  
        
        # 2. Use boolean indexing to get the indexes (i.e., the column names) and convert the index 
        # to a list. https://stackoverflow.com/a/52173171
        self.cols_list = s[s].index.to_list()

        # 3. Convert list to tuple, because tk.StringVar takes a tuple argument.
        cols_tuple = tuple(self.cols_list)
        
        # 4. Create tk.StringVar object for listbox and assign it to the col_list_var variable
        col_list_var = tk.StringVar(value=cols_tuple)
        
        # 5. Create listbox
        self.col_listbox = tk.Listbox(
            left_frame, 
            listvariable=col_list_var, 
            selectmode='browse',
            exportselection=False)
        
        # 6. Display listbox in frame
        self.col_listbox.grid(row=1, column=0, padx=0, pady=5, sticky='NSEW')

        # 7. Bind listbox to column_selection function.  When a column is selected, in the listbox,
        #    it's unique values are displayed in the text widget.
        self.col_listbox.bind('<<ListboxSelect>>', self.column_selection)

        # Create scrollbar for listbox
        lb_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.col_listbox.yview)
        lb_scroll.grid(row=1, column=1, pady=5, sticky='NSEW')
        self.col_listbox['yscrollcommand'] = lb_scroll.set

        # Create a label to place above the listbox 
        listbox_label = ttk.Label(
            left_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Numeric Columns w/Nulls'
            )
        listbox_label.grid(row=0, column=0, padx=0, pady=5, sticky='W')

        # Create dictionary for columns and their unique values (e.g., 'yes' and 'no')
        # This dictionary is needed to dynamically populate the labels as 
        # the user selects a column from the listbox
        self.a_dict = {}

        # Populate the dictionary with columns and values
        self.populate_dict()

        # Create a label to place above the text widget 
        # that indicates that the widget displays values of the selected column
        column_values_label = ttk.Label(
            left_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Column Values'
            )
        column_values_label.grid(row=2, column=0, padx=0, pady=5, sticky='W')

        # Create a text widget to present the values when a column is selected.
        # Displaying values gives the user more insight into which impute method to use.
        self.column_values_text = tk.Text(
            left_frame, 
            font=("Segoe UI", 14), 
            height=4,
            wrap=WORD)
        self.column_values_text.grid(row=3, column=0, padx=0, pady=5, sticky='NSEW')
        
        # Create scrollbar for text widget
        text_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.column_values_text.yview)
        text_scroll.grid(row=3, column=1, pady=5, sticky='NSEW')
        self.column_values_text['yscrollcommand'] = text_scroll.set

        # Create a label to place above the action buttons 
        action_label = ttk.Label(
            right_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Action'
            )
        action_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create buttons and put in right frame
        impute_with_mean_btn = ttk.Button(
            right_frame,
            text='Impute w/Mean',
            width=16, command=lambda: self.impute_with_mmm('mean')
            )
        impute_with_mean_btn.grid(row=1, column=0, padx=5, pady=5, sticky='E')

        impute_with_mode_btn = ttk.Button(
            right_frame,
            text='Impute w/Mode',
            width=16, 
            command=lambda: self.impute_with_mmm('mode')
            )
        impute_with_mode_btn.grid(row=2, column=0, padx=5, pady=5, sticky='E')

        impute_with_median_btn = ttk.Button(
            right_frame, 
            text='Impute w/Median', 
            width=16, command=lambda: self.impute_with_mmm('median')
            )
        impute_with_median_btn.grid(row=3, column=0, padx=5, pady=5, sticky='E')

        close_btn = ttk.Button(
            right_frame, 
            text='Close', 
            width=16, 
            command=self.destroy
            )
        close_btn.grid(row=4, column=0, padx=5, pady=5, sticky='E')

    def populate_dict(self):
        # clear dictionary
        self.a_dict = {}
        # populate dictionary with initial or updated keys (i.e., column names) and 
        # values (i.e., list of unique column values)
        for col in self.cols_list:
            self.a_dict[col] = df[col].sort_values(na_position='first').unique().tolist()

    def column_selection(self, event):
        # Get the index of the listbox item
        selected_index = self.col_listbox.curselection()
        # Use index to get listbox item (i.e., column name)
        column_name = (self.col_listbox.get(selected_index))
        # Get columns' values
        list_of_values = self.a_dict[column_name]
        # Enable text widget
        self.column_values_text.config(state="normal")
        # Delete any text that may be in text widget
        self.column_values_text.delete("1.0","end")
        # Enter column name into to text widget
        self.column_values_text.insert(END, column_name + ' Values:  ')
        # Enter column's values into text widget
        for value in list_of_values:
            self.column_values_text.insert(END, str(value) + ', ')
        # Delete ending space from text widget
        self.column_values_text.delete("end-2c")
        # Delete ending comma from text widget
        self.column_values_text.delete("end-2c")
        # Disable text widget
        self.column_values_text.config(state="disabled")

    def impute_with_mmm(self, impute_method):
        # Get the selected listbox items and put in a list
        impute_value = None
        col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
        col_str = ', '.join(col_list)
        # Loop through col_list to impute each column with selected value (i.e., mean, mode, median)
        for col in col_list:
            if impute_method == 'mean':
                impute_value = round(df[col].mean(), 1)
                df[col].fillna(impute_value, inplace=True)
                self.populate_dict()
                self.column_selection(None)
            elif impute_method == 'mode':
                impute_value = round(df[col].mode().tail(1).item(), 1)
                df[col].fillna(impute_value, inplace=True)
                self.populate_dict()
                self.column_selection(None)
            else:
                impute_value = round(df[col].median(), 1)
                df[col].fillna(impute_value, inplace=True)
                self.populate_dict()
                self.column_selection(None)
        # Send confirmation
        messagebox.showinfo(title="Impute with MMM", 
        message=f'Column(s) {col_str} imputed with a {impute_method} of {impute_value}.')


class FillAllNullsWindow(tk.Toplevel):
    global df

    def __init__(self, root):
        super().__init__(root)

        # Set window properties
        self.geometry('600x120')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Fill All Nulls in DataFrame')
        self.configure(bg='#1ac6ff')

        # Create frame for window
        fillna_all_frame = tk.Frame(self, bg='#1ac6ff', width=600, height=120)
        fillna_all_frame.columnconfigure((0,1), weight=1)
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

        # Create variable to hold fillna value
        self.fillna_all_value = tk.StringVar()

        # Create entry widget (to enter fillna_all_value) and display in frame
        fillna_all_input = ttk.Entry(
            fillna_all_frame, 
            textvariable=self.fillna_all_value,
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
            command=lambda: fill_all_nulls(self.fillna_all_value.get())
            )
        fillna_all_btn.grid(row=1, column=0, padx=5, pady=5)

        # Create button widget to fill nulls
        fillna_all_close_btn = ttk.Button(
            fillna_all_frame,
            text='Close',
            command=self.destroy
            )
        fillna_all_close_btn.grid(row=1, column=1, padx=5, pady=5)

        def fill_all_nulls(impute_value):
            
            num_of_nulls = int(df.isnull().sum().sum())
            question = messagebox.askyesno(
                "Impute Nulls", 
                f"Impute {num_of_nulls} nulls with {impute_value}?")
            if question == 1:
                df.fillna(impute_value, inplace=True)
                messagebox.showinfo(title="Impute Nulls", message=f'{num_of_nulls} nulls imputed.')

root = PandaDataCleaner()
# Set global font.  Doesn't apply to fields.  
font.nametofont('TkDefaultFont').configure(size=15)
root.mainloop()