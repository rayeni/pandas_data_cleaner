[![](./images/interface.png)](https://pandasdatacleaner.com/)

Pandas Data Cleaner is a Python interactive data cleaning tool that allows users to quickly clean data in a few mouse clicks.

## Highlights

*  Simply point-and-click to clean data.
*  Easy to read [documentation.](https://pandasdatacleaner.com/documentation/)
*  No dependencies for standalone versions of Windows, macOS, and Ubuntu Linux
*  If running from source, dependencies are Pandas, Scikit-learn, and Pillow

## Installation

### Executable
* [Download](https://pandasdatacleaner.com/download/) the zip file for your specific operating system.
* Unzip the package.
* Find and run the pandas_data_cleaner.exe file.

### Source
* Clone or download the repo.
* Find and run the pandas_data_cleaner.py file.


## Documentation

See the complete documentation at https://pandasdatacleaner.com/documentation/

## Features

|Feature|Description|
|---|---|
|[**Import Data**](https://pandasdatacleaner.com/documentation/#import-data)|Imports data from a CSV file.|
|[**Fix Missing Data -> Drop All Nulls**](https://pandasdatacleaner.com/documentation/#drop-all-nulls)|Drops all nulls from dataframe.|
|[**Fix Missing Data -> Fill All Nulls w/Specific Value**](https://pandasdatacleaner.com/documentation/#fill-all-nulls-with-specific-value)|Imputes all nulls with a specific value at dataframe level.|
|[**Fix Missing Data -> Drop Rows with X Pct of Nulls**](https://pandasdatacleaner.com/documentation/#drop-rows-with-x-pct-of-nulls)|Finds and removes rows with a certain percentage of missing values.|
|[**Fix Missing Data -> Fill Forward/Backward**](https://pandasdatacleaner.com/documentation/#fill-forward-backward)|Identifies numeric columns with nulls. User selects column in which to impute null values.|
|[**Fix Missing Data -> Impute w/Mean, Mode, Median**](https://pandasdatacleaner.com/documentation/#impute-with-mean-mode-median)|User can select which method to use to impute nulls.|
|[**Fix Missing Data -> Impute with KNN**](https://pandasdatacleaner.com/documentation/#impute-with-knn)|User can use KNNImputer to impute nulls.|
|[**DataFrame Tasks -> Drop Columns**](https://pandasdatacleaner.com/documentation/#drop-columns)|User can select one of several columns to drop.|
|[**DataFrame Tasks -> Change Column Names to Lowercase**](https://pandasdatacleaner.com/documentation/#change-column-names-to-lowercase)|Change columns names to lowercase, and replace spaces with underscores.|
|[**Clean Numerics -> Remove Percent Signs**](https://pandasdatacleaner.com/documentation/#remove-percent-signs)|Remove percent sign from value. Convert value to numeric and divide by 100.|
|[**Clean Numerics -> Remove Units of Measurement**](https://pandasdatacleaner.com/documentation/#remove-units-of-measurement)|Convert values such as 10s, $2,000, and 24hrs to 10, 2000, and 24, respectively.|
|[**Categorize Data -> Classify Target (0/1)**](https://pandasdatacleaner.com/documentation/#classify-target)|Convert target values such as 'Yes' and 'No' to 1 and 0, respectively.|
|[**Categorize Data -> Dummify Columns**](https://pandasdatacleaner.com/documentation/#dummify-columns)|Converts a column’s string values to numeric values.|
|[**Clean String Data -> Remove Trailing/Leading Spaces**](https://pandasdatacleaner.com/documentation/#remove-trailing-spaces)|Reduces duplicate values by removing trailing/leading whitespaces.|
|[**Clean String Data -> Remove Special Characters**](https://pandasdatacleaner.com/documentation/#remove-special-characters)|Removes special characters by comparing data chars to known special chars.|
|[**Clean String Data -> Change Column Values to Lowercase**](https://pandasdatacleaner.com/documentation/#change-column-values-to-lowercase)|Converts all text data to lowercase.|
|[**Clean String Data -> Replace Synonyms with Single Word**](https://pandasdatacleaner.com/documentation/#replace-synonyms-with-single-word)|User can replace multiple values such as **\[U.S., United States, U.S.A., US, USA, United States of America\]** with a single term, **USA.**|
|[**Clean String Data -> Replace NA (False NaN) with N.A.**](https://pandasdatacleaner.com/documentation/#replace-false-nan-with-na)|This feature finds and replaces false NaNs, (NA) with N.A.|
|[**DateTime -> Set Date to Index**](https://pandasdatacleaner.com/documentation/#set-date-to-index)|This feature finds the Date column and sets it the index.|
|[**DateTime -> Index to DatetimeIndex**](https://pandasdatacleaner.com/documentation/#index-datetime)|This feature determines if the Index is comprised of date data.  If it has date data, then it is converted to a DatetimeIndex.|


## Bug reports & Feature Requests

For bug reports and feature requests, open an issue [here](https://github.com/rayeni/pandas_data_cleaner/issues)

## License

Licensed under [BSD](https://github.com/rayeni/pandas_data_cleaner/blob/main/LICENSE.txt)

## Contact

info@pandasdatacleaner.com
