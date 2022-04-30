# Ryanair Python Querying

This script allows querying ryanair and finding each flights and cheapest flight according to inputted settings.  
This is using the ryanair-py package, pandas and datetime modules.  
### Installation
Run the following command in the terminal:
```
pip install -r requriements.txt
```
### Running
Change the settings in settings.py of AIRPORT, YEAR_TO_CHECK, MONTH_TO_CHECK, DAYS_LIST_TO_CHECK, DAYS_TO_ADD_DICT.
Default is set to query all Wednesday-Saturday departures and returns after 2-4 days if departure on Wednesday or 
Thursday, 2-3 days if on Friday and 2 days if on Saturday, on May 2022 from TLV airport.

After configuring settings.py run the following command:
```
cd ryanair_python_querying
python main.py
```
### Output
The output will print in the console all the settings, all the dates calculated, 
and table of top 5 cheapest flights queried.

In addition, 2 XLSX files will generate in the directory:
1. Flights.xlsx - Excel file of all the flights queried
2. Cheapest Flights.xlsx - Excel file of cheapest flight in each date queried
