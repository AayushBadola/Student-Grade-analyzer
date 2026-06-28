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

######################### WEIGHTED AVERAGE PER STUDENT ##########################

# grades is (20, 5) and SUBJECT_WEIGHTS is (5,)
# grades @ SUBJECT_WEIGHTS -> (20, 5) . (5,) = (20,)
# one weighted score per student

def get_weighted_averages(grades):
    weighted = grades @ SUBJECT_WEIGHTS
    print(f"\nweighted averages shape : {weighted.shape}")   # (20,)
    print(f"first 3 averages        : {weighted[:3].round(2)}")
    return weighted


########################## SUBJECT STATISTICS ##########################

# axis=0 collapses across students (rows) and gives one value per subject (column)
# result shape is (5,) -> one number per subject

def get_subject_stats(grades):
    mean_per_subject = np.mean(grades, axis=0)   # shape (5,)
    std_per_subject  = np.std(grades,  axis=0)
    min_per_subject  = np.min(grades,  axis=0)
    max_per_subject  = np.max(grades,  axis=0)

    # stacking into 2D array shape (4, 5)
    # row 0 = means , row 1 = stds , row 2 = mins , row 3 = maxs
    stats = np.array([mean_per_subject, std_per_subject,
                      min_per_subject,  max_per_subject])

    print(f"\nsubject stats shape  : {stats.shape}")         # (4, 5)
    print(f"mean per subject     : {stats[0].round(1)}")    # row 0
    return stats

########################## RANKING ##########################

# np.argsort gives indices that would sort the array in ascending order
# [::-1] reverses it to get descending (highest first)

def rank_students(weighted_avg, names):
    sorted_indices = np.argsort(weighted_avg)[::-1]

    ranked_names  = [names[i] for i in sorted_indices]
    ranked_scores = [weighted_avg[i] for i in sorted_indices]

    # ranks[i] = rank number of student i in original order
    ranks = np.zeros(len(names), dtype=int)
    for rank_number, original_index in enumerate(sorted_indices):
        ranks[original_index] = rank_number + 1

    return ranked_names, ranked_scores, ranks


