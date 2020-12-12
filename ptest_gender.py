# ptest_US_vs_non_US.py
#
# Does a permutation test with test statistic defined as
# t = proportion of accepted papers with all US domains - proportion of rejected papers with all US domains

import os
import json
import random
import tqdm

NUM_PERMUTATIONS = 100000  # number of permutations to compute for p-test

male_papers_accepted = 200
male_papers_total = 589
female_papers_accepted = 17
female_papers_total = 58

pct_male_accept = male_papers_accepted / male_papers_total
pct_female_accept = female_papers_accepted / female_papers_total
actual_test_statistic = pct_male_accept - pct_female_accept
print(
    f'p1 = proportion of male-authored papers accepted: {male_papers_accepted}/{male_papers_total} = {pct_male_accept}')
print(
    f'p2 = proportion of female-authored papers accepted: {female_papers_accepted}/{female_papers_total} = {pct_female_accept}')
print(f'test statistic value = p1 - p2 = {actual_test_statistic}')

# [1] * total accepted + [0] * total rejected
all_papers = [1] * (male_papers_accepted + female_papers_accepted) + [0] * (
    male_papers_total - male_papers_accepted + female_papers_total - female_papers_accepted)

all_test_statistics = []

# do the p-test
for i in tqdm.tqdm(range(NUM_PERMUTATIONS)):
    random.shuffle(all_papers)

    perm_male_accept_count = 0
    for j in range(male_papers_total):
        perm_male_accept_count += all_papers[j]
    perm_female_accept_count = 0
    for j in range(female_papers_total):
        perm_female_accept_count += all_papers[male_papers_total + j]

    perm_pct_male_accept = perm_male_accept_count / male_papers_total
    perm_pct_female_accept = perm_female_accept_count / female_papers_total
    perm_test_statistic = perm_pct_male_accept - perm_pct_female_accept

    all_test_statistics.append(perm_test_statistic)

all_test_statistics.sort()

f = open('ptest_gender_distribution', 'w')

for i in range(len(all_test_statistics)):
    f.write(str(all_test_statistics[i]) + '\n')

for i in range(len(all_test_statistics)):
    if actual_test_statistic <= all_test_statistics[i]:
        print(f'p-value = {1.0 - (i / len(all_test_statistics))}')
        break
