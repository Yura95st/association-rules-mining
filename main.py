import csv
import operator
from apriori import Apriori


def get_transactions_from_file(filename):
    result = []

    with open(filename, 'r') as csvfile:
        lines = csv.reader([line for line in csvfile if line.strip()])

        for line in lines:
            result.append({item for item in line})

    return result


def main(filename='data/data.txt', min_support=4, min_confidence=0):
    transactions = get_transactions_from_file(filename)

    apriori = Apriori(transactions, min_support, min_confidence)

    elements, rules = apriori.perform()

    print('Elements:')
    for elem in sorted(elements):
        for item in sorted([sorted(item) for item in elem]):
            print(item)
        print()

    print('Rules:')
    rules = sorted(rules, key=lambda x: list(x[0]))
    rules = sorted(rules, key=lambda x: len(x[0]))

    for head, tail in rules:
        print('{} -> {}'.format(sorted(head), sorted(tail)))


if __name__ == '__main__':
    main()
