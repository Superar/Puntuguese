import pandas as pd
from datasets import DatasetDict, concatenate_datasets, load_dataset

ds_original  = load_dataset("Superar/Puntuguese")
ds_controlled = load_dataset("Superar/Puntuguese", "pair_controlled")

assert isinstance(ds_original, DatasetDict)
assert isinstance(ds_controlled, DatasetDict)

all_original = concatenate_datasets([ds_original[key] for key in ds_original])
all_controlled = concatenate_datasets([ds_controlled[key] for key in ds_controlled])
assert set(all_original["id"]) == set(all_controlled["id"])

for split, ds in ds_controlled.items():
    base_ids = pd.Series(ds["id"]).str[:-2]
    assert (base_ids.value_counts() == 2).all()

print("Controlled pairs are good.")
