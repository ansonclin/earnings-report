"""
For each earnings event, guess its reaction size using that same ticker's
own history - no real model, no features.

pct_reaction was already calculated back in dataset_builder.py, for every
row. This file doesn't recompute anything - it just reads that column.

How the guess is made: filter dataset down to that ticker's other rows
with an earlier earnings_date, take just their pct_reaction column, and
average it (abs value, since only size matters, not direction). That
average is the guess.

Then check how wrong each guess was against the real pct_reaction for that
row, and average all those errors into one MAE score - the number a real
model has to beat later.
"""

import pandas as pd
from dataset_builder import dataset

avg_error_calc = []
# rows aren't in date order, but that's fine - the filter below checks dates, not position
for i, row in dataset.iterrows():
    # i = row number (unused). row = current row's full data.
    ticker = row["ticker"]
    earnings_date = row["earnings_date"]
    actual = abs(row["pct_reaction"])

    # rows with same ticker AND an earlier date
    earlier = dataset[(dataset["ticker"] == ticker) & (dataset["earnings_date"] < earnings_date)]

    if earlier.empty:
        continue

    avg_past_reaction = earlier["pct_reaction"].abs().mean()  # how much the ticker has moved after past earnings report using the avg. of percent change (pct_reaction)
    error = abs(actual - avg_past_reaction)  # how far off that guess was from what really happened
    avg_error_calc.append(error)

mae = pd.Series(avg_error_calc).mean()  # avg of all those errors = Mean Absolute Error
print("Naive baseline MAE:", mae)
