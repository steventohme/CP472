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

