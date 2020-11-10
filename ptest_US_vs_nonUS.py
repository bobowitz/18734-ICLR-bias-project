# ptest_US_vs_non_US.py
#
# Does a permutation test with test statistic defined as
# t = proportion of accepted papers with all US domains - proportion of rejected papers with all US domains

import os
import json
import random
import tqdm

NUM_PERMUTATIONS = 50000  # number of permutations to compute for p-test

accepted_papers_all_us = 0
accepted_papers_total = 0
rejected_papers_all_us = 0
rejected_papers_total = 0

for fname in os.listdir('Data/2020/Accept/'):
    with open('Data/2020/Accept/' + fname, 'r') as f:
        data = json.load(f)
        if data['authorid_domain_countries'] == ['US']:
            accepted_papers_all_us += 1
        accepted_papers_total += 1
for fname in os.listdir('Data/2020/Reject/'):
    with open('Data/2020/Reject/' + fname, 'r') as f:
        data = json.load(f)
        if data['authorid_domain_countries'] == ['US']:
            rejected_papers_all_us += 1
        rejected_papers_total += 1

pct_accept_all_us = accepted_papers_all_us / accepted_papers_total
pct_reject_all_us = rejected_papers_all_us / rejected_papers_total
actual_test_statistic = pct_accept_all_us - pct_reject_all_us
print(
    f'p1 = proportion of accepted papers with only-US email domains: {accepted_papers_all_us}/{accepted_papers_total} = {pct_accept_all_us}')
print(
    f'p2 = proportion of rejected papers with only-US email domains: {rejected_papers_all_us}/{rejected_papers_total} = {pct_reject_all_us}')
print(f'test statistic value = p1 - p2 = {actual_test_statistic}')

all_papers = [1] * (accepted_papers_all_us + rejected_papers_all_us) + [0] * (
    accepted_papers_total - accepted_papers_all_us + rejected_papers_total - rejected_papers_all_us)

all_test_statistics = []

# do the p-test
for i in tqdm.tqdm(range(NUM_PERMUTATIONS)):
    random.shuffle(all_papers)

    perm_us_accept_count = 0
    for j in range(accepted_papers_total):
        perm_us_accept_count += all_papers[j]
    perm_us_reject_count = 0
    for j in range(rejected_papers_total):
        perm_us_reject_count += all_papers[accepted_papers_total + j]

    perm_pct_accept_all_us = perm_us_accept_count / accepted_papers_total
    perm_pct_reject_all_us = perm_us_reject_count / rejected_papers_total
    perm_test_statistic = perm_pct_accept_all_us - perm_pct_reject_all_us

    all_test_statistics.append(perm_test_statistic)

all_test_statistics.sort()

for i in range(len(all_test_statistics)):
    if actual_test_statistic < all_test_statistics[i]:
        print(f'p-value = {1.0 - (i / len(all_test_statistics))}')
        break
