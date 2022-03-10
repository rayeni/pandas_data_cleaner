# Import libaries
import pandas as pd
import sklearn.impute

from datetime import datetime
import io

import csv

import re

import tkinter as tk
import tkinter.font as font
from tkinter.constants import WORD
from tkinter import ttk, END, StringVar, IntVar, messagebox, filedialog

from PIL import ImageTk, Image

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

# Main application window
class PandasDataCleaner(tk.Tk):
    '''
    This class is for the root window of the TKinter application.
    It inherits from Tkinter's tk.Tk class.
    '''
    def __init__(self):
        '''The constuctor for the PandasDataCleaner class.'''
        super().__init__()

        # Change window title
        self.title('Pandas Data Cleaner')
        try:
            # Set window icon
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        # Set window dimensions
        self.geometry("800x350")
        # Disable resizing window
        self.resizable(False, False)
        self.configure(bg='#1ac6ff')

        # Create variable to hold file path, to be accessed later by other functions
        self.csv_file = ''

        # Create frame for logo
        logo_frame = tk.Frame(self, bg='#1ac6ff', width=800, height=70)
        logo_frame.columnconfigure(0, weight=1)
        logo_frame.pack(padx=5, pady=0)
        logo_frame.pack_propagate(0)

        # Create top level frame to hold buttons for import, export and close tasks
        top_frame = tk.Frame(self, bg='#1ac6ff', width=800, height=70)
        top_frame.columnconfigure((0,1,2), weight=1)
        top_frame.pack(padx=5, pady=0)
        top_frame.grid_propagate(0)

        # Create functionality frame to hold buttons for different tasks
        func_frame_1 = tk.Frame(self, bg='#1ac6ff', width=800, height=150)
        func_frame_1.columnconfigure((0,1,2), weight=1)
        func_frame_1.pack(padx=5, pady=0)
        func_frame_1.grid_propagate(0)

        # Menu button font
        menu_option_font = 14

        #--- Add widgets ---#

        # Create logo
        try:
            self.logo = ImageTk.PhotoImage(Image.open('./images/logo.png'))
        except:
            self.logo = ImageTk.PhotoImage(Image.open(my_dir / './images/logo.png'))
        # Create label for logo
        logo_label = tk.Label(logo_frame, bg='#1ac6ff', image=self.logo)
        # Place logo in logo_frame
        logo_label.pack()

        '''
        The buttons to import csv, export dataframe, 
        and to close the app are created here and added
        to the frame, top_frame.
        '''
        # ---FIRST MENU BUTTON (Import from CSV), Top Frame, First Row, First Column--- #

        # Create import button to import CSV file
        #import_data = ttk.Button(
        #    top_frame, 
        #    text='Import from CSV', 
        #    width=17, 
        #    command=self.import_from_csv)

        # Create "Import Data" menu button
        mb_import_data = ttk.Menubutton(top_frame, text='Import Data', width=15)

        # Create "Import Data" menu
        menu_import_data = tk.Menu(mb_import_data, tearoff=False)

        # Create "Import CSV" menu option
        menu_import_data.add_command(
            label='Import CSV', 
            font=("Segoe UI", menu_option_font), 
            command=self.import_csv)

        # Create "Import TSV" menu option
        menu_import_data.add_command(
            label='Import TSV', 
            font=("Segoe UI", menu_option_font), 
            command=self.import_tsv)

        # Create "Import Excel" menu option
        menu_import_data.add_command(
            label='Import Excel', 
            font=("Segoe UI", menu_option_font), 
            command=self.import_excel)

        # Associate menu with menu button
        mb_import_data["menu"] = menu_import_data

        # Display menu button in frame
        mb_import_data.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # ---SECOND MENU BUTTON (Export to CSV), Top Frame, First Row, Second Column--- #

        # Create export button to export Dataframe to CSV file
        export_data = ttk.Button(top_frame, text='Export to CSV', width=17, command=self.export_to_csv)
        # Add export button to frame
        export_data.grid(row=0, column=1, padx=5, pady=5)

        # ---THIRD MENU BUTTON (Export to CSV), Top Frame, First Row, Third Column--- #

        # Create close button to close application
        close_root = ttk.Button(top_frame, text='Close App', width=17, command=self.close_app)
        # Add close button to frame
        close_root.grid(row=0, column=2, padx=5, pady=5, sticky='E')

        '''
        The remaining widgets are menu buttons that present the user with
        data cleaning options.  The menu buttons are added to the frame,
        func_frame_1.
        '''
        # ---FIRST MENU BUTTON (MISSING DATA), First Row, First Column--- #

        # Create "Missing Data" menu button
        mb_missing_data = ttk.Menubutton(func_frame_1, text='Fix Missing Data', width=15)

        # Create "Missing Data" menu
        menu_missing_data = tk.Menu(mb_missing_data, tearoff=False)

        # Create "Drop nulls" menu option
        menu_missing_data.add_command(
            label='Drop All Nulls', 
            font=("Segoe UI", menu_option_font), 
            command=self.drop_all_nulls)

        # Create "Fill NA" menu option
        menu_missing_data.add_command(
            label='Fill All Nulls w/Specific Value', 
            font=("Segoe UI", menu_option_font), 
            command=self.open_fill_all_nulls_window)

        # Create "Remove Rows with High% of Missing Data" menu option
        menu_missing_data.add_command(
            label='Remove Rows with X Pct of Nulls', 
            font=("Segoe UI", menu_option_font), 
            command=self.open_remove_rows_with_x_nulls_window)

    # Create "Fill-Forward" menu option
        menu_missing_data.add_command(
            label='Fill Forward/Backward', 
            font=("Segoe UI", menu_option_font), 
            command=self.open_fill_forward_window)

        # Create "Impute Nulls with Mean" menu option
        menu_missing_data.add_command(
            label='Impute w/Mean, Mode, Median', 
            font=("Segoe UI", menu_option_font), 
            command=self.open_impute_nulls_with_mean_window)

        # Create "Impute with KNN" menu option
        menu_missing_data.add_command(
            label='Impute with KNN', 
            font=("Segoe UI", menu_option_font), 
            command=self.impute_with_knn)

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
        
        # Create Convert Column Headers to Lowercase menu option
        menu_df_tasks.add_command(
            label='Change Column Names to Lowercase', 
            font=("Segoe UI", menu_option_font), 
            command=self.change_col_names_to_lowercase)        

        # Associate menu with menu button
        mb_df_tasks["menu"] = menu_df_tasks

        # Display menu button in frame
        mb_df_tasks.grid(row=0, column=1, padx=5, pady=5) 

        # ---THIRD MENU BUTTON (CLEAN NUMERICS) First Row, Third Column--- #

        # Create Clean Numerics menu button
        mb_clean_numeric = ttk.Menubutton(func_frame_1, text='Clean Numerics', width=15)

        # Create Clean Numerics menu
        menu_clean_numeric = tk.Menu(mb_clean_numeric, tearoff=False)

        # Create Numeric Text -> Int menu option
        #menu_clean_numeric.add_command(
        #    label='Numeric Text -> Int',
        #    font=('Segoe UI', menu_option_font),
        #    command='')

        # Create Remove % Signs menu option
        menu_clean_numeric.add_command(
            label='Remove Percent Signs',
            font=('Segoe UI', menu_option_font),
            command=self.open_remove_pcts_window)

        # Create Remove Units Measurement menu option
        menu_clean_numeric.add_command(
            label='Remove Units Measurement',
            font=('Segoe UI', menu_option_font),
            command=self.open_remove_units_of_measure_window)

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

        # Create Dummify Columns menu option
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

        # Create Remove Special Characters menu option
        menu_clean_string.add_command(
            label='Remove Special Characters', 
            font=("Segoe UI", menu_option_font), 
            command=self.remove_special_characters)

        # Create Change Chars to Lowercase menu option
        menu_clean_string.add_command(
            label='Change Column Values to Lowercase', 
            font=("Segoe UI", menu_option_font), 
            command=self.convert_to_lowercase)

        # Create Change Chars to Lowercase menu option
        menu_clean_string.add_command(
            label='Replace Synonyms with Single Word', 
            font=("Segoe UI", menu_option_font), 
            command=self.open_replace_synonyms_window)

        # Create Replace NA with N.A. menu option
        menu_clean_string.add_command(
            label='Replace NA (False NaN) with N.A.', 
            font=("Segoe UI", menu_option_font), 
            command=self.replace_na_with_ndotadot)

        # Associate menu with menu button
        mb_clean_string["menu"] = menu_clean_string

        # Display menu button in frame
        mb_clean_string.grid(row=1, column=1, padx=5, pady=5)

        # ---SIXTH MENU BUTTON (DateTime) Second Row, Third Column--- #

        # Create DateTime menu button
        mb_datetime = ttk.Menubutton(func_frame_1, text='DateTime', width=15)

        # Create DateTime menu
        menu_datetime = tk.Menu(mb_clean_numeric, tearoff=False)

        # Create Set Date to Index menu option
        menu_datetime.add_command(
            label='Set Date to Index',
            font=('Segoe UI', menu_option_font),
            command=self.date_to_index)

        # Create Index -> DatetimeIndex menu option
        menu_datetime.add_command(
            label='Index -> DatetimeIndex',
            font=('Segoe UI', menu_option_font),
            command=self.index_to_datetimeindex)

        # Associate menu with menu button
        mb_datetime["menu"] = menu_datetime

        # Display menu button in frame
        mb_datetime.grid(row=1, column=2, padx=5, pady=5, sticky='E')

    def import_csv(self):
        '''Import csv file into dataframe.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Get path/location of csv file to import
        self.csv_file = filedialog.askopenfilename(
            initialdir="./", 
            title="Open CSV File", 
            filetypes=(("CSV Files", "*.csv"),("All Files","*.*")))
        
        # Read csv into global df variable
        df = pd.read_csv(self.csv_file)

        # Give user confirmation that csv file was imported.
        if len(df) > 0:
            messagebox.showinfo(
                title="Load CSV", 
                message='CSV file loaded successfully.'
                )
        else:
            messagebox.showerror(
                title='Error', 
                message='Error loading CSV file.'
                )
        
    def import_tsv(self):
        '''Import tsv file into dataframe.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Get path/location of tsv file to import
        tsv_file = filedialog.askopenfilename(
            initialdir="./", 
            title="Open TSV File", 
            filetypes=(("TSV Files", "*.tsv"),("All Files","*.*")))
        
        # Read tsv into global df variable
        df = pd.read_csv(tsv_file, sep='\t')

        # Give user confirmation that tsv file was imported.
        if len(df) > 0:
            messagebox.showinfo(
                title="Load TSV", 
                message='TSV file loaded successfully.'
                )
        else:
            messagebox.showerror(
                title='Error', 
                message='Error loading TSV file.'
                )
    
    def import_excel(self):
        '''Import Excel file into dataframe.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Get path/location of Excel file to import
        excel_file = filedialog.askopenfilename(
            initialdir="./", 
            title="Open Excel File", 
            filetypes=(("Excel Files", "*.xlsx"),("All Files","*.*")))
        
        # Read Excel file into global df variable
        df = pd.read_excel(excel_file)

        # Give user confirmation that Excel file was imported.
        if len(df) > 0:
            messagebox.showinfo(
                title="Load Excel File", 
                message='Excel file loaded successfully.'
                )
        else:
            messagebox.showerror(
                title='Error', 
                message='Error loading Exce; file.'
                )    

    def export_to_csv(self):
        '''Export dataframe to csv file.'''

        # Set df variable as global variable to enable all functions to modify it
        global df
        
        # Check if dataframe is loaded.  If not, notify user of error.
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present", 
                message='A dataframe was not created. Please load a CSV file.'
                ) 
        else:
            # Get name of csv file and where it should be exported from user
            csv_name = filedialog.asksaveasfilename(
                initialdir="./", 
                title="Export to CSV", 
                filetypes=(("CSV Files","*.csv"),("All Files","*.*")))

            # Export dataframe to csv file
            df.to_csv(csv_name, index=False)

            # Confirmation of export to csv file
            messagebox.showinfo(
                title="CSV Export", 
                message='DataFrame exported to CSV.'
                )

    def close_app(self):
        '''Close application.'''

        # Ask user if they are sure about closing application
        question = messagebox.askyesno(
            title="Close Pandas Data Cleaner", 
            message="Are you sure you want to exit?")

        # If user answers Yes, the close application
        if question == 1:
            self.destroy()

    def change_col_names_to_lowercase(self):
        '''Change column names to lowercase.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present",
                message='Please load CSV file.'
                )
        else:
            # Rename column names
            df.columns = df.columns.str.lower().str.replace(' ','_')
            df.columns = df.columns.str.lower().str.replace('/','_')
            # Notify user
            messagebox.showinfo(
                title="Change Column Names", 
                message='Column names were changed to lowercase successfully.'
                )

    def drop_all_nulls(self):
        '''Drop all nulls unconditionally'''

        # Set df variable as global variable to enable all functions to modify it
        global df
        
        # Check if dataframe is loaded. If it's not loaded (len(df) == 0) exit drop operation
        if len(df) == 0: 
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        else:
            # Get number of nulls:
            num_of_nulls = int(df.isnull().sum().sum())
            # If there are no nulls, notify that there are no nulls.
            if num_of_nulls == 0:
                messagebox.showinfo(
                    title='No Nulls to Drop', 
                    message=f'There are no nulls to drop.'
                    )
            else:
                # Confirm with user to drop nulls
                question = messagebox.askyesno(
                    title="Drop Nulls", 
                    message=f"Drop {num_of_nulls} nulls?"
                    )
                # If user answers Yes, then drop nulls
                if question == 1:
                    # Drop nulls
                    df.dropna(inplace = True)
                    # Send confirmation of drop.
                    messagebox.showinfo(
                        title="Drop Nulls", 
                        message=f'{num_of_nulls} nulls dropped.'
                        )

    def impute_with_knn(self):
        '''Use KNN Imputer to fill missing values'''

        # Set df variable as global variable to enable all functions to modify it
        global df
        
        # Check if dataframe is loaded. If it's not loaded (len(df) == 0) exit drop operation
        if len(df) == 0: 
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        # Check if there are any columns of type object
        elif df.select_dtypes(include=['object']).shape[1] > 0:
            messagebox.showerror(
                title="Non-Numeric Column Exists", 
                message='There are one or more non-numeric columns.  KNN requires numeric columns.'
                )
        else:
            # Get number of nulls:
            num_of_nulls = int(df.isnull().sum().sum())
            # If there are no nulls, notify that there are no nulls.
            if num_of_nulls == 0:
                messagebox.showinfo(
                    title='No Nulls to Impute', 
                    message=f'There are no nulls to impute.'
                    )
            else:
                # Confirm with user to impute nulls
                question = messagebox.askyesno(
                    title="Impute Nulls",
                    message=f"Impute {num_of_nulls} nulls? The process may take a few moments."
                    )
                # If user answers Yes, then impute nulls
                if question == 1:
                    # Create and initialize KNN imputation model
                    impKNN = sklearn.impute.KNNImputer(n_neighbors=5)
                    # Impute Nulls
                    df = pd.DataFrame(impKNN.fit_transform(df),columns=df.columns)
                    # Send confirmation.
                    messagebox.showinfo(
                        title="Impute Nulls", 
                        message=f'{num_of_nulls} nulls imputed.'
                        )

    def check_for_date_string(self, date_text):
        '''
        Check if text value is of format YYYY-MM-DD
        https://stackoverflow.com/a/37045601

        :param date_text: text data from df.info() function
        :type date_text: string

        :raises ValueError: if date_text is not in correct date format
        :return True/False: True, if text is in date format, otherwise False
        '''

        try:
            if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            return True
        except ValueError:
            return False

    def get_dataframe_info(self):
        '''
        Get dataframe information.
        Store information in buffer.
        Return contents of buffer.

        :return buffer.getvalue(): Contents in buffer
        '''
        # Create StringIO object
        buffer = io.StringIO()

        # Get Dataframe information and place in buffer
        df.info(buf=buffer)

        # Get and return string from buffer
        return buffer.getvalue()

    def get_index_info(self, df_inf, start_marker, end_marker):
        '''
        Get current index information from dataframe info.
        https://www.kite.com/python/answers/how-to-get-the-substring-between-two-markers-in-python

        :param df_inf: Text output from the DataFrame.info() function
        :type df_inf: string

        :param start_marker: The beginning point of the df_inf to start grabbing data
        type start_marker: string

        :param end_marker: The ending point of the df_inf to stop grabbing data
        type end_marker: string

        :return index_substring.split(): A list of words from a substring of df_inf          
        '''

        # Get the starting point for substring (The line that starts with Index info)
        start = df_inf.find(start_marker) + len(start_marker)

        # Get the ending point for substring
        end = df_inf.find(end_marker)

        # Get the substring
        index_substring = df_inf[start:end]

        # Return the substring in the form of a list
        return index_substring.split()

    def date_to_index(self):
        '''Convert date column to index'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0: 
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        else:
            # Get columns.  
            columns = df.columns.to_list()

            # Search for a date column in the list of columns
            if 'date' in columns:
                df.set_index('date', inplace=True)
                messagebox.showinfo(
                    title="Set Date to Index",
                    message=f'The "date" column was set to index successfully.'
                    )
            elif 'DATE' in columns:
                df.set_index('DATE', inplace=True)
                messagebox.showinfo(
                    title="Set Date to Index",
                    message=f'The "DATE" column was set to index successfully.'
                    )
            elif 'Date' in columns:
                df.set_index('Date', inplace=True)
                messagebox.showinfo(
                    title="Set Date to Index",
                    message=f'The "Date" column was set to index successfully.'
                    )
            else:
                messagebox.showwarning(
                    title="Set Date to Index",
                    message=f'Either a date column was set previously, or a "date" column was NOT found.'
                    )

    def index_to_datetimeindex(self):
        '''Check Index for datatime data. Convert Index to DatetimeIndex'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0: 
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        else:
            # Get dataframe info
            df_info = self.get_dataframe_info()

            # Get Index information BEFORE changing index.
            index_info = self.get_index_info(df_info, "<class 'pandas.core.frame.DataFrame'>\n", "\nData")         
            
            # Get information about list indices 0,3 and 5
            index_type = index_info[0]
            str_3_is_date = self.check_for_date_string(index_info[3])
            str_5_is_date = self.check_for_date_string(index_info[5])

            # Convert Index to DatetimeIndex
            if str_3_is_date is True & str_5_is_date is True:
                if index_type == 'Index:':
                    df.index = pd.to_datetime(df.index)

            # Get dataframe info
            df_info = self.get_dataframe_info()

            # Get Index information AFTER changing index.
            index_info = self.get_index_info(df_info, "<class 'pandas.core.frame.DataFrame'>\n", "\nData")

            # Get information about list index 0
            index_type = index_info[0]
            
            # Notify user of result
            if index_type == "DatetimeIndex:":
                messagebox.showinfo(
                    title="Index to DatetimeIndex",
                    message=f'Index was converted DatetimeIndex successfully'
                    )
            else:
                messagebox.showwarning(
                    title="Index to DatetimeIndex",
                    message=f'Index was NOT converted DatetimeIndex. Check index values.'
                    )

    def remove_trailing_leading_spaces(self):
        '''Find and remove all trailing and leading spaces from strings.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0: 
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
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
                messagebox.showinfo(
                    title="Remove Trailing/Leading Spaces", 
                    message=f'NO trailing/leading spaces were found.'
                    )
            elif total_diff == 1:
                messagebox.showinfo(
                    title="Remove Trailing/Leading Spaces", 
                    message=f'{total_diff} trailing/leading space has been removed.'
                    )
            else:
                messagebox.showinfo(
                    title="Remove Trailing/Leading Spaces", 
                    message=f'{total_diff} trailing/leading spaces have been removed.'
                    )

    def rm_spec_chars_from_cols(self, x):
        '''
        Receive call from .apply() to 
        remove special characters from 
        DataFrame column values.
        
        :param x: Column value to be modified
        :type x: string

        :return x: Modified column value
        '''

        # try except is use here to handle any 
        # NaNs that may exist and break application
        try:
            x = re.sub(r'[^a-zA-Z0-9\s]','',x)
        except TypeError:
            pass
        
        return x

    def remove_special_characters(self):
        '''Find and remove all special characters from strings'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Get all columns of type string/object and place in list
        obj_cols_list = df.select_dtypes(include='object').columns.to_list()

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0: 
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        elif len(obj_cols_list) == 0:
            messagebox.showinfo(
                title="Remove Special Characters", 
                message='No string data is present.'
                )
        else:
            # iterate over columns, and apply function to values
            for col in obj_cols_list:
                df[col] = df[col].apply(self.rm_spec_chars_from_cols)
            
            # Notify user of result
            messagebox.showinfo(
                title="Remove Special Characters", 
                message=f'Special characters removed.'
                )

    def convert_cols_to_lowercase(self, x):
        '''
        Receive call from .apply() to 
        convert DataFrame columns values
        to lowercase.
        
        :param x: Column value to be modified
        :type x: string

        :return x: Modified column value
        '''

        # try except is use here to handle any 
        # NaNs that may exist and break application
        try:
            x = x.lower()
        except AttributeError:
            pass
        
        return x

    def convert_to_lowercase(self):
        '''Find and remove all special characters from strings'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Get all columns of type string/object and place in list
        obj_cols_list = df.select_dtypes(include='object').columns.to_list()

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0: 
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        elif len(obj_cols_list) == 0:
            messagebox.showinfo(
                title="Convert to Lowercase", 
                message='No string data is present.'
                )
        else:
            # iterate over columns, and apply function to values
            for col in obj_cols_list:
                df[col] = df[col].apply(self.convert_cols_to_lowercase)
            
            # Notify user of result
            messagebox.showinfo(
                title="Convert Strings to Lowercase", 
                message=f'Column values converted to lowercase.'
                )

    def replace_na_with_ndotadot(self):
        '''
        Find and replace NA NaN with N.A. 
        This eliminates false NaNs.
        '''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Set counter variable to count the number of replacements
        counter = 0

        # Create dictionary.  Dictionary will be used to recreate df to capture instances of NA
        a_dict = {}

        # Create variable to get number of rows in df. Used in range of for loop.
        rows = df.shape[0] + 1

        # Create variable to get number of columns in df. Used in range of for loop.
        columns = df.shape[1]

        # Read CSV using csv.reader, not pandas, to capture instances of NA
        with open(self.csv_file, "r") as file:
            csv_reader = csv.reader(file, delimiter=',')
            lists = [lines for lines in csv_reader]

        # Grab the first list from lists to get the column headers
        list_0 = lists[0]

        # Add keys and empty values/list to dictionary
        for i in range(0,len(list_0)):
            a_dict[list_0[i]] = []
        
        # Add values to dictionary:
        for c in range(0,columns):
            for r in range(1, rows):
                a_dict[list_0[c]].append(lists[r][c])

        # Replace NA NaN with N.A. to eliminate NaNs
        for key in a_dict:
            for i in range(0, rows-1):
                if a_dict[key][i] in ['N/A','NA','n/a']:
                    df[key][i] = 'N.A.'
                    counter = counter + 1

        # Notify user
        if counter == 0: 
            messagebox.showinfo(
                title="Replace NA (False NaN) with N.A.", 
                message='No NA NaNs found.'
                )
        else:
            messagebox.showinfo(
                title="Replace NA NaN with N.A.", 
                message=f'{counter} NAs were replaced with N.A.'
                )

    def open_remove_rows_with_x_nulls_window(self):
        '''Open Fill All Nulls window.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        # Open window
        else:
            window = RemoveRowsWithXNullsWindow(self)
            window.grab_set()

    def open_fill_all_nulls_window(self):
        '''Open Fill All Nulls window.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        # Open window
        else:
            window = FillAllNullsWindow(self)
            window.grab_set()

    def open_fill_forward_window(self):
        '''Open Fill Forward window.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        # Open window
        else:
            window = FillForward(self)
            window.grab_set()

    def open_impute_nulls_with_mean_window(self):
        '''Open Impute Nulls with Mean window.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        # Open window
        else:
            window = ImputeNullsWithMean(self)
            window.grab_set()

    def open_drop_cols_window(self):
        '''Open Drop Columns window.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        # Open DropColumns window
        else:
            window = DropColumns(self)
            window.grab_set()

    def open_binary_class_window(self):
        '''Open Binary Classification window.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        # Open window
        else:
            window = BinaryClassification(self)
            window.grab_set()

    def open_dummify_columns_window(self):
        '''Open Dummify Columns window.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        # Open window
        else:
            window = DummifyColumns(self)
            window.grab_set()

    def open_remove_pcts_window(self):
        '''Open Remove Percents window.'''

        # Set df variable as global variable to enable all functions to modify it
        global df
        
        # Check for any object columns:
        object_cols = df.select_dtypes(include='object')

        # Check for any percent signs
        percent_signs = object_cols.apply(lambda col: col.str.contains('%').any(), axis=0)

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        # If there are no object columns, then exit
        elif object_cols.shape[1] == 0:
            messagebox.showinfo(
                title="No Object Columns", 
                message='No object columns exist.'
                )
        # If there are no percent signs, then exit
        elif percent_signs.any() == False:
            messagebox.showinfo(
                title="No % Signs", 
                message='No Percent Signs(%) exist.'
                )
        # Open window
        else:
            window = RemovePercents(self)
            window.grab_set()

    def open_remove_units_of_measure_window(self):
        '''Open Remove Measurement window.'''

        # Set df variable as global variable to enable all functions to modify it
        global df
        
        # Check for any object columns:
        object_cols = df.select_dtypes(include='object')

        # Check if columns have values with leading numbers or currency symbols
        leads_with_num = object_cols.apply(lambda col: col.str.startswith(
            ('$', '€', '£', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')), axis=0)

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        # If there are no object columns, then exit
        elif object_cols.shape[1] == 0:
            messagebox.showinfo(
                title="No Object Columns", 
                message='No object columns exist.'
                )
        # If there are no column values leading with numbers or currency symbols, then exit
        elif any(leads_with_num) == False:
            messagebox.showinfo(
                title="No Data Found", 
                message='No data found that meets criteria.'
                )
        # Open window
        else:
            window = RemoveUnitsOfMeasurment(self)
            window.grab_set()

    def open_replace_synonyms_window(self):
        '''Open Replace Synonyms Window.'''

        # Set df variable as global variable to enable all functions to modify it
        global df

        # Check for any object columns:
        object_cols = df.select_dtypes(include='object')

        # Check if dataframe is loaded. If it's not loaded (len(df) == 0 ), then showerror
        if len(df) == 0:
            messagebox.showerror(
                title="No Data Present", 
                message='Please load CSV file.'
                )
        # If there are no object columns, then exit
        elif object_cols.shape[1] == 0:
            messagebox.showinfo(
                title="No Object Columns", 
                message='No object columns exist.'
                )
        # Open window
        else:
            window = ReplaceSynonyms(self)
            window.grab_set()

class ReplaceSynonyms(tk.Toplevel):
    '''
    This class is for the secondary window,
    FillF, of the TKinter application.
    It inherits from Tkinter's tk.Toplevel class.
    '''

    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        '''The constuctor for the ReplaceSynonyms class.'''
        super().__init__(root)

        # Set window properties
        self.geometry('770x650')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Replace Synonyms...')
        self.configure(bg='#1ac6ff')

        # Create top left frame for listbox displaying column names
        left_frame = tk.Frame(self, bg='#1ac6ff', width=250, height=370)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)
        #left_frame.grid_columnconfigure(0, weight=1) # disabled to remove gap between scroll and lb

        # Create top center frame for listbox displaying column values
        center_frame = tk.Frame(self, bg='#1ac6ff', width=250, height=370)
        center_frame.grid(row=0, column=1, padx=5, pady=5)
        center_frame.grid_propagate(0)
        #center_frame.grid_columnconfigure(0, weight=1)

        # Create top right frame for listbox displaying column values
        right_frame = tk.Frame(self, bg='#1ac6ff', width=240, height=370)
        right_frame.grid(row=0, column=2, padx=5, pady=5)
        right_frame.grid_propagate(0)
        #right_frame.grid_columnconfigure(0, weight=1)

        # Create middle frame for text widget presenting column values
        middle_frame = tk.Frame(self, bg='#1ac6ff', width=750, height=200)
        middle_frame.grid(row=1, column=0, columnspan=3, padx=0, pady=5)
        middle_frame.grid_propagate(0)
        middle_frame.grid_columnconfigure(0, weight=1) #Needed for scrollbar to appear

        # Create frame for buttons
        bottom_frame = tk.Frame(self, bg='#1ac6ff', width=750, height=50)
        bottom_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        bottom_frame.grid_propagate(0)
        #bottom_frame.grid_columnconfigure(0, weight=1)

        # Create a label to place above the column names listbox 
        col_names_listbox_label = ttk.Label(
            left_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='In Column...'
            )
        col_names_listbox_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # The following creates a listbox and puts it in left frame
        # 1. Get a list of columns that are objects.
        self.cols_list = df.select_dtypes(include='object').columns.tolist()

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
        self.col_listbox.grid(row=1, column=0, padx=0, pady=0, sticky='NESW')

        # 7. Bind listbox to column_selection function.  When a column is selected, in the listbox,
        #    it's unique values are displayed in the text widget.
        self.col_listbox.bind('<<ListboxSelect>>', self.column_selection)

        # Create scrollbar for listbox
        col_lb_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.col_listbox.yview)
        col_lb_scroll.grid(row=1, column=1, padx=0, pady=0, sticky='NSEW')
        self.col_listbox['yscrollcommand'] = col_lb_scroll.set

        # Create dictionary for columns and their unique values (e.g., 'yes' and 'no')
        # This dictionary is needed to dynamically populate the labels as 
        # the user selects a column from the listbox
        self.a_dict = {}

        # Populate the dictionary with columns and values
        self.populate_dict()

        # Create a label to place above the first column values listbox 
        col_values_listbox_1_label = ttk.Label(
            center_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Replace...'
            )
        col_values_listbox_1_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create first listbox to contain column values.  When an item (column name) is selected in the 
        # col_listbox, the values_listbox_1 is populated with the column's values.
        # 1. Create empty tuple.  
        col_values_1_tpl = ()

        # 2. Create listvariable for listbox. 
        col_values_1_var = tk.StringVar(value=col_values_1_tpl)

        # 3. Create listbox
        self.col_values_listbox_1 = tk.Listbox(
            center_frame, 
            listvariable=col_values_1_var, 
            selectmode='extended',
            exportselection=False)        

        # Display listbox in center_frame
        self.col_values_listbox_1.grid(row=1, column=0, padx=0, pady=0)

        # Bind listbox to column_selection function.  When a column is selected, in the listbox,
        # it's unique values are displayed in the text widget.
        #self.values_listbox_1.bind('<<ListboxSelect>>', self.column_selection)    

        # Create scrollbars for listbox containing column values
        col_values_lb_scroll_1 = ttk.Scrollbar(
            center_frame, 
            orient='vertical', 
            command=self.col_values_listbox_1.yview)
        col_values_lb_scroll_1.grid(row=1, column=1, pady=0, sticky='NSEW')
        self.col_values_listbox_1['yscrollcommand'] = col_values_lb_scroll_1.set

        col_values_lb_scroll_1_h = ttk.Scrollbar(
            center_frame, 
            orient='horizontal', 
            command=self.col_values_listbox_1.xview)
        col_values_lb_scroll_1_h.grid(row=2, column=0, pady=0, sticky='NSEW')
        self.col_values_listbox_1['xscrollcommand'] = col_values_lb_scroll_1_h.set

        # Create a label to place above the second column values listbox 
        col_values_listbox_2_label = ttk.Label(
            right_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='With...'
            )
        col_values_listbox_2_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create second listbox containing column values.
        # 1. Create empty tuple.
        col_values_2_tpl = ()

        # 2. Create list variable for listbox.  This also populates listbox.
        col_values_2_var = tk.StringVar(value=col_values_2_tpl)

        # 3. Create listbox
        self.col_values_listbox_2 = tk.Listbox(
            right_frame, 
            listvariable=col_values_2_var, 
            selectmode='browse',
            exportselection=False)        

        # Display first listbox containing column values in frame
        self.col_values_listbox_2.grid(row=1, column=0, padx=0, pady=0)

        # Bind listbox to column_selection function.  When a column is selected, in the listbox,
        # it's unique values are displayed in the text widget.
        #self.values_listbox_2.bind('<<ListboxSelect>>', self.column_selection)    

        # Create scrollbars for second listbox containing column values
        col_values_lb_scroll_2 = ttk.Scrollbar(
            right_frame, 
            orient='vertical', 
            command=self.col_values_listbox_2.yview)
        col_values_lb_scroll_2.grid(row=1, column=1, pady=0, sticky='NSEW')
        self.col_values_listbox_2['yscrollcommand'] = col_values_lb_scroll_2.set

        col_values_lb_scroll_2_h = ttk.Scrollbar(
            right_frame, 
            orient='horizontal', 
            command=self.col_values_listbox_2.xview)
        col_values_lb_scroll_2_h.grid(row=2, column=0, pady=0, sticky='NSEW')
        self.col_values_listbox_2['xscrollcommand'] = col_values_lb_scroll_2_h.set

        # Create a label to place above the text widget 
        # that indicates that the widget displays values of the selected column
        column_values_tx_label = ttk.Label(
            middle_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Column Values'
            )
        column_values_tx_label.grid(row=0, column=0, padx=0, pady=5, sticky='W')

        # Create a text widget to present the values when a column is selected.
        # Displaying values gives the user more insight into which impute method to use.
        self.column_values_text = tk.Text(
            middle_frame, 
            font=("Segoe UI", 14),
            height=5,
            wrap=WORD)
        self.column_values_text.grid(row=1, column=0, padx=0, pady=5, sticky='NSEW')
        
        # Create scrollbar for text widget
        text_scroll = ttk.Scrollbar(middle_frame, orient='vertical', command=self.column_values_text.yview)
        text_scroll.grid(row=1, column=1, pady=5, sticky='NSEW')
        self.column_values_text['yscrollcommand'] = text_scroll.set

        # Create buttons and put in right frame
        replace_btn = ttk.Button(
            bottom_frame,
            text='Replace',
            width=16, command=self.reduce_synonyms_to_one_word)
        replace_btn.grid(row=0, column=0, padx=5, pady=5, sticky='E')

        close_btn = ttk.Button(
            bottom_frame, 
            text='Close', 
            width=16, 
            command=self.destroy
            )
        close_btn.grid(row=0, column=1, padx=5, pady=5, sticky='W')

    def populate_dict(self):
        '''
        Clear and populate dictionary 
        with columns (keys) and list of values (values).
        '''

        # Clear dictionary
        self.a_dict = {}
        # populate dictionary with initial or updated keys (i.e., column names) and 
        # values (i.e., list of unique column values)
        for col in self.cols_list:
            self.a_dict[col] = df[col].sort_values(na_position='first').unique().tolist()

    def column_selection(self, event):
        '''
        Receive event that represents a selection in the col_listbox selection.
        Upon receipt, populate/update the text widget and listboxes (col_values) 
        
        :param event: Listbox selection event
        :type event: object
        '''

        #-----BEGIN Updating Text Widget-----#

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

        #-----END Updating Text Widget-----#

        #-----BEGIN Updating Listbox Widgets-----#

        # Clear listboxes
        self.col_values_listbox_1.delete(0, END)
        self.col_values_listbox_2.delete(0, END)
        # Populate listboxes
        for value in list_of_values:
            self.col_values_listbox_1.insert(END, value)
            self.col_values_listbox_2.insert(END, value)

        #-----END Updating Listbox Widgets-----#      

    def reduce_synonyms_to_one_word(self):
        '''
        Reduce synonyms to one word.
        For example, if a column has the following terms:
        {'Country': ['US', 'U.S.', 'America, United States', 'United States of America', 'Canada']}, 
        after reducing synonyms, the column appears as:
        {'Country': ['United States of America', 'Canada']} 
        '''

        global df

        # Get the selected listbox item (column name)
        #col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
        # Get index of selected listbox item
        col_listbox_index = self.col_listbox.curselection()
        # Use index to get selected listbox item
        column_name = self.col_listbox.get(col_listbox_index)

        # Get the selected listbox items (column values to be replaced) and put in a list
        replace_these_values = [self.col_values_listbox_1.get(i) for i in self.col_values_listbox_1.curselection()]

        # Get the selected listbox item (substitute for column values to be replaced)
        col_values_listbox_2_index = self.col_values_listbox_2.curselection()
        # Use index to get selected listbox item
        with_this_value = self.col_values_listbox_2.get(col_values_listbox_2_index)

        # This list is needed to hold elements in the replace_the_values list,
        # after being checked for special characters. If spec chars exist in
        # an element, the application will miss it during replacment operation. 
        replace_these_vals_cleaned = []
        
        # Validate that the synonyms to be replaced don't have special characters. 
        for col_value in replace_these_values:
            col_value_before = col_value
            col_value = re.sub(r'[^a-zA-Z0-9\s]','',col_value)
            df = df.replace(col_value_before, col_value)
            replace_these_vals_cleaned.append(col_value)

        # Replace synonyms
        for col_value in replace_these_vals_cleaned:
            df[column_name] = df[column_name].str.replace(col_value, with_this_value)
            self.populate_dict()
            self.column_selection(None)
            
        # Send confirmation
        messagebox.showinfo(
            title="Reduce Synonyms to One Word", 
            message=f'Synonyms replaced.'
            )

class RemoveUnitsOfMeasurment(tk.Toplevel):
    '''
    This class is for the secondary window,
    RemoveUnitsOfMeasurment, of the TKinter application.
    It inherits from Tkinter's tk.Toplevel class.
    '''

    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        '''The constuctor for the RemoveUnitsOfMeasurement class.'''
        super().__init__(root)

        # Set window properties
        self.geometry('530x590')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Remove Units of Measurement')
        self.configure(bg='#1ac6ff')

        # Create left frame for listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=300, height=590)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)
        left_frame.grid_columnconfigure(0, weight=1)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=230, height=590)
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
            text='Columns'
            )
        # Place label in frame
        listbox_label.grid(row=0, column=0, padx=0, pady=5, sticky='W')

        # Create dictionary for columns and their unique values.
        # This dictionary is needed to dynamically populate the label as 
        # the user selects a column from the listbox
        self.a_dict = {}

        # Populate the dictionary with columns and values
        self.populate_dict()

        # Create a label to place above the text widget 
        # that indicates that the widget displays values 
        # of the selected column
        column_values_label = ttk.Label(
            left_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Column Values'
            )
        # Place label in frame
        column_values_label.grid(row=2, column=0, padx=0, pady=5, sticky='W')

        # Create a text widget to present the values when a column is selected.
        # Displaying values gives the user visibility of the data to be modified.
        self.column_values_text = tk.Text(
            left_frame, 
            font=("Segoe UI", 14), 
            height=6,
            wrap=WORD)
        #Place text widget in frame
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
        # Place label in frame
        action_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create buttons and put in right frame
        remove_units_btn = ttk.Button(
            right_frame,
            text='Remove Units',
            width=16, command=lambda: self.remove_units()
            )
        # Place button in frame
        remove_units_btn.grid(row=1, column=0, padx=5, pady=5, sticky='E')

        close_btn = ttk.Button(
            right_frame, 
            text='Close', 
            width=16, 
            command=self.destroy
            )
        # Place button in frame
        close_btn.grid(row=4, column=0, padx=5, pady=5, sticky='E')

    def get_col_list(self):
        '''
        Get and return list of columns 
        with which to populate listbox.
        '''

        # Get all columns that are of type object
        df1 = df.select_dtypes(include='object')
        
        # Make copy of dataframe.
        df2 = df1.copy(deep=True)
        
        # Get columns that have values starting with leading numeric strings or currency signs
        mask = df2.apply(lambda col: col.str.startswith(
            ('$', '€', '£', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')), axis=0)

        # Drop any columns that don't meet above criteria or that meets 
        # criteria but doesn't meet threshold of 50%
        droplist = [col for col in mask.columns if any(mask[col]) == False or mask[col].value_counts(normalize=True).to_dict()[True] < 0.5]
        mask.drop(droplist, axis=1, inplace=True)

        return mask.columns.to_list()

    def column_selection(self, event):
        '''
        Receive event that represents a selection in the col_listbox selection.
        Upon receipt, populate/update the text widget with col_values
        
        :param event: Listbox selection event
        :type event: object
        '''
        
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
        '''
        Clear and populate dictionary 
        with columns (keys) and list of values (values).
        '''
        
        # Clear dictionary
        self.a_dict = {}
        
        # populate dictionary with initial or updated keys (i.e., column names) and 
        # values (i.e., list of unique column values)
        for col in self.cols_list:
            self.a_dict[col] = df[col].sort_values(na_position='first').unique().tolist()

    def remove_units_of_measurement(self, x):
        '''
        Receive call from .apply() to remove 
        units of measurment from column string values
        and convert them to numeric values.
        
        :param x: Column string value with unit of measurement
        :type x: string

        :return x: Modified column value converted to float
        '''
        # try-except block is use here to handle any NaNs that may exist
        try:
            x = re.sub(r'[^0-9\.]','',x)
        except TypeError:
            pass
    
        return float(x)

    def remove_units(self):
        '''Remove units of measure from column values.'''

        # Get the selected listbox items and put in a list
        col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
        col_str = ', '.join(col_list)
        # Loop through col_list to remove units of measurement
        for col in col_list:
            df[col] = df[col].apply(self.remove_units_of_measurement)
        
        # Update dictionary of column's values
        self.populate_dict()
        # Update text widget to show the updated changes
        self.column_selection(None)

        # Send confirmation
        messagebox.showinfo(
            title="Remove Units of Measurment", 
            message=f'Units removed from Column(s) {col_str} values.'
            )

class RemovePercents(tk.Toplevel):
    '''
    This class is for the secondary window
    RemovePercents of the TKinter application.
    It inherits from Tkinter's tk.Toplevel class.
    '''

    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        '''The constuctor for the RemovePercents class.'''
        super().__init__(root)

        # Set window properties
        self.geometry('530x590')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Remove Percent Signs')
        self.configure(bg='#1ac6ff')

        # Create left frame for listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=300, height=590)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)
        left_frame.grid_columnconfigure(0, weight=1)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=230, height=590)
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
        # Place label in frame
        listbox_label.grid(row=0, column=0, padx=0, pady=5, sticky='W')

        # Create dictionary for columns and their unique values.
        # This dictionary is needed to dynamically populate the label as 
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
        # Place label in frame
        column_values_label.grid(row=2, column=0, padx=0, pady=5, sticky='W')

        # Create a text widget to present the values when a column is selected.
        # Displaying values gives the user visibility of the data to be modified.
        self.column_values_text = tk.Text(
            left_frame, 
            font=("Segoe UI", 14), 
            height=6,
            wrap=WORD)
        #Place text widget in frame
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
        # Place label in frame
        action_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create buttons and put in right frame
        remove_pct_sign_btn = ttk.Button(
            right_frame,
            text='Remove % Sign',
            width=16, command=lambda: self.remove_pct_sign()
            )
        # Place button in frame
        remove_pct_sign_btn.grid(row=1, column=0, padx=5, pady=5, sticky='E')

        close_btn = ttk.Button(
            right_frame, 
            text='Close', 
            width=16, 
            command=self.destroy
            )
        # Place button in frame
        close_btn.grid(row=4, column=0, padx=5, pady=5, sticky='E')

    def get_col_list(self):
        '''
        Get and return list of columns 
        with which to populate listbox.
        '''

        # Get all columns that are of type object
        df1 = df.select_dtypes(include='object')
    
        # Make copy of dataframe avoid SettingWithCopyWarning error
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
        df2 = df1.copy(deep=True)
    
        # Get columns that contain a percent sign
        # https://thispointer.com/pandas-select-dataframe-columns-containing-string/
        mask = df2.apply(lambda col: col.str.contains('%').any(), axis=0)
        df3 = df2.loc[: , mask]
    
        # Drop percent sign from dataframe.
        # This is needed to determine which columns contain majority numeric values
        df4 = df3.copy(deep=True)
        df4.replace('%', '', regex=True, inplace=True)
    
        # The presence of nulls will break the for loop, located below
        df4.dropna(inplace=True)
    
        # Place the column names in a list
        df4_col_list = df4.columns.to_list()
    
        # Get total number of rows in df4.  This number is needed to determine
        # the ratio of numeric values to total values in column
        total_rows = df4.shape[0]
    
        # Initialize a list to hold columns that have mostly numeric values and
        # have percent symbol in its values
        pct_cols = []
    
        # Loop through df4_col_list to determine which column has a ratio of numeric values
        # to total values greater than 90%.  Chances are that the column is a percent column
        for col in df4_col_list:
            # Get the number of column values that are numeric
            num_digits = df4[col].apply(lambda x: x.isnumeric()).sum()
            # If column has a majority of numeric values, add to list
            if num_digits / total_rows > 0.9:
                pct_cols.append(col)

        return pct_cols
    
    def column_selection(self, event):
        '''
        Receive event that represents a selection in the col_listbox selection.
        Upon receipt, populate/update the text widget with col_values 
        
        :param event: Listbox selection event
        :type event: object
        '''
        
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
        '''
        Clear and populate dictionary 
        with columns (keys) and list of values (values).
        '''
        
        # Clear dictionary
        self.a_dict = {}
        
        # populate dictionary with initial or updated keys (i.e., column names) and 
        # values (i.e., list of unique column values)
        for col in self.cols_list:
            self.a_dict[col] = df[col].sort_values(na_position='first').unique().tolist()

    def convert_pct_to_num(self, x):
        '''
        Receive call from .apply() to remove 
        % sign from column string values
        and convert them to numeric values.
        
        :param x: Column string value with % sign
        :type x: string

        :return x: Modified column value converted to int
        '''

        # try except is use here to handle and NaNs that may exist and break task
        try:
            x = x.replace('%','')
        except TypeError:
            pass

        return int(x)/100

    def remove_pct_sign(self):
        '''Remove percent sign from column value.'''

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
        messagebox.showinfo(
            title="Remove % Sign", 
            message=f'Percent removed from Column(s) {col_str} values.'
            )

class DummifyColumns(tk.Toplevel):
    '''
    This class is for the secondary window
    DummifyColumns of the TKinter application.
    It inherits from Tkinter's tk.Toplevel class.
    '''

    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        '''The constuctor for the DummifyColumns class.'''
        super().__init__(root)

        # Set window properties
        self.geometry('530x390')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Dummify Columns')
        self.configure(bg='#1ac6ff')

        # Create left frame for label and listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=300, height=390)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=230, height=390)
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
        self.col_listbox.grid(row=1, column=0, padx=0, pady=5, sticky='NS')

        # Create scrollbar for listbox
        lb_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.col_listbox.yview)
        lb_scroll.grid(row=1, column=1, pady=5, sticky='NSEW')
        self.col_listbox['yscrollcommand'] = lb_scroll.set
        
        # Create a label to place over list box 
        listbox_label = ttk.Label(
            left_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Object (String) Columns'
            )
        # Place label in frame
        listbox_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create Dummify button
        dummify_btn = ttk.Button(
            right_frame, 
            text='Dummify', 
            width=17, 
            command=self.dummify_columns)
        # Place button in frame
        dummify_btn.grid(row=1, column=0, padx=5, pady=5, sticky='W')

        # Create Dummify Drop First button
        dummify_drop_first_btn = ttk.Button(
            right_frame, 
            text='Dummify Drop First', 
            width=17, 
            command=self.dummify_columns_drop_first)
        # Place button in frame
        dummify_drop_first_btn.grid(row=2, column=0, padx=5, pady=5, sticky='W')

        # Create Close button
        dc_close_btn = ttk.Button(
            right_frame, 
            text='Close', 
            width=17, 
            command=self.destroy)
        # Place button in frame
        dc_close_btn.grid(row=3, column=0, padx=5, pady=5, sticky='W')

        # Create a label to place over buttons 
        listbox_label = ttk.Label(
            right_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Action'
            )
        # Place label in frame
        listbox_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

    def dummify_columns(self):
        '''Dummify specified columns.'''

        # Set df as global variable.  Without it, the application breaks.
        global df

        # Get the selected listbox items and put in a list
        col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
        # Dummify columns
        df = pd.get_dummies(df,columns=col_list, drop_first=True)
        # Notify User
        messagebox.showinfo(
            title="Dummify Columns", 
            message='Columns dummified.'
            )
        
    def dummify_columns_drop_first(self):
        '''Dummify columns with the drop_first option set to True'''

        # Set df as global variable.  Without it, the application breaks.
        global df 

        # Get the selected listbox items and put in a list
        col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
        # Dummify columns with drop_first set to True
        df = pd.get_dummies(df,columns=col_list, drop_first=True)
        # Notify user
        messagebox.showinfo(
            title="Dummify Columns", 
            message='Columns dummified.'
            )

class BinaryClassification(tk.Toplevel):
    '''
    This class is for the secondary window,
    BinaryClassification, of the TKinter application.
    It inherits from Tkinter's tk.Toplevel class.
    '''
    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        '''The constuctor for the BinaryClassification class.'''
        super().__init__(root)

        # Set window properties
        self.geometry('530x420')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Binary Classification of Target')
        self.configure(bg='#1ac6ff')

        # Set variable for combobox font. Use this variable when creating combobox  
        # https://www.delftstack.com/tutorial/tkinter-tutorial/tkinter-combobox/
        cb_font = font.Font(family="Segoe UI",size=14)
        # Set font of listbox that is embedded in combobox
        self.option_add('*TCombobox*Listbox.font', cb_font)     

        # Create left frame for label and listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=230, height=420)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)

        # Create middle frame for labels (header and target values)
        middle_frame = tk.Frame(self, bg='#1ac6ff', width=160, height=420)
        middle_frame.grid(row=0, column=1, padx=5, pady=5, sticky='NSEW')
        middle_frame.grid_propagate(0)
        middle_frame.grid_columnconfigure(0, weight=1)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=90, height=420)
        right_frame.grid(row=0, column=2, padx=5, pady=5, sticky='NSEW')
        right_frame.grid_propagate(0)
        #right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Create header label for listbox
        listbox_header_label = ttk.Label(
            left_frame,
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Select Target',
            width=12
            )
        # Place header in frame
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
            font = ('Segoe UI', 14),
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
            font = ('Segoe UI', 14),
            text='Values',
            width=12
            )
        # Place label in frame
        values_header_label.grid(row=0, column=0, padx=5, pady=5, sticky='')
        values_header_label.grid_columnconfigure(0, weight=1)

        # The following creates labels to display column values
        #
        # 1. Create string variables for value #1 and value #2
        self.col_val_1 = tk.StringVar()
        self.col_val_2 = tk.StringVar()

        # 2. Create labels and display in middle frame
        value1_label = ttk.Label(
            middle_frame,
            background='#ffffff',
            font = ('Segoe UI', 14),
            textvariable=self.col_val_1,
            width=15
            )
        value1_label.grid(row=1, column=0, padx=5, pady=5, sticky='')

        value2_label = ttk.Label(
            middle_frame,
            background='#ffffff',
            font = ('Segoe UI', 14),
            textvariable=self.col_val_2,
            width=15
            )
        value2_label.grid(row=2, column=0, padx=5, pady=5, sticky='')

        # Header for Categories (comboboxes)
        category_header_label = ttk.Label(
            right_frame,
            background='#1ac6ff',
            font = ('Segoe UI', 14),
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
            font=cb_font,
            exportselection=False
            )
        cb_category_0.current(0)
        cb_category_0.grid(row=1, column=0, padx=5, pady=5, sticky='')

        # - Create second combobox to hold category and display in right_frame
        cb_category_1 = ttk.Combobox(
            right_frame,
            textvariable=self.selected_category_1,
            values=(0, 1),
            state='readonly',
            width=2,
            font=cb_font,
            exportselection=False
            )
        cb_category_1.current(1)
        cb_category_1.grid(row=2, column=0, padx=5, pady=4, sticky='')

        # - Bind clickboxes to functions
        cb_category_0.bind('<<ComboboxSelected>>', self.category_selection_0)
        cb_category_1.bind('<<ComboboxSelected>>', self.category_selection_1)

        # The following creates buttons to categorize target values and to close window
        # - Create button style
        btn_style = ttk.Style()
        btn_style.configure('ttk.TButton', font=('Segoe UI', 14))

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
        '''
        Clear and populate dictionary 
        with columns (keys) and list of values (values).
        '''

        # Clear existing dictionary
        self.a_dict = {}
        # Populate dictionary
        for col in self.bin_cols:
            self.a_dict[col] = df[col].unique().tolist()

    def column_selection(self, event):
        '''
        Receive event that represents a selection in the col_listbox selection.
        Update labels in response to listbox selection

        :param event: Mouse click selection of listbox item
        :type event: object
        '''

        # Get the index of the listbox item (i.e. column name)
        selected_index = self.col_listbox.curselection()
        # Use index to get listbox item (i.e., column name)
        column_name = (self.col_listbox.get(selected_index))
        # Update the labels with the column values
        self.col_val_1.set(self.a_dict[column_name][0])
        self.col_val_2.set(self.a_dict[column_name][1])
                
    def category_selection_0(self, event):
        '''
        Receive event from first combobox monitor.
        Update second combobox value in response 
        to first combobox selection.

        :param event: Mouse click selection of first combobox item
        :type event: object
        '''

        if self.selected_category_0.get() == 0:
            self.selected_category_1.set(1)
        elif self.selected_category_0.get() == 1:
            self.selected_category_1.set(0)

    def category_selection_1(self, event):
        '''
        Receive event from second combobox monitor.
        Update first combobox value in response 
        to second combobox selection.

        :param event: Mouse click selection of second combobox item
        :type event: object
        '''

        if self.selected_category_1.get() == 0:
            self.selected_category_0.set(1)
        elif self.selected_category_1.get() == 1:
            self.selected_category_0.set(0)

    def categorize_target(self,target_col, value_1, category_1, value_2, category_2):
        '''
        Categorize target by converting its 
        string values (i.e., No/Yes) to 0/1,
        respectively.

        :param target_col: Name of column whose values to convert.
        :type target_col: string

        :param value_1: A column value
        :type value_1: string

        :param value_2: A column value
        :type value_1: string

        :param category_1: A number, either 0 or 1
        :type category_1: int

        :param category_2: A number, either 0 or 1
        :type category_2: int     
        '''

        # Set df as global variable.  Without it, the application breaks.
        global df
        df[target_col] = df[target_col].map({value_1: category_1, value_2: category_2})

        messagebox.showinfo(
            title="Categorize Target", 
            message=f'Target {target_col} categorized.'
            )

