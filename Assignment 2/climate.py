from collections import defaultdict
import time
class ClimateData:

    def __init__(self, date: str, max_gust: int, total_precipitation: float, min_temperature: float, max_temperature: float, avg_temperature: float):
        self.date = date
        self.max_gust = max_gust
        self.total_precipitation = total_precipitation
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.avg_temperature = avg_temperature

# Function to parse the climate data from the file
def parseClimateData(filename: str) -> list[ClimateData]:
    data = []

    with open(filename, 'r') as file:
        for line in file:
            try:
                date, max_gust, total_precipitation, min_temperature, max_temperature, avg_temperature = line.split(',')

                data.append(ClimateData(date, int(max_gust), float(total_precipitation), float(min_temperature), float(max_temperature), float(avg_temperature)))
            except ValueError:
                # dont include lines that are not formatted correctly
                continue
    
    return data

# Function to convert the date from the format YYYY-MM-DD to a more readable format
def convertDateTime(date: str, type: str) -> str:
    months = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}
    if type == "day":
        return f"{months[date.split('-')[1]]} {date.split('-')[2].split(' ')[0]} {date.split("-")[0]}"
    elif type == "month":
        return f"{months[date.split("-")[1]]} {date.split("-")[0]}"

# Function to analyze the climate data
def analyzeData(data: list[ClimateData]) -> None:

    max_precipitation = 0
    max_gust_day = None
    max_gust = 0
    max_temp_fluctuation_day = None
    max_temp_fluctuation = 0
    precipitation_per_month = defaultdict(float)

    for value in data:
        month_key = (convertDateTime(value.date, "month"))
        precipitation_per_month[month_key] += value.total_precipitation

        if value.max_gust > max_gust:
            max_gust = value.max_gust
            max_gust_day = value.date

        if value.max_temperature - value.min_temperature > max_temp_fluctuation:
            max_temp_fluctuation = value.max_temperature - value.min_temperature
            max_temp_fluctuation_day = value.date
    
    max_precipitation_month, max_precipitation = max(precipitation_per_month.items(), key=lambda item: item[1])
    print("\n--Climate Data Analysis--")
    print(f"Month with the most precipitation: {max_precipitation_month} with {max_precipitation:.2f}mm")
    print(f"Day with the highest gust: {convertDateTime(max_gust_day, "day")} with {max_gust}km/h")
    print(f"Day with the highest temperature fluctuation: {convertDateTime(max_temp_fluctuation_day, "day")} with {max_temp_fluctuation:.2f}°C\n")

# Function to generate a user generated report
def userGeneratedReport(data: list[ClimateData]) -> None:
    while True:
        print("1. Monthly report")
        print("2. Weather records between two dates")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            start_time = time.time()
            monthly_report(data)
            end_time = time.time()
            print(f"Monthly report took {end_time - start_time} seconds to run.")
        elif choice == '2':
            start_date = input("Enter the start date (YYYY-MM-DD): ")
            end_date = input("Enter the end date (YYYY-MM-DD): ")
            date_range_report(data, start_date, end_date)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

# Function to generate a monthly report
def monthly_report(data: list[ClimateData]) -> None:
    # create a dictionary with default values for each month
    months = defaultdict(lambda: {"count": 0, "max_gust": 0, "total_precipitation": 0, "min_temperature": float('inf'), "max_temperature": float('-inf'), "avg_temperature": 0})

    for value in data:
        month = convertDateTime(value.date, "month")
        months[month]["count"] += 1
        months[month]["max_gust"] += value.max_gust
        months[month]["total_precipitation"] += value.total_precipitation
        months[month]["min_temperature"] = min(months[month]["min_temperature"], value.min_temperature)
        months[month]["max_temperature"] = max(months[month]["max_temperature"], value.max_temperature)
        months[month]["avg_temperature"] += value.avg_temperature

    for month, values in months.items():
        print(f"Month: {month}")
        print(f"Average Max Gust: {values['max_gust'] / values['count']:.2f}")
        print(f"Total Precipitation: {values['total_precipitation']:.2f}")
        print(f"Min Temperature: {values['min_temperature']:.2f}")
        print(f"Max Temperature: {values['max_temperature']:.2f}")
        print(f"Mean Temperature: {values['avg_temperature'] / values['count']:.2f}")
        print()

# Function to generate a report for a date range
def date_range_report(data: list[ClimateData], start_date: str, end_date:str):

    for value in data:
        if value.date >= start_date and value.date <= end_date:
            print(f"\nDate: {convertDateTime(value.date, 'day')}")
            print(f"Max Gust: {value.max_gust}km/h")
            print(f"Total Precipitation: {value.total_precipitation}mm")
            print(f"Min Temperature: {value.min_temperature}°C")
            print(f"Max Temperature: {value.max_temperature}°C")
            print(f"Avg Temperature: {value.avg_temperature}°C\n")

if __name__ == "__main__":
    data = parseClimateData("Assignment 2/climate-daily.csv")
    analyzeData(data)
    userGeneratedReport(data)