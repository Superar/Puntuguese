from argparse import ArgumentParser
from pathlib import Path

import json
import sys

parser = ArgumentParser()
parser.add_argument('--input', '-i',
                    help='Input JSON file to be fixed.',
                    required=True, type=Path)
args = parser.parse_args()

with args.input.open(encoding='utf-8') as f:
    data = json.load(f)

cur_ids = dict()
new_data = data.copy()
for (i, pun) in enumerate(data):
    source_id, pun_id = map(int, pun['id'].split('.'))
    if source_id not in cur_ids:
        cur_ids[source_id] = 1
    if pun_id != cur_ids[source_id]:
        print(f'Fixed {pun["id"]} from {pun_id} to {cur_ids[source_id]}.',
                file=sys.stderr)
        new_data[i]['id'] = str(source_id) + '.' + str(cur_ids[source_id])
    cur_ids[source_id] += 1

savepath = args.input.with_stem(args.input.stem + 'fix')
with savepath.open('w', encoding='utf-8') as file_:
    json.dump(new_data, file_,
              ensure_ascii=False,
              indent=4)