class DropColumns(tk.Toplevel):
    '''
    This class is for the secondary window,
    DropColumns, of the TKinter application.
    It inherits from Tkinter's tk.Toplevel class.
    '''

    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        '''The constuctor for the DropColumns class.'''
        super().__init__(root)

        # Set window properties
        self.geometry('510x400')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Drop Columns')
        self.configure(bg='#1ac6ff')

        # Create left frame for label and listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=300, height=400)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=210, height=400)
        right_frame.grid(row=0, column=1, padx=5, pady=5)
        #right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_propagate(0)

        # The following creates a list box
        # 1. Get column names
        col_idxs = df.columns
        # 2. Convert the index to a tuple
        cols = tuple(col_idxs)
        # 3. Create listvariable for listbox.  This step also populates listbox
        col_list_var = tk.StringVar(value=cols)
        # 4. Create listlistbox and place in left frame
        self.col_listbox = tk.Listbox(
            left_frame, 
            listvariable=col_list_var, 
            selectmode='extended')
        # 5. Display listbox in frame
        self.col_listbox.grid(row=1, column=0, padx=0, pady=5, sticky='NS')

        # Create scrollbar for listbox
        lb_scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.col_listbox.yview)
        lb_scroll.grid(row=1, column=1, pady=5, sticky='NSEW')
        self.col_listbox['yscrollcommand'] = lb_scroll.set
        
        # Create a label to place over listbox
        listbox_label = ttk.Label(
            left_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='DataFrame Columns'
            )
        listbox_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create buttons and display in frame
        dc_dropcols_btn = ttk.Button(
            right_frame, 
            text='Drop Columns', 
            width=15, 
            command=lambda: drop_columns(self))
        dc_dropcols_btn.grid(row=1, column=0, padx=5, pady=5, sticky='EW')

        dc_close_btn = ttk.Button(
            right_frame, 
            text='Close', 
            width=15, 
            command=self.destroy)
        dc_close_btn.grid(row=2, column=0, padx=5, pady=5, sticky='EW')

        # Create a label to place over buttons
        listbox_label = ttk.Label(
            right_frame, 
            background='#1ac6ff',
            font = ('Segoe UI', 14),
            text='Actions'
            )
        listbox_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        def drop_columns(self):
            '''Drop columns in DataFrame'''

            # Get the selected listbox items and put in a list
            col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
            
            # Drop selected column(s)
            df.drop(columns=col_list, inplace=True)

            # Update listbox
            # https://stackoverflow.com/a/42485391
            # 1. Clear listbox
            self.col_listbox.delete(0, END)
            # 2. Repopulate listbox
            for col in df.columns:
                self.col_listbox.insert(END, col)

            # Send confirmation to user that column(s) was/were dropped
            messagebox.showinfo(
                title="Drop Columns", 
                message=f'Column(s) {col_list} dropped.'
                )

