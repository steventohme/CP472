#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char date[11];
    int maxGust;
    float totalPrecipitation;
    float minTemperature;
    float maxTemperature;
} ClimateRecord;

ClimateRecord* parse_line(char* line) {
    ClimateRecord* record = malloc(sizeof(ClimateRecord));
    char* token = strtok(line, ",");
    strcpy(record->date, token);
    token = strtok(NULL, ",");
    record->maxGust = atoi(token);
    token = strtok(NULL, ",");
    record->totalPrecipitation = atof(token);
    token = strtok(NULL, ",");
    record->minTemperature = atof(token);
    token = strtok(NULL, ",");
    record->maxTemperature = atof(token);
    return record;
}


void analyzeData(ClimateRecord* records[], int record_count) {
    char* maxPrecipitationDate = NULL;
    float maxPrecipitation = 0;
    char* maxGustDate = NULL;
    int maxGust = 0;
    char* maxTempFluctuationDate = NULL;
    float maxTempFluctuation = 0;

    for (int i = 0; i < record_count; i++) {
        ClimateRecord* record = records[i];

        if (record->totalPrecipitation > maxPrecipitation) {
            maxPrecipitation = record->totalPrecipitation;
            maxPrecipitationDate = record->date;
        }

        if (record->maxGust > maxGust) {
            maxGust = record->maxGust;
            maxGustDate = record->date;
        }

        float tempFluctuation = record->maxTemperature - record->minTemperature;
        if (tempFluctuation > maxTempFluctuation) {
            maxTempFluctuation = tempFluctuation;
            maxTempFluctuationDate = record->date;
        }
    }

    printf("\n--Climate Data Analysis--\n");
    printf("Day with the most precipitation: %s with %.2fmm\n", maxPrecipitationDate, maxPrecipitation);
    printf("Day with the highest gust: %s with %dkm/h\n", maxGustDate, maxGust);
    printf("Day with the highest temperature fluctuation: %s with %.2f°C\n", maxTempFluctuationDate, maxTempFluctuation);
}

int main() {
    int record_count = 0;
    int record_capacity = 100;

    // Allocate initial memory
    ClimateRecord** records = malloc(record_capacity * sizeof(ClimateRecord*));

    FILE* file = fopen("climate.csv", "r");
    char line[256];

    while (fgets(line, sizeof(line), file)) {
        // Resize the array if needed
        if (record_count == record_capacity) {
            record_capacity *= 2;
            records = realloc(records, record_capacity * sizeof(ClimateRecord*));
        }

        ClimateRecord* record = parse_line(line);
        records[record_count++] = record;
    }

    fclose(file);

    analyzeData(records, record_count);

    for (int i = 0; i < record_count; i++) {
        free(records[i]);
    }

    return 0;
}

void userGeneratedReport(ClimateRecord** records, int record_count) {
    int choice;
    do {
        printf("1. Monthly report\n");
        printf("2. Weather records between two dates\n");
        printf("3. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                monthly_report(records, record_count);
                break;
            case 2:
                char start_date[11], end_date[11];
                printf("Enter the start date (YYYY-MM-DD): ");
                scanf("%s", start_date);
                printf("Enter the end date (YYYY-MM-DD): ");
                scanf("%s", end_date);
                date_range_report(records, record_count, start_date, end_date);
                break;
            case 3:
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 3);
}