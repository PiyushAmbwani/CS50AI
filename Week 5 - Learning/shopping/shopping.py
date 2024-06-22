import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Import python standard library "Calendar" to create a dict for the moth index.
    # import calendar
    # month_dict= {month : index for index, month in enumerate(calendar.month_abbr) if month}
    
    month_dict = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11
    }
    # print(month_dict)
    # with open(rb'C:\PycharmProjects\edx_pythonAI\project6_shopping\shopping\shopping.csv') as fin:
    evidence = []
    labels = []
    with open(filename) as fin:
        lines = csv.reader(fin)
        next(lines)

        for line in lines:
            evidence.append([int(month_dict[cell]) if cell in month_dict.keys() else float(cell) if idx in (1, 3, 5, 6, 7, 8, 9) else 1 if (idx == 15 and cell == "Returning_Visitor") else 0 if (
                idx == 15 and cell != "Returning_Visitor") else 1 if idx == 16 and cell == 'TRUE' else 0 if (idx == 16 and cell == 'FALSE') else int(cell) for idx, cell in enumerate(line[:16])])
            labels.append(1 if line[17] == 'TRUE' else 0)

    # print(f'{evidence} and {labels}')
    return (evidence, labels)
    # raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    m = KNeighborsClassifier(n_neighbors=1)
    m.fit(evidence, labels)

    return m
    # raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive_cntr = 0
    negative_cntr = 0
    for label, prediction in zip(labels, predictions):
        if label == prediction:
            if label == 1:
                positive_cntr += 1
            else:
                negative_cntr += 1
        
    sensitivity = positive_cntr / labels.count(1)
    specificity = negative_cntr / labels.count(0)

    return (sensitivity, specificity)
    # raise NotImplementedError


if __name__ == "__main__":
    main()