class FillForward(tk.Toplevel):
    '''
    This class is for the secondary window,
    FillForward, of the TKinter application.
    It inherits from Tkinter's tk.Toplevel class.
    '''

    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        '''The constuctor for the FillForward class.'''
        super().__init__(root)

        # Set window properties
        self.geometry('520x550')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Fill Forward')
        self.configure(bg='#1ac6ff')

        # Create left frame for listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=300, height=550)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)
        left_frame.grid_columnconfigure(0, weight=1)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=220, height=550)
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
            height=5,
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
        fill_forward_btn = ttk.Button(
            right_frame,
            text='Fill Fwd/Bkwd',
            width=16, command=self.fill_forward)
        fill_forward_btn.grid(row=1, column=0, padx=5, pady=5, sticky='E')

        close_btn = ttk.Button(
            right_frame, 
            text='Close', 
            width=16, 
            command=self.destroy
            )
        close_btn.grid(row=4, column=0, padx=5, pady=5, sticky='E')

    def populate_dict(self):
        '''
        Clear and populate dictionary 
        with columns (keys) and list of values (values).
        '''

        # Clear dictionary
        self.a_dict = {}
        # populate dictionary with initial or updated keys (i.e., column names) and 
        # values (i.e., list of unique column values)
        for col in self.cols_list:
            self.a_dict[col] = df[col].sort_values(na_position='first').unique().tolist()

    def column_selection(self, event):
        '''
        Receive event that represents a selection in the col_listbox selection.
        Upon receipt, populate/update the text widget with col_values.
        
        :param event: Listbox selection event
        :type event: object
        '''

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

    def fill_forward(self):
        '''Impute missing values using the ffill and bfill methods'''

        # Get the selected listbox items and put in a list
        col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
        col_str = ', '.join(col_list)
        # Loop through col_list to impute missing values with the ffill and bfill methods
        for col in col_list:
            df[col].fillna(method='ffill', inplace=True)
            df[col].fillna(method='bfill', inplace=True)
            self.populate_dict()
            self.column_selection(None)
            
        # Send confirmation
        messagebox.showinfo(
            title="Impute with Forward/Back Fill", 
            message=f'Column(s) {col_str} imputed with forward/backward propagation.'
            )

