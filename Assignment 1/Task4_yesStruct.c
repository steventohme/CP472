#include <stdio.h>
#include <string.h>

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

void display_student_by_id(int id){
    // Find student in database
    for (int i = 0; i < student_count; i++){
        if (students[i].id == id){
            printf("ID: %d, Name: %s, Age: %d\n", students[i].id, students[i].name, students[i].age);
            return;
        }
    }
    printf("Student not found\n");
}

void display_all_students(){
    for (int i = 0; i < student_count; i++){
        printf("ID: %d, Name: %s, Age: %d\n", students[i].id, students[i].name, students[i].age);
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