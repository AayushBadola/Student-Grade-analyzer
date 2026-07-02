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
# just like test_2_D[row][col] from our notes

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


########################## WEIGHTED AVERAGE PER STUDENT ##########################

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


########################## AT RISK STUDENTS ##########################

# student is at risk if weighted average < 55
# OR they scored below 40 in any single subject

def find_at_risk(grades, weighted_avg, names, cutoff=55):
    at_risk_list = []

    for i in range(len(names)):
        student_marks = grades[i]    # row i -> all 5 subject marks for student i
        failed = [SUBJECTS[j] for j in range(len(SUBJECTS)) if student_marks[j] < 40]

        if weighted_avg[i] < cutoff or len(failed) > 0:
            at_risk_list.append((names[i], round(weighted_avg[i], 2), failed))

    return at_risk_list


########################## REPORT CARD ##########################

def print_report_card(name, marks_row, rank, total_students):
    w_avg    = float(marks_row @ SUBJECT_WEIGHTS)
    strongest = SUBJECTS[int(np.argmax(marks_row))]
    weakest   = SUBJECTS[int(np.argmin(marks_row))]

    print(f"\n  +{'─'*43}+")
    print(f"  |{'REPORT CARD':^43}|")
    print(f"  +{'─'*43}+")
    print(f"  |  Student    : {name:<27}  |")
    print(f"  |  Rank       : {rank} out of {total_students:<20}  |")
    print(f"  |  Overall    : {w_avg:.1f}  ({score_to_letter(w_avg)}){'':>18}  |")
    print(f"  +{'─'*43}+")
    print(f"  |  {'Subject':<12} {'Marks':>5}  {'Grade':>5}  {'Bar':<10}  |")
    print(f"  |  {'─'*39}  |")

    for j in range(len(SUBJECTS)):
        mark = marks_row[j]
        bar  = '█' * int(mark / 10) + '░' * (10 - int(mark / 10))
        print(f"  |  {SUBJECTS[j]:<12} {mark:>5.0f}  {score_to_letter(mark):>5}  {bar}  |")

    print(f"  +{'─'*43}+")
    print(f"  |  Strongest subject : {strongest:<21}|")
    print(f"  |  Weakest subject   : {weakest:<21}|")
    print(f"  +{'─'*43}+")


########################## MAIN ##########################

print("=" * 50)
print("   Student Grade Analyzer")
print("=" * 50)

############ generate data ############

grades, names = generate_class_data(n_students=20)

############ weighted averages ############

weighted_avg = get_weighted_averages(grades)

############ subject stats ############

sub_stats = get_subject_stats(grades)

print(f"\n── Subject Performance ──")
print(f"  {'Subject':<12} {'Mean':>6} {'Std':>6} {'Min':>5} {'Max':>5}  Grade")
print(f"  {'─'*44}")
for j in range(len(SUBJECTS)):
    print(f"  {SUBJECTS[j]:<12} {sub_stats[0][j]:>6.1f} {sub_stats[1][j]:>6.1f}"
          f" {sub_stats[2][j]:>5.0f} {sub_stats[3][j]:>5.0f}  {score_to_letter(sub_stats[0][j])}")

############ class summary ############

print(f"\n── Class Summary ──")
print(f"  Class average     : {np.mean(weighted_avg):.2f}")
print(f"  Highest score     : {np.max(weighted_avg):.2f}")
print(f"  Lowest score      : {np.min(weighted_avg):.2f}")
print(f"  Pass rate  (>=50) : {np.sum(weighted_avg >= 50) / len(weighted_avg) * 100:.1f}%")
print(f"  Distinction (>=80): {np.sum(weighted_avg >= 80) / len(weighted_avg) * 100:.1f}%")

############ rankings ############

ranked_names, ranked_scores, ranks = rank_students(weighted_avg, names)

print(f"\n── Top 5 Students ──")
print(f"  {'Rank':<5} {'Name':<14} {'Score':>8}  Grade")
print(f"  {'─'*34}")
for i in range(5):
    print(f"  {i+1:<5} {ranked_names[i]:<14} {ranked_scores[i]:>8.2f}  {score_to_letter(ranked_scores[i])}")

print(f"\n── Bottom 3 Students ──")
print(f"  {'Rank':<5} {'Name':<14} {'Score':>8}  Grade")
print(f"  {'─'*34}")
for i in range(-3, 0):
    rank_num = len(names) + i + 1
    print(f"  {rank_num:<5} {ranked_names[i]:<14} {ranked_scores[i]:>8.2f}  {score_to_letter(ranked_scores[i])}")

############ at risk ############

at_risk = find_at_risk(grades, weighted_avg, names, cutoff=55)

print(f"\n── At Risk Students ({len(at_risk)} flagged) ──")
for name, avg, failed in at_risk:
    subjects_str = ', '.join(failed) if failed else "low average"
    print(f"  >> {name:<14}  avg = {avg}   issue : {subjects_str}")

############ report cards ############

print(f"\n── Report Cards ──")

top_index = int(np.argmax(weighted_avg))
print_report_card(names[top_index], grades[top_index], ranks[top_index], len(names))
print_report_card(names[0], grades[0], ranks[0], len(names))

print("\n" + "=" * 50)