class ImputeNullsWithMean(tk.Toplevel):
    '''
    This class is for the secondary window,
    ImputeNullsWithMean, of the TKinter application.
    It inherits from Tkinter's tk.Toplevel class.
    '''

    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        '''The constuctor for the ImputeNullwithMean class.'''
        super().__init__(root)

        # Set window properties
        self.geometry('520x550')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Impute Nulls with Mean, Mode, Median')
        self.configure(bg='#1ac6ff')

        # Create left frame for listbox
        left_frame = tk.Frame(self, bg='#1ac6ff', width=300, height=550)
        left_frame.grid(row=0, column=0, padx=5, pady=5)
        left_frame.grid_propagate(0)
        left_frame.grid_columnconfigure(0, weight=1)

        # Create right frame for buttons
        right_frame = tk.Frame(self, bg='#1ac6ff', width=220, height=550)
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
            height=5,
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
        '''
        Clear and populate dictionary 
        with columns (keys) and list of values (values).
        '''

        # clear dictionary
        self.a_dict = {}
        # populate dictionary with initial or updated keys (i.e., column names) and 
        # values (i.e., list of unique column values)
        for col in self.cols_list:
            self.a_dict[col] = df[col].sort_values(na_position='first').unique().tolist()

    def column_selection(self, event):
        '''
        Receive event that represents a selection in the col_listbox selection.
        Upon receipt, populate/update the text widget with col_values.
        
        :param event: Listbox selection event
        :type event: object
        '''

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
        '''
        Impute missing values with either mean, mode, or median.

        :param impute_method: the method with which to impute missing values
        :type impute_method: string
        '''
        # Get the selected listbox items and put in a list
        impute_value = None
        col_list = [self.col_listbox.get(i) for i in self.col_listbox.curselection()]
        col_str = ', '.join(col_list)

        # Loop through col_list to impute each column with selected value (i.e., mean, mode, median)
        for col in col_list:
            if impute_method == 'mean':
                impute_value = int(df[col].mean())
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
        messagebox.showinfo(
            title="Impute with MMM", 
            message=f'Column(s) {col_str} imputed with a {impute_method} of {impute_value}.'
            )

