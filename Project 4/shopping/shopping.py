import csv
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def load_data(filename):
    month_mapping = {
        "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
        "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }

    evidence = []
    labels = []

    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ev = [
                int(row["Administrative"]),
                float(row["Administrative_Duration"]),
                int(row["Informational"]),
                float(row["Informational_Duration"]),
                int(row["ProductRelated"]),
                float(row["ProductRelated_Duration"]),
                float(row["BounceRates"]),
                float(row["ExitRates"]),
                float(row["PageValues"]),
                float(row["SpecialDay"]),
                month_mapping[row["Month"]],
                int(row["OperatingSystems"]),
                int(row["Browser"]),
                int(row["Region"]),
                int(row["TrafficType"]),
                1 if row["VisitorType"] == "Returning_Visitor" else 0,
                1 if row["Weekend"] == "TRUE" else 0
            ]
            label = 1 if row["Revenue"] == "TRUE" else 0

            evidence.append(ev)
            labels.append(label)

    return evidence, labels


def train_model(evidence, labels):
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    true_positive = sum(1 for actual, predicted in zip(labels, predictions) if actual == predicted == 1)
    true_negative = sum(1 for actual, predicted in zip(labels, predictions) if actual == predicted == 0)
    total_positive = labels.count(1)
    total_negative = labels.count(0)

    sensitivity = true_positive / total_positive if total_positive else 0
    specificity = true_negative / total_negative if total_negative else 0

    return sensitivity, specificity
