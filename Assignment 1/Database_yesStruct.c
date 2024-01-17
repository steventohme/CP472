#include <stdio.h>

#define MAX_STUDENTS 100

// Declare struct to hold student information
typedef struct {
    int id;
    char name[75];
    int age;
} Student;

// Declare array of structs to hold student information
// This will act as our database

Student students[MAX_STUDENTS];
int student_count = 0;

void add_student(int id, char name[], int age){
    students[student_count].id = id;
    strcpy(students[student_count].name, name);
    students[student_count].age = age; 
    student_count++;
}