class RemoveRowsWithXNullsWindow(tk.Toplevel):
    '''
    This class is for the secondary window
    RemoveRowsWithXNulls of the TKinter application.
    It inherits from Tkinter's tk.Toplevel class.
    '''

    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        '''The constuctor for the RemoveRowsWithXNullsWindow class.'''
        super().__init__(root)

        # Set window properties
        self.geometry('400x120')
        try:
            self.iconbitmap('./images/panda.ico')
        except:
            self.iconbitmap(my_dir / './images/panda.ico')
        self.resizable(0,0)
        self.title('Remove Rows with High Number of Missing Values')
        self.configure(bg='#1ac6ff')

        # Create top frame for window
        top_frame = tk.Frame(self, bg='#1ac6ff', width=400, height=55)
        top_frame.grid(row=0, column=0, padx=5, pady=5)
        top_frame.grid_propagate(0)

        # Create bottom frame for window
        bottom_frame = tk.Frame(self, bg='#1ac6ff', width=400, height=65)
        bottom_frame.grid(row=1, column=0, padx=5, pady=5)

        # Create label and display in frame
        remove_rows_label = ttk.Label(
            top_frame, 
            background='#1ac6ff',
            width=32,
            font = ('Segoe UI', 14),
            text='Select % values missing threshold:'
            )
        remove_rows_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create variable to percent value
        self.selected_percent = tk.IntVar()
        
        # Set variable for combobox font. Use this variable when creating combobox
        # https://www.delftstack.com/tutorial/tkinter-tutorial/tkinter-combobox/
        cb_percentage_font = ('Segoe UI', 15)
        # Set font of listbox that is embedded in combobox
        self.option_add('*TCombobox*Listbox.font', cb_percentage_font)

        # Create comboxbox for percentages and display in frame
        cb_percentage = ttk.Combobox(
            top_frame, 
            textvariable=self.selected_percent,
            values=(99, 95, 90, 80, 70, 60, 50),
            state='readonly', # switch to 'normal' to enable editing
            width=2,
            exportselection=False,
            font=cb_percentage_font
            )
        # Set default value of combobox. 2 refers to the index of values tuple, wich is 90.
        cb_percentage.current(2)
        # Position combobox in frame
        cb_percentage.grid(row=0, column=1, padx=5, pady=5, sticky='W')

        # Create button widget to fill nulls
        remove_rows_btn = ttk.Button(
            bottom_frame,
            text='Remove Rows',
            command=lambda: self.remove_rows(self.selected_percent.get())
            )
        remove_rows_btn.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create button widget to fill nulls
        close_btn = ttk.Button(
            bottom_frame,
            text='Close',
            command=self.destroy
            )
        close_btn.grid(row=0, column=1, padx=5, pady=5, sticky='E')

    def remove_rows(self, pct):
        '''
        Drop rows based on a percentage of missing values.
        For example, if a row is missing 90% (9/10) of its
        values, then it is dropped.

        :param pct: Percent threshold of missing values to trigger drop.
        :type pct: int
        '''

        # Convert percent integer value to a decimal
        pct = pct/100

        # Get number of rows before removal of rows.
        num_rows_before = df.shape[0]

        # Get number of columns
        num_cols = df.shape[1]

        # Get series of rows and the number of its missing values 
        rows_with_nulls = df.isnull().sum(axis=1)

        # Determine missing value threshold-- the number of missing values
        # that will trigger row deletion
        missing_thresh = int(pct*num_cols)

        # Get number of rows to be deleted
        num_rows_to_be_deleted = len(df.loc[rows_with_nulls>=missing_thresh])

        # Get percent of total rows to be deleted
        pct_of_total_rows = round((num_rows_to_be_deleted/num_rows_before)*100,2)

        # Ask the user if they want to delete specfied number of rows
        question = messagebox.askyesno(
            title="Drop Rows Exceeding Null Threshold", 
            message=f"Drop {num_rows_to_be_deleted} rows, ({pct_of_total_rows}% of data)?"
            )

        # If the user answers Yes, then proceed to delete rows
        if question == 1:
            # Determine value for dropna thresh option: dropna(thresh=)
            threshold = num_cols - missing_thresh + 1
            # Drop rows
            df.dropna(thresh=threshold, inplace=True)
            # Notify user that rows have been deleted
            messagebox.showinfo(
                title="Drop Rows Exceeding Null Threshold", 
                message=f'{num_rows_to_be_deleted} rows, ({pct_of_total_rows}% of data), deleted.'
                )

