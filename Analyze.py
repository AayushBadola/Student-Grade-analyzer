import numpy as np
import random

SUBJECTS = ["Math", "Physics", "Chemistry", "English", "CS"]

# weight of each subject , all add up to 1.0
# 1D array shape (5,)
SUBJECT_WEIGHTS = np.array([0.25, 0.20, 0.20, 0.15, 0.20])

NAMES = [
    "Aayush", "Riya",   "Aryan",  "Priya",    "Karan",
    "Sneha",  "Rohan",  "Meera",  "Vikram",   "Ananya",
    "Dev",    "Nisha",  "Rahul",  "Pooja",    "Siddharth",
    "Kavya",  "Ishan",  "Tanya",  "Mohit",    "Shreya",
]


########################## GENERATING STUDENT DATA ##########################

# we directly generate random marks for every student in every subject
# np.random.randint(30, 101, size=(20, 5)) creates a 2D array
# 20 rows = 20 students , 5 columns = 5 subjects
# grades[i][j] = student i's mark in subject j
# just like test_2_D[row][col] from our notes, refer my repo "My_python_Journey/NUMPY/multidimension_array"

def generate_class_data(n_students=20):
    grades = np.random.randint(30, 101, size=(n_students, len(SUBJECTS)))
    names  = random.sample(NAMES, n_students)

    print(f"grades shape : {grades.shape}")     # should be (20, 5)
    print(f"grades[0]    : {grades[0]}")        # first student's marks in all 5 subjects
    print(f"grades[0][2] : {grades[0][2]}")     # first student's Chemistry mark

    return grades.astype(float), names


########################## SCORE TO LETTER GRADE ##########################

def score_to_letter(score):
    if   score >= 90 : return "A+"
    elif score >= 80 : return "A "
    elif score >= 70 : return "B "
    elif score >= 60 : return "C "
    elif score >= 50 : return "D "
    else             : return "F "
