AIRPORT = "TLV"

# Date constants to change as wanted
YEAR_TO_CHECK = 2022
MONTH_TO_CHECK = 5
DAYS_LIST_TO_CHECK = [4, 5, 6, 7]
# Dates to add for each day to check, change as wanted
# Example: For checking all Wednesday-Friday and all Wednesday-Saturday - {4: [2, 3]}
DAYS_TO_ADD_DICT = {
    4: [2, 3, 4],
    5: [2, 3, 4],
    6: [2, 3],
    7: [2]
}


DAYS_DICT = {
    1: "SUN",
    2: "MON",
    3: "TUE",
    4: "WED",
    5: "THU",
    6: "FRI",
    7: "SAT"
}
DATETIME_WEEKDAYS_DICT = {
    6: 1,
    0: 2,
    1: 3,
    2: 4,
    3: 5,
    4: 6,
    5: 7
}
DATE_FORMAT = "%d/%m/%Y"
