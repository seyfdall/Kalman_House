
import pandas as pd
from matplotlib import pyplot as plt


# read in the data
df = pd.read_csv("../archive/nyc-property-sales.csv", low_memory=False)

# cast the five numeric columns to appropriate types
df["YEAR BUILT"] = pd.to_numeric(df["YEAR BUILT"], errors="coerce")
df["SALE PRICE"] = pd.to_numeric(df["SALE PRICE"], errors="coerce")
df["LAND SQUARE FEET"] = pd.to_numeric(df["LAND SQUARE FEET"], errors="coerce")
df["GROSS SQUARE FEET"] = pd.to_numeric(df["GROSS SQUARE FEET"], errors="coerce")
df["SALE DATE"] = pd.to_datetime(df["SALE DATE"], errors="coerce")

# select single family homes built after 1985 that had nonzero square footage
df = df[df["YEAR BUILT"] >= 1985]
df = df[df["BUILDING CLASS CATEGORY"] == "01 ONE FAMILY DWELLINGS"]
df = df[df["LAND SQUARE FEET"] > 0]
df = df[df["GROSS SQUARE FEET"] > 0]


# drop irrelevant columns
df.drop(columns=["BOROUGH", "TAX CLASS AT PRESENT", "BLOCK", "LOT", "EASE-MENT", "BUILDING CLASS AT PRESENT",
                 " ZIP CODE", "RESIDENTIAL UNITS", "COMMERCIAL UNITS", "TOTAL UNITS", "TAX CLASS AT TIME OF SALE",
                 "BUILDING CLASS AT TIME OF SALE", "APARTMENT NUMBER", "BUILDING CLASS CATEGORY"], inplace=True)
# even though apartment no is part of address, since we are looking at homes it is always blank

# make plots to help choose reasonable cutoff point for minimum sale value
plt.title("All Sale Prices on Log Scale")
plt.hist(df["SALE PRICE"], bins=[0, 1, 10, 100, 1000, 10000, 100_000, 1_000_000, 10_000_000, 100_000_000])
plt.gca().set_xscale("log")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()

plt.title("Sale Prices in [1000, 100000] on Linear Scale")
x = df["SALE PRICE"][df["SALE PRICE"] <= 100000]
plt.hist(x[x >= 1000], bins=21)
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()


# remove low sales
df = df[df["SALE PRICE"] >= 100_000]

# drop duplicate rows and save data
# some sales had duplicate rows with wrong square footage, so we assume no house was sold twice in the same day
df.drop_duplicates(inplace=True, subset=["ADDRESS", "SALE DATE"])


df.to_csv("../archive/nyc-property-sales-cleaned.csv", index=False)

print(f"number of data points: {len(df)}")
