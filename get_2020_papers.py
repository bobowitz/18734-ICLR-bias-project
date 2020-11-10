# get_2020_papers.py
#
# Uses the openreview API to fetch the 2020 ICLR accept/reject dataset

import openreview
import json
import os

from tqdm import tqdm

client = openreview.Client(baseurl='https://api.openreview.net')
decision_iterator = openreview.tools.iterget_notes(
    client,
    invitation='ICLR.cc/2020/Conference/Paper.*/-/Decision'
)

print("downloading papers...")

id_to_submission = {note.id: note for note in openreview.tools.iterget_notes(
    client, invitation='ICLR.cc/2020/Conference/-/Blind_Submission')}

for decision in tqdm(decision_iterator):
    note_id = decision.id
    paper_id = decision.forum
    paper = id_to_submission[paper_id]

    if 'Accept' in decision.content['decision']:
        os.makedirs(f'Data/2020/Accept/', exist_ok=True)
        with open(f'Data/2020/Accept/{paper_id}.json', 'w') as f:
            json.dump(paper.content, f, indent=2)
    else:
        os.makedirs(f'Data/2020/Reject/', exist_ok=True)
        with open(f'Data/2020/Reject/{paper_id}.json', 'w') as f:
            json.dump(paper.content, f, indent=2)

print("done.")
