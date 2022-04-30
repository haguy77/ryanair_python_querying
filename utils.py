import pandas as pd
from ryanair import Ryanair
from datetime import datetime, timedelta
from settings import AIRPORT, DAYS_DICT, DATE_FORMAT, DATETIME_WEEKDAYS_DICT, DAYS_TO_ADD_DICT


def get_dates(days: list, month: int, year=2022) -> list:
    """
    Get the dates to search flights in.

    :param days: list of the departure dates
    :param month: month of flight dates
    :param year: year of the flight dates
    :return: list of tuple strings to search flights in ryanair
    """
    # Convert digits days to string days for pd.date_range freq argument
    days_str = [DAYS_DICT[day] for day in days]

    # Print settings of dates
    print("Days entered in strings: " + ", ".join(days_str))
    print(f"Month entered in int: {month}")
    print(f"Year entered in int: {year}")
    print("Days to add entered:")
    print(DAYS_TO_ADD_DICT)

    # Create datetime of inputted month start
    month_start = datetime.strptime(f"01/{month}/{year}", DATE_FORMAT)

    # Create a list of departure dates by loop all days of week inputted in the month inputted and compute for each one
    departure_dates = []
    for day in days_str:
        days_pd = pd.date_range(
            start=month_start,
            end=month_start+timedelta(days=31),
            freq=f"W-{day}"
        )
        departure_dates.extend(days_pd.tolist())
    departure_dates = [timestamp.to_pydatetime() for timestamp in departure_dates]

    # Loop over departure dates and compute optional return dates for them
    tuple_flight_dates = []
    for departure_date in departure_dates:
        tuple_flight_dates.extend(compute_returns(departure_date))

    # Convert tuple_flight_dates to list of tuple of string that are suited for Ryanair.get_return_flights
    tuple_flight_dates = [(f"{tuple_flight_date[0].year}-{'{:02d}'.format(tuple_flight_date[0].month)}-{'{:02d}'.format(tuple_flight_date[0].day)}", f"{tuple_flight_date[1].year}-{'{:02d}'.format(tuple_flight_date[1].month)}-{'{:02d}'.format(tuple_flight_date[1].day)}") for tuple_flight_date in tuple_flight_dates]
    return tuple_flight_dates


def compute_returns(dep: datetime):
    """
    Compute all monthly flight dates according to dep and settings.DAYS_TO_ADD_DICT

    :param dep: departure date
    :return: list of all flight dates that are suited for dep.weekday() departure date and settings.DAYS_TO_ADD_DICT
    """
    returns = []
    dep_weekday = DATETIME_WEEKDAYS_DICT[dep.weekday()]
    days_to_add = DAYS_TO_ADD_DICT[dep_weekday]
    for day_to_add in days_to_add:
        returns.append((dep, dep + timedelta(days=day_to_add)))
    return returns


def get_flights(dates: list) -> tuple:
    """
    Get 2 DataFrames of all flights in dates list and cheapest flights in each date

    :param dates: list of dates to check flights and cheapest flight in
    :return: tuple contains 2 pandas.DataFrame - all flights DataFrame and cheapest flights DataFrame
    """
    # Initialize Ryanair instance
    ra = Ryanair("EUR")

    # Create empty all flights df and empty cheapest flights df
    flights_df = pd.DataFrame(columns=[
        "Total Price", "Origin", "Destination", "Departure Flight DateTime", "Return Flight DateTime",
        "Departure Flight Price", "Return Flight Price", "Origin Code", "Destination Code",
        # "Departure Flight Date", "Departure Flight Time", "Return Flight Date", "Return Flight Time"
    ])
    cheapest_flights = pd.DataFrame(columns=flights_df.columns.tolist())

    # Loop over dates and query Ryanair for each one
    for flight_date in dates:
        flights = ra.get_return_flights(
            AIRPORT,
            flight_date[0], flight_date[0],
            flight_date[1], flight_date[1]
        )
        # Loop over every flight and append to flights_df and cheapest_flights if cheapest
        for flight in flights:
            flight_df = pd.DataFrame({
                flights_df.columns[0]: [flight.totalPrice],
                flights_df.columns[1]: [flight.outbound.originFull],
                flights_df.columns[2]: [flight.outbound.destinationFull],
                flights_df.columns[3]: [flight.outbound.departureTime],
                flights_df.columns[4]: [flight.inbound.departureTime],
                flights_df.columns[5]: [flight.outbound.price],
                flights_df.columns[6]: [flight.inbound.price],
                flights_df.columns[7]: [flight.outbound.origin],
                flights_df.columns[8]: [flight.outbound.destination],
            })
            flights_df = pd.concat([flights_df, flight_df])
            if flight == flights[0]:  # Cheapest flight is first after Ryanair's query
                cheapest_flights = pd.concat([cheapest_flights, flight_df])

    # Rearrange DataFrames' index
    flights_df = flights_df.reset_index(drop=True)
    cheapest_flights = cheapest_flights.reset_index(drop=True)
    return flights_df, cheapest_flights
