import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("../data/expedia_sample.csv")

# Date conversion
df["srch_ci"] = pd.to_datetime(df["srch_ci"])
df["srch_co"] = pd.to_datetime(df["srch_co"])

# Feature Engineering
df["stay_length"] = (
    df["srch_co"] - df["srch_ci"]
).dt.days

# ------------------------------------
# Booking Rate
# ------------------------------------

booking_rate = (
    df.groupby("is_mobile")["is_booking"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(6,4))

sns.barplot(
    data=booking_rate,
    x="is_mobile",
    y="is_booking"
)

plt.xticks([0,1], ["Desktop","Mobile"])
plt.title("Booking Rate by Device Type")

plt.savefig("../visuals/booking_rate.png")
plt.close()

# ------------------------------------
# Distance Boxplot
# ------------------------------------

plt.figure(figsize=(8,5))

sns.boxplot(
    data=df,
    x="is_mobile",
    y="orig_destination_distance"
)

plt.xticks([0,1], ["Desktop","Mobile"])
plt.title("Travel Distance by Device Type")

plt.savefig("../visuals/distance_boxplot.png")
plt.close()

# ------------------------------------
# Stay Length Boxplot
# ------------------------------------

plt.figure(figsize=(8,5))

sns.boxplot(
    data=df,
    x="is_mobile",
    y="stay_length"
)

plt.xticks([0,1], ["Desktop","Mobile"])
plt.title("Stay Length by Device Type")

plt.savefig("../visuals/stay_length_boxplot.png")
plt.close()

# ------------------------------------
# Histogram
# ------------------------------------

plt.figure(figsize=(8,5))

sns.histplot(
    data=df,
    x="stay_length",
    hue="is_mobile",
    bins=20,
    kde=True
)

plt.title("Stay Length Distribution")

plt.savefig("../visuals/stay_distribution.png")
plt.close()

print("Analysis completed.")