class FillAllNullsWindow(tk.Toplevel):
    '''
    This class is for the secondary window,
    FillAllNulls, of the TKinter application.
    It inherits from Tkinter's tk.Toplevel class.
    '''

    # Set df variable as global variable to enable all functions to modify it
    global df

    def __init__(self, root):
        '''The constuctor for the FillAllNullsWindow class.'''
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
        # Place label in frame
        fillna_all_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        # Create variable to hold fillna value
        self.fillna_all_value = tk.StringVar()

        # Create entry widget for user to enter fillna value
        fillna_all_input = ttk.Entry(
            fillna_all_frame, 
            textvariable=self.fillna_all_value,
            justify='center',
            font=('Segoe UI', 15)
            )
        # Place entry widget in frame
        fillna_all_input.grid(row=0, column=1, padx=5, pady=5, sticky='EW')
        # Set the entry frame to receive focus when window opens
        fillna_all_input.focus()

        # Create button widget to fill nulls
        fillna_all_btn = ttk.Button(
            fillna_all_frame,
            text='Fill Nulls',
            command=lambda: self.fill_all_nulls(self.fillna_all_value.get())
            )
        # Place button in frame
        fillna_all_btn.grid(row=1, column=0, padx=5, pady=5)

        # Create button widget to close window
        fillna_all_close_btn = ttk.Button(
            fillna_all_frame,
            text='Close',
            command=self.destroy
            )
        # Place button in frame
        fillna_all_close_btn.grid(row=1, column=1, padx=5, pady=5)

    def fill_all_nulls(self, impute_value):
        '''
        Impute null values with a specific value.
        
        :param impute_value: Value with which to replace null value
        :type impute_value: string, int, or float
        '''

        # Get number of nulls    
        num_of_nulls = int(df.isnull().sum().sum())
        # Ask user if they want to impute nulls with specified value
        question = messagebox.askyesno(
            title="Impute Nulls", 
            message=f"Impute {num_of_nulls} nulls with {impute_value}?")
        # If the user answers Yes, proceed with replacement of nulls
        if question == 1:
            # Impute nulls
            df.fillna(impute_value, inplace=True)
            # Notify user that null were imputed
            messagebox.showinfo(
                title="Impute Nulls", 
                message=f'{num_of_nulls} nulls imputed.')
    
# Bootstrap application
if __name__ == "__main__":
    root = PandasDataCleaner()
    # Set global font.  Doesn't apply to fields.  
    font.nametofont('TkDefaultFont').configure(size=15)
    root.mainloop()
