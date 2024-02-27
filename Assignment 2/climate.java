import java.util.*;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.nio.file.*;
import java.io.*;

class ClimateRecord {
    LocalDate date;
    int maxGust;
    float totalPrecipitation;
    float minTemperature;
    float maxTemperature;
    float avgTemperature;

    public ClimateRecord(LocalDate date, int maxGust, float totalPrecipitation, float minTemperature, float maxTemperature, float avgTemperature) {
        this.date = date;
        this.maxGust = maxGust;
        this.totalPrecipitation = totalPrecipitation;
        this.minTemperature = minTemperature;
        this.maxTemperature = maxTemperature;
        this.avgTemperature = avgTemperature;
    }
}

public class climate {
    public static void main(String[] args) {
        ArrayList<ClimateRecord> records = new ArrayList<>();

        loadRecords(records);
        analyzeData(records);

        while (true) {
            System.out.println("1. Monthly report");
            System.out.println("2. Weather records between two dates");
            System.out.println("3. Exit");
            System.out.println("Enter your choice: ");
            Scanner scanner = new Scanner(System.in);
            String choice = scanner.nextLine();
            scanner.close();

            if (choice.equals("1")) {
                long startTime = System.nanoTime();
                monthlyReport(records);
                long endTime = System.nanoTime();
                long duration = (endTime - startTime);  
                double durationInSeconds = (double)duration / 1_000_000_000;
                System.out.println("Monthly report took " + durationInSeconds + " seconds");
            } else if (choice.equals("2")) {
                System.out.println("Enter the start date (YYYY-MM-DD): ");
                String startDate = scanner.nextLine();
                System.out.println("Enter the end date (YYYY-MM-DD): ");
                String endDate = scanner.nextLine();
                dateRangeReport(records, LocalDate.parse(startDate), LocalDate.parse(endDate));
            } else if (choice.equals("3")) {
                break;
            } else {
                System.out.println("Invalid choice. Please try again.");
            }
        }
    }

    public static void loadRecords(ArrayList<ClimateRecord> records) {
        Path pathToFile = Paths.get("climate-daily.csv");

        try (BufferedReader br = Files.newBufferedReader(pathToFile)) {
            String line = br.readLine();
            while ((line = br.readLine()) != null) {
                String[] attributes = line.split(",");
                if (attributes.length < 6) {
                    System.out.println("Skipping line with missing data: " + line);
                    continue;
                } 
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd H:mm");
                LocalDate date = LocalDate.parse(attributes[0], formatter);
                try {
                    int maxGust = Integer.parseInt(attributes[1]);
                    float totalPrecipitation = Float.parseFloat(attributes[2]);
                    float minTemperature = Float.parseFloat(attributes[3]);
                    float maxTemperature = Float.parseFloat(attributes[4]);
                    float avgTemperature = Float.parseFloat(attributes[5]);
                    ClimateRecord record = new ClimateRecord(date, maxGust, totalPrecipitation, minTemperature, maxTemperature, avgTemperature);
                    records.add(record);
                } catch (NumberFormatException nfe) {
                    continue;
                }
                
            }
            } catch (IOException ioe) {
                ioe.printStackTrace();
        }
    }

    public static void analyzeData(ArrayList<ClimateRecord> records) {
        Map<String, Float> precipitationPerMonth = new HashMap<>();
        LocalDate maxGustDay = null;
        int maxGust = 0;
        LocalDate maxTempFluctuationDay = null;
        float maxTempFluctuation = 0;
    
        for (ClimateRecord record : records) {
            String monthKey = record.date.format(DateTimeFormatter.ofPattern("MM-yyyy"));
            precipitationPerMonth.put(monthKey, precipitationPerMonth.getOrDefault(monthKey, 0f) + record.totalPrecipitation);
    
            if (record.maxGust > maxGust) {
                maxGust = record.maxGust;
                maxGustDay = record.date;
            }
    
            float tempFluctuation = record.maxTemperature - record.minTemperature;
            if (tempFluctuation > maxTempFluctuation) {
                maxTempFluctuation = tempFluctuation;
                maxTempFluctuationDay = record.date;
            }
        }
    
        Map.Entry<String, Float> maxEntry = null;
        for (Map.Entry<String, Float> entry : precipitationPerMonth.entrySet()) {
            if (maxEntry == null || entry.getValue().compareTo(maxEntry.getValue()) > 0) {
                maxEntry = entry;
            }
        }
    
        System.out.println("\n--Climate Data Analysis--");
        System.out.println("Month with the most precipitation: " + maxEntry.getKey() + " with " + String.format("%.2f", maxEntry.getValue()) + "mm");
        System.out.println("Day with the highest gust: " + maxGustDay + " with " + maxGust + "km/h");
        System.out.println("Day with the highest temperature fluctuation: " + maxTempFluctuationDay + " with " + String.format("%.2f", maxTempFluctuation) + "°C\n");
    }


    public static void monthlyReport(ArrayList<ClimateRecord> records) {
        Map<String, ClimateRecord> monthlyRecords = new HashMap<>();
        for (ClimateRecord record : records) {
            String monthYear = record.date.getMonth().toString() + "-" + record.date.getYear();
            ClimateRecord monthlyRecord = monthlyRecords.getOrDefault(monthYear, new ClimateRecord(record.date, 0, 0, Float.MAX_VALUE, Float.MIN_VALUE, 0));
            if (monthlyRecord.maxGust < record.maxGust) {
                monthlyRecord.maxGust = record.maxGust;
            }
            monthlyRecord.totalPrecipitation += record.totalPrecipitation;
            monthlyRecord.minTemperature = Math.min(monthlyRecord.minTemperature, record.minTemperature);
            monthlyRecord.maxTemperature = Math.max(monthlyRecord.maxTemperature, record.maxTemperature);
            monthlyRecord.avgTemperature += record.avgTemperature;
            monthlyRecords.put(monthYear, monthlyRecord);
        }
    
        for (Map.Entry<String, ClimateRecord> entry : monthlyRecords.entrySet()) {
            ClimateRecord record = entry.getValue();
            System.out.println("Month-Year: " + entry.getKey());
            System.out.println("Max Gust: " + record.maxGust);
            System.out.println("Total Precipitation: " + record.totalPrecipitation);
            System.out.println("Min Temperature: " + record.minTemperature);
            System.out.println("Max Temperature: " + record.maxTemperature);
            System.out.println("Avg Temperature: " + record.avgTemperature / records.size());
        }
    }

    public static void dateRangeReport(ArrayList<ClimateRecord> records, LocalDate startDate, LocalDate endDate) {
        for (ClimateRecord record : records) {
            if (record.date.isAfter(startDate) && record.date.isBefore(endDate)) {
                System.out.println("Date: " + record.date);
                System.out.println("Max Gust: " + record.maxGust);
                System.out.println("Total Precipitation: " + record.totalPrecipitation);
                System.out.println("Min Temperature: " + record.minTemperature);
                System.out.println("Max Temperature: " + record.maxTemperature);
                System.out.println("Avg Temperature: " + record.avgTemperature);
            }
        }
    }
}
