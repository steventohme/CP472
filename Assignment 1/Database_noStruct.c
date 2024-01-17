#include <stdio.h>
#include <string.h>

#define MAX_STUDENTS 100

// Declare arrays to hold student information
// This will act as our database
int student_ids[MAX_STUDENTS];
char student_names[MAX_STUDENTS][75];
int student_ages[MAX_STUDENTS];
int student_count = 0;

void add_student(int id, char name[], int age) {
    // Check if database is full
    if (student_count >= MAX_STUDENTS) {
        printf("Database is full\n");
        return;
    }
    // Add student to database
    student_ids[student_count] = id;
    strcpy(student_names[student_count], name);
    student_ages[student_count] = age;
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

void display_all_students(){
    for (int i = 0; i < student_count; i++){
        printf("ID: %d, Name: %s, Age: %d\n", student_ids[i], student_names[i], student_ages[i]);
    }
}

int main(){
    // Add students to database
    add_student(1, "John", 20);
    add_student(2, "Jane", 21);
    add_student(3, "Jack", 22);
    add_student(4, "Jill", 23);

    // Display student that exists
    display_student_by_id(1);
    // Display student that does not exist
    display_student_by_id(5);

    // Display all students
    display_all_students();
}