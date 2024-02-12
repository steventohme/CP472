class ClimateData:

    def __init__(self, date: str, max_gust: int, total_precipitation: float, min_temperature: float, max_temperature: float, avg_temperature: float):
        self.date = date
        self.max_gust = max_gust
        self.total_precipitation = total_precipitation
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.avg_temperature = avg_temperature

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
def convertDateTime(date: str, type: str) -> str:
    months = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}
    if type == "day":
        return f"{months[date.split('-')[1]]} {date.split('-')[2]}"
    elif type == "month":
        return months[date.split("-")[1]]

def analyze_data(data: list[ClimateData]) -> None:

    max_percip_month = None
    max_percip = 0
    max_gust_day = None
    max_gust = 0
    max_temp_fluctuation_day = None
    max_temp_fluctuation = 0

    for value in data:
        if value.total_precipitation > max_percip:
            max_percip = value.total_precipitation
            max_percip_month = value.date

        if value.max_gust > max_gust:
            max_gust = value.max_gust
            max_gust_day = value.date

        if value.max_temperature - value.min_temperature > max_temp_fluctuation:
            max_temp_fluctuation = value.max_temperature - value.min_temperature
            max_temp_fluctuation_day = value.date
    
    print(f"Month with the most precipitation: {max_percip_month} with {max_percip}mm")
    print(f"Day with the highest gust: {max_gust_day} with {max_gust}km/h")
    print(f"Day with the highest temperature fluctuation: {max_temp_fluctuation_day} with {max_temp_fluctuation}°C")

if __name__ == "__main__":
    data = parseClimateData("Assignment 2/climate-daily.csv")
    analyze_data(data)