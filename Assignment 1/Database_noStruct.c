#include <stdio.h>

#define MAX_STUDENTS 100

// Declare arrays to hold student information
// This will act as our database
int student_ids[MAX_STUDENTS];
char student_names[MAX_STUDENTS][75];
int student_ages[MAX_STUDENTS][5];
int student_count = 0;

void add_student(int id, char name[], int age[]) {
    // Check if database is full
    if (student_count >= MAX_STUDENTS) {
        printf("Database is full\n");
        return;
    }
    // Add student to database
    student_ids[student_count] = id;
    strcpy(student_names[student_count], name);
    for (int i = 0; i < 5; i++) {
        student_ages[student_count][i] = age[i];
    }
    student_count++;
}

void display_student_by_id(int id){
    // Find student in database
    for (int i = 0; i < student_count; i++){
        if (student_ids[i] == id){
            printf("ID: %d, Name: %s, Age: %d\n", student_ids[i], student_names[i], student_ages[i]);
            return;
        }
    }
    printf("Student not found\n");
}