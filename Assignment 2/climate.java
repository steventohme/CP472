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
                    System.out.println("Skipping line with invalid data: " + line);
                    continue;
                }
                
            }
            } catch (IOException ioe) {
                ioe.printStackTrace();
        }

        while (true) {
            System.out.println("1. Monthly report");
            System.out.println("2. Weather records between two dates");
            System.out.println("3. Exit");
            System.out.println("Enter your choice: ");
            Scanner scanner = new Scanner(System.in);
            String choice = scanner.nextLine();
            scanner.close();

            if (choice.equals("1")) {
                monthlyReport(records);
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



    public static void monthlyReport(ArrayList<ClimateRecord> records) {
        Map<String, ClimateRecord> monthlyRecords = new HashMap<>();
        for (ClimateRecord record : records) {
            String month = record.date.getMonth().toString() + " " + record.date.getYear();
            ClimateRecord monthlyRecord = monthlyRecords.getOrDefault(month, new ClimateRecord(record.date, 0, 0, Float.MAX_VALUE, Float.MIN_VALUE, 0));
            monthlyRecord.maxGust += record.maxGust;
            monthlyRecord.totalPrecipitation += record.totalPrecipitation;
            monthlyRecord.minTemperature = Math.min(monthlyRecord.minTemperature, record.minTemperature);
            monthlyRecord.maxTemperature = Math.max(monthlyRecord.maxTemperature, record.maxTemperature);
            monthlyRecord.avgTemperature += record.avgTemperature;
            monthlyRecords.put(month, monthlyRecord);
        }

        for (Map.Entry<String, ClimateRecord> entry : monthlyRecords.entrySet()) {
            ClimateRecord record = entry.getValue();
            System.out.println("Month: " + entry.getKey());
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
