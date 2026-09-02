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
