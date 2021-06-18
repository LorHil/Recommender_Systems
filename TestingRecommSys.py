import csv
import time
import random


def eclat(prefix, items, rules=[]):
    while items:
        i, itids = items.pop()
        isupp = len(itids)
        if isupp >= minsup:
            if len(prefix + [i]) >= 2:  # Only add itemsets of minimum 2 elements
                # print(sorted(prefix+[i]), ':', isupp)
                rules.append(sorted(prefix + [i]))  # storage of the learned rules
            suffix = []
            for j, ojtids in items:
                jtids = itids & ojtids
                if len(jtids) >= minsup:
                    suffix.append((j, jtids))
            eclat(prefix + [i], sorted(suffix, key=lambda item: len(item[1]), reverse=True))
    return rules


if __name__ == '__main__':
    # initialize parameters
    data = {}
    minsup = 120
    trans = 0
    filename = 'train.csv'
    # start time for program
    timestart = time.time()
    item_def = 2  # column ITEM ID
    # transaction_def = 7  # TRANSACTION = USER ID
    transaction_def = 8  # TRANSACTION = USER SESSION

    f = open('train.csv', mode='r')
    for row in f:
        trans = row.split(',')[transaction_def].strip()
        item = row.split(',')[item_def]

        if item is not '':
            if item not in data:
                data[item] = set()
            # if row.split(',')[1] == 'purchase':  # comment if you want all types of transactions - here only put in cart
            data[item].add(trans)  # add does not add an element to the set key if it is already in the set
    f.close()
    rules = eclat([], sorted(data.items(), key=lambda item: len(item[1]), reverse=True))
    timestop = time.time()
    duration = timestop - timestart
    print(duration)

    ######################## TEST THE TEST DATASET ################################
    f = open('test.csv', mode='r')
    # pre-processing
    data = {}
    for row in f:
        trans = row.split(',')[transaction_def].strip()
        item = row.split(',')[item_def]

        if trans != 'user_session':
            if trans not in data:
                data[trans] = [item]
            data[trans].append(item)
    f.close()

    recommend = {}
    for i in range(1, len(data)):
        candidates = []
        maximum = 0
        for j in range(0, len(rules)):
            items = list(data.values())[i]
            comparisonset = set(rules[j]) & set(items)
            if len(comparisonset) == (len(rules[j])-1):
                # list of all items in that transaction -> which is the missing?
                if len(rules[j]) > maximum:
                    candidates = list(comparisonset)
                    maximum = len(rules[j])
                elif len(rules[j]) == maximum:
                    candidates.append(list(set(rules[j]) - comparisonset)) 

        if not candidates:
            candidates.append(random.choice(sum(rules, [])))  # if no association was found, pick a random recommended item
        candidate = random.choice(candidates)[0]
        #print(candidate) ########### candidate is een lijst! klopt niet!

        transaction = list(data.keys())[i]
        if transaction not in recommend:
            recommend[transaction] = set()
        recommend[transaction].add(candidate)
    # print(recommend)
    # print(list(recommend.keys()))

    #################### PERFORMANCE ###################################
    f = open('test_gt.csv', mode='r')
    correctRec = {}
    for row in f:
        split = row.split(',')
        correctRec[split[0]] = split[1].strip()

    f.close()

    right = 0
    wrong = 0
    for i in range(0, len(recommend)):
        transaction = list(recommend.keys())[i]
        if list(recommend.values())[i] == int(correctRec[transaction]):
            right += 1
        else:
            wrong += 1
    print(right)
    print(wrong)