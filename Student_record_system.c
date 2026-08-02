#include <stdio.h>
#include <string.h>

#define MAX_STUDENTS 100

struct Student {
    int id;
    char name[50];
    int age;
    float marks;
};

struct Student students[MAX_STUDENTS];
int count = 0;

// Function to add a student
void addStudent() {
    if (count >= MAX_STUDENTS) {
        printf("\nDatabase is full!\n");
        return;
    }

    printf("\nEnter Student ID: ");
    scanf("%d", &students[count].id);

    printf("Enter Student Name: ");
    scanf(" %[^\n]", students[count].name);

    printf("Enter Age: ");
    scanf("%d", &students[count].age);

    printf("Enter Marks: ");
    scanf("%f", &students[count].marks);

    count++;

    printf("\nStudent added successfully!\n");
}

// Function to display all students
void displayStudents() {
    if (count == 0) {
        printf("\nNo student records found.\n");
        return;
    }

    printf("\n-------------------------------------------------------------\n");
    printf("ID\tName\t\tAge\tMarks\n");
    printf("-------------------------------------------------------------\n");

    for (int i = 0; i < count; i++) {
        printf("%d\t%-15s\t%d\t%.2f\n",
               students[i].id,
               students[i].name,
               students[i].age,
               students[i].marks);
    }
}

// Function to search student
void searchStudent() {
    int id;
    printf("\nEnter Student ID: ");
    scanf("%d", &id);

    for (int i = 0; i < count; i++) {
        if (students[i].id == id) {
            printf("\nStudent Found\n");
            printf("ID    : %d\n", students[i].id);
            printf("Name  : %s\n", students[i].name);
            printf("Age   : %d\n", students[i].age);
            printf("Marks : %.2f\n", students[i].marks);
            return;
        }
    }

    printf("\nStudent not found!\n");
}

// Function to update student marks
void updateMarks() {
    int id;

    printf("\nEnter Student ID: ");
    scanf("%d", &id);

    for (int i = 0; i < count; i++) {
        if (students[i].id == id) {
            printf("Enter New Marks: ");
            scanf("%f", &students[i].marks);

            printf("\nMarks updated successfully!\n");
            return;
        }
    }

    printf("\nStudent not found!\n");
}

// Function to delete student
void deleteStudent() {
    int id;

    printf("\nEnter Student ID to delete: ");
    scanf("%d", &id);

    for (int i = 0; i < count; i++) {
        if (students[i].id == id) {

            for (int j = i; j < count - 1; j++) {
                students[j] = students[j + 1];
            }

            count--;

            printf("\nStudent deleted successfully!\n");
            return;
        }
    }

    printf("\nStudent not found!\n");
}

// Function to calculate average marks
void averageMarks() {

    if (count == 0) {
        printf("\nNo records available.\n");
        return;
    }

    float total = 0;

    for (int i = 0; i < count; i++) {
        total += students[i].marks;
    }

    printf("\nAverage Marks = %.2f\n", total / count);
}

// Main Function
int main() {

    int choice;

    while (1) {

        printf("\n=================================\n");
        printf(" STUDENT MANAGEMENT SYSTEM\n");
        printf("=================================\n");
        printf("1. Add Student\n");
        printf("2. Display Students\n");
        printf("3. Search Student\n");
        printf("4. Update Marks\n");
        printf("5. Delete Student\n");
        printf("6. Average Marks\n");
        printf("7. Exit\n");

        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {

            case 1:
                addStudent();
                break;

            case 2:
                displayStudents();
                break;

            case 3:
                searchStudent();
                break;

            case 4:
                updateMarks();
                break;

            case 5:
                deleteStudent();
                break;

            case 6:
                averageMarks();
                break;

            case 7:
                printf("\nExiting program...\n");
                return 0;

            default:
                printf("\nInvalid choice! Please try again.\n");
        }
    }

    return 0;
}
