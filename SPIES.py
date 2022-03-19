# Author: Rodeo Flagellum
# Desc: Attempted implemenation of SPIES
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

#interval = np.logspace(start=1, stop=6, num=5) # 1-1e6, 5 groups
# [1.00000000e+01 1.77827941e+02 3.16227766e+03 5.62341325e+04
#1.00000000e+06]

def find_smallest_array(probabilities, str_tups, conf):
    prob_tups = dict(list(zip(str_tups, probabilities))) # (0.45, 4-45)
    sub_probs = []
    inter = []
    for index, tup in enumerate(prob_tups.keys()):
        if ('<' in tup) or ('>' in tup):
            sub_probs.append(prob_tups[tup])
            inter.append(tup)
        else:
            #7-5 = 2, but it should be 5,6,7, so 3
            int_length = (int(tup.split('-')[1])-int(tup.split('-')[0]))+1
            interval = prob_tups[tup]/int_length
            sub_probs.extend([interval]*int_length)
            inter.extend([str(elt) for elt in range(int(tup.split('-')[0]), int(tup.split('-')[1])+1)])
    indices = []
    for i1, e1 in enumerate(sub_probs):
        value = e1
        min_index = i1
        max_index = 0
        for i2, e2 in enumerate(sub_probs[i1+1:]):
            value += e2
            if value >= conf:
                max_index = i1+i2+1
                indices.append((min_index, max_index))
                break
    outcome = sorted(indices, key=lambda x: x[1]-x[0]+1)
    return (inter[outcome[0][0]], inter[outcome[0][1]])

# elicit interval
min_val = int(input("Enter minimum value: "))
max_val = int(input("Enter maximum value: "))
step_size = int(input("How many intervals would you like?: "))
interval = list(range(min_val, max_val+1, int(((max_val-min_val)/step_size))))
int_tups = list(zip(interval[:-1], interval[1:]))
int_tups = [(elt[0], elt[1]) for elt in int_tups]
int_tups[1:] = [(elt[0]+1, elt[1]) for elt in int_tups[1:]]
print(int_tups)
str_tups = [str(elt[0])+'-'+str(elt[1]) for elt in int_tups]
open_lower = input("Would like an open lower bound? (y/n): ")
if open_lower == "y":
    str_tups.insert(0, f"<{str_tups[0].split('-')[0]}")
open_upper = input("Would like an open upper bound? (y/n): ")
if open_upper == "y":
    str_tups.insert(len(str_tups), f">{str_tups[-1].split('-')[1]}")
options = ''.join([elt+" ?\n" for elt in str_tups])
print(options)

# setup graph of the probabilities by interval
fig = plt.figure(figsize=(8, 4))
ax = fig.add_subplot()
ax.grid()
ax.set_title('SPIES', color='black', fontsize=16.0)
ax.set_ylabel('Probability', color='black', fontsize=14.0)
ax.set_xlabel('Intervals', color='black', fontsize=14.0)

while True:

    # get the likelihood estimates for each interval
    likelihoods = []
    for op in str_tups:
        ans = int(input(f"Likelihood (0/100) for {op}: "))
        likelihoods.append(ans)

    # normalize the likelihoods as probabilities
    probabilities = [round((100*li)/sum(likelihoods), 2) for li in likelihoods]
    print("You assigned the following probabilities to the intervals:")

    # display the probabilities
    prob_msg = ''.join([elt+f" {probabilities[index]}%\n" for index, elt in enumerate(str_tups)])
    print(prob_msg)

    # graph the probabilities by interval
    ax.bar(str_tups, probabilities, color='black')
    plt.show()

    # ask user for confidence interval
    conf = int(input('\nWhat would you like the confidence interval to be?: '))

    # accrue the probabilities
    out = find_smallest_array(probabilities, str_tups, conf)
    print(f"You are {conf}% confident that the target value will be between {out[0]} and {out[1]}")
