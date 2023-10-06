# pipenv run python experiments/editing_statistics.py -e data/split_annotation/
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

parser = ArgumentParser()
parser.add_argument('--editions', '-e',
                    help='Directory with edited puns JSON files.',
                    required=True, type=Path)
args = parser.parse_args()


editions = dict()
for filepath in args.editions.iterdir():
    edited = pd.read_json(filepath)
    editions[filepath.stem] = edited
df = pd.concat(editions)

edited_df = df.query('tokens != `edited tokens`').copy()
edited_df['editions'] = edited_df.apply(lambda x: [(i, j)
                                                   for i, j in zip(x['tokens'], x['edited tokens'])
                                                   if i != j],
                                        axis='columns')
edited_df['deletions'] = edited_df.apply(lambda x: [(i, j)
                                                    for i, j in x['editions']
                                                    if not j],
                                         axis='columns')
edited_df['num_editions'] = edited_df['editions'].str.len()
edited_df['num_deletions'] = edited_df['deletions'].str.len()

total = len(df)
edited = len(edited_df)
avg_edited_tokens = edited_df['num_editions'].mean()
median_edited_tokens = edited_df['num_editions'].median()
max_edited_tokens = edited_df['num_editions'].max()

with_deletion = edited_df.query('num_deletions > 0')
avg_deleted_tokens = with_deletion['num_deletions'].mean()
median_deleted_tokens = with_deletion['num_deletions'].median()
max_deleted_tokens = with_deletion['num_deletions'].max()

print(f'Puns in the corpus: {total}')
print(f'Edited puns: {edited}')
print(f'Average number of editions: {avg_edited_tokens:.4f}')
print(f'Median number of editions: {median_edited_tokens}')
print(f'Max number of editions: {max_edited_tokens}')
print(f'Puns with deletion: {len(with_deletion)}')
print(f'Average number of deletions: {avg_deleted_tokens:.4f}')
print(f'Median number of deletions: {median_deleted_tokens}')
print(f'Max number of deletions: {max_deleted_tokens}')
