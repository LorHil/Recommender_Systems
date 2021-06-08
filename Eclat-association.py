import csv
import time

def eclat(prefix, items):
        while items:
            i,itids = items.pop()
            isupp = len(itids)
            if isupp >= minsup:
              if len(prefix+[i]) >= 3: #Only print itemsets of minimum 3 elements
                print(sorted(prefix+[i]), ':', isupp)  # Output all frequent pairs
              suffix = [] 
              for j, ojtids in items:
                  jtids = itids & ojtids
                  if len(jtids) >= minsup:
                      suffix.append((j,jtids))
              eclat(prefix+[i], sorted(suffix, key=lambda item: len(item[1]), reverse=True))

if __name__ == '__main__':
    #initialize parameters
    data = {}
    minsup   = 250
    trans = 0
    filename = 'train.csv'
    #start time for program
    timestart = time.time()
    item_def = 2  # column ITEM ID
    transaction_def = 7  # TRANSACTION = USER ID
    #transaction_def = 8  # TRANSACTION = USER SESSION
    


    f = open('train.csv', mode='r')
    for row in f:
        trans = row.split(',')[transaction_def]  
        item =  row.split(',')[item_def] 

        if item is not '':
            if item not in data:
                data[item] = set()
            #if row.split(',')[1] == 'purchase':  # comment if you want all types of transactions - here only put in cart
            data[item].add(trans)   # add does not add an element to the set key if it is already in the set
    f.close()
    eclat([], sorted(data.items(), key=lambda item: len(item[1]), reverse=True))
    timestop = time.time()
    duration = timestop - timestart
    print(duration)
