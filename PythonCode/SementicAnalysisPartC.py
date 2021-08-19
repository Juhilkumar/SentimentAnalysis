import csv

with open("./WordSementicAnalysis-b/semanticAnalysisB.csv", 'rU') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header row
    answer = max(reader, key=lambda column: int(column[2]))

highestRelativeFrequency = (int(answer[2]) / int(answer[1]))
print("Article with highest relative frequency : " + answer[0])
print("Total Words (m): " + answer[1])
print("Frequency (f): " + answer[2])
print("Relative frequency : " + str(highestRelativeFrequency))
