import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Example data
criteria = ['Criterion A', 'Criterion B', 'Criterion C', 'Criterion A', 'Criterion B', 'Criterion C','Criterion A','Criterion A','Criterion A','Criterion A']
grades = [1, 2, 3, 2, 4, 1,1,1,2]

# Construct a frequency matrix
unique_criteria = sorted(set(criteria))
grade_scale = [1, 2, 3, 4]
frequency_matrix = np.zeros((len(unique_criteria), len(grade_scale)))

for criterion, grade in zip(criteria, grades):
    row = unique_criteria.index(criterion)
    col = grade_scale.index(grade)
    frequency_matrix[row, col] += 1

# Create the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(frequency_matrix, annot=True, fmt=".0f", cmap="Reds", xticklabels=grade_scale, yticklabels=unique_criteria)
plt.xlabel('Grades')
plt.ylabel('Evaluation Criteria')
plt.title('Grade Distribution by Evaluation Criteria')
plt.show()