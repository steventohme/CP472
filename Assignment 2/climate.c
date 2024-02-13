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

void parse_records(char* filename, ClimateRecord* records[], int* record_count) {
    FILE* file = fopen(filename, "r");
    char line[256];

    while (fgets(line, sizeof(line), file)) {
        ClimateRecord* record = parse_line(line);
        records[(*record_count)++] = record;
    }

    fclose(file);
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

