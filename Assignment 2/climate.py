class ClimateData:

    def __init__(self, date: str, max_gust: int, total_precipitation: float, min_temperature: float, max_temperature: float, avg_temperature: float):
        self.date = date
        self.max_gust = max_gust
        self.total_precipitation = total_precipitation
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.avg_temperature = avg_temperature

def parseClimateData(filename: str):
    data = []

    with open(filename, 'r') as file:
        for line in file:
            try:
                date, max_gust, total_precipitation, min_temperature, max_temperature, avg_temperature = line.split(',')

                data.append(ClimateData(date, int(max_gust), float(total_precipitation), float(min_temperature), float(max_temperature), float(avg_temperature)))
            except ValueError:
                # dont include lines that are not formatted correctly
                continue

if __name__ == "__main__":
    parseClimateData("Assignment 2/climate-daily.csv")