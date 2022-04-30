import pandas as pd
from pprint import pprint
from settings import YEAR_TO_CHECK, MONTH_TO_CHECK, DAYS_LIST_TO_CHECK
from utils import get_dates, get_flights

# Setting options to print DataFrames properly
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

if __name__ == "__main__":
    # Get all dates to query in Ryanair.get_return_flights
    dates_for_ra = get_dates(DAYS_LIST_TO_CHECK, MONTH_TO_CHECK, YEAR_TO_CHECK)
    pprint(dates_for_ra)

    # Get DataFrames of flights and cheapest flights
    flights_df, cheapest_df = get_flights(dates_for_ra)

    # Export DataFrames to XLSX File to view in excel
    flights_df.to_excel("Flights.xlsx")
    cheapest_df.to_excel("Cheapest Flights.xlsx")

    # Print TOP 5 flights in month
    print(cheapest_df[["Total Price",
                       "Origin",
                       "Destination",
                       "Departure Flight DateTime",
                       "Return Flight DateTime"]]
          .sort_values("Total Price").head())
