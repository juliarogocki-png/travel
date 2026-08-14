import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Setup
os.makedirs("visuals", exist_ok=True)
df = pd.read_csv("data/travel.csv")

# Portfolio colors
BG = "#f7f6f2"
TEXT = "#1f1d17"
MUTED = "#6f6b63"
LINE = "#ddd8cf"
ACCENT = "#d98fa1"
ACCENT_DARK = "#b96f84"
ACCENT_SOFT = "#f6e1e7"


def style(ax):
    ax.set_facecolor(BG)
    ax.grid(axis="y", color=LINE, linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

    ax.spines["bottom"].set_color(LINE)
    ax.tick_params(colors=MUTED, length=0, pad=8)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(
        f"visuals/{name}",
        dpi=300,
        bbox_inches="tight",
        facecolor=BG
    )
    plt.show()
    plt.close(fig)


# ------------------------------------------------------------
# Data preparation
# ------------------------------------------------------------

df["srch_ci"] = pd.to_datetime(df["srch_ci"], errors="coerce")
df["srch_co"] = pd.to_datetime(df["srch_co"], errors="coerce")

df["stay_length"] = (
    df["srch_co"] - df["srch_ci"]
).dt.days


# ============================================================
# 1. BOOKING RATE
# ============================================================

booking = (
    df.groupby("is_mobile")["is_booking"]
    .mean()
    .reset_index()
)

booking["device"] = booking["is_mobile"].map({
    0: "Desktop",
    1: "Mobile"
})

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor(BG)

bars = ax.bar(
    booking["device"],
    booking["is_booking"],
    width=0.55,
    color=ACCENT
)

for bar, value in zip(bars, booking["is_booking"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.002,
        f"{value:.1%}",
        ha="center",
        color=TEXT,
        fontsize=11,
        fontweight="600"
    )

ax.set_title(
    "Booking Rate by Device Type",
    loc="left",
    fontsize=20,
    color=TEXT,
    pad=20
)

ax.set_xlabel("Device Type", color=MUTED)
ax.set_ylabel("Booking Rate", color=MUTED)

ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"{y:.0%}")
)

style(ax)
save(fig, "booking_rate.png")


# ============================================================
# 2. TRAVEL DISTANCE
# ============================================================

distance = [
    df.loc[df["is_mobile"] == 0, "orig_destination_distance"].dropna(),
    df.loc[df["is_mobile"] == 1, "orig_destination_distance"].dropna()
]

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor(BG)

box = ax.boxplot(
    distance,
    tick_labels=["Desktop", "Mobile"],
    patch_artist=True,
    widths=0.5
)

for patch in box["boxes"]:
    patch.set_facecolor(ACCENT_SOFT)
    patch.set_edgecolor(ACCENT)
    patch.set_linewidth(1.5)

for median in box["medians"]:
    median.set_color(ACCENT)
    median.set_linewidth(2)

for element in ["whiskers", "caps"]:
    for item in box[element]:
        item.set_color(MUTED)

for flier in box["fliers"]:
    flier.set_markerfacecolor(ACCENT)
    flier.set_markeredgecolor(ACCENT)
    flier.set_alpha(0.35)

ax.set_title(
    "Travel Distance by Device Type",
    loc="left",
    fontsize=20,
    color=TEXT,
    pad=20
)

ax.set_xlabel("Device Type", color=MUTED)
ax.set_ylabel("Distance", color=MUTED)

style(ax)
save(fig, "distance_boxplot.png")


# ============================================================
# 3. STAY LENGTH
# ============================================================

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor(BG)

sns.histplot(
    data=df,
    x="stay_length",
    hue="is_mobile",
    bins=20,
    kde=True,
    stat="density",
    common_norm=False,
    palette={
        0: ACCENT,
        1: ACCENT_DARK
    },
    alpha=0.45,
    ax=ax
)

ax.set_title(
    "Distribution of Stay Length by Device Type",
    loc="left",
    fontsize=20,
    color=TEXT,
    pad=20
)

ax.set_xlabel("Stay Length (Days)", color=MUTED)
ax.set_ylabel("Density", color=MUTED)

legend = ax.get_legend()

if legend:
    legend.set_title("Device Type")

style(ax)
save(fig, "stay_distribution.png")


# ============================================================
# 4. CORRELATION HEATMAP
# ============================================================

columns = [
    "is_mobile",
    "is_package",
    "srch_adults_cnt",
    "srch_children_cnt",
    "srch_rm_cnt",
    "is_booking"
]

corr = df[columns].corr()

rose_cmap = LinearSegmentedColormap.from_list(
    "rose",
    [
        "#f1d1d9",
        "#f6e1e7",
        "#ffffff",
        "#e9b5c2",
        ACCENT
    ]
)

fig, ax = plt.subplots(figsize=(9, 6))
fig.patch.set_facecolor(BG)

sns.heatmap(
    corr,
    annot=True,
    cmap=rose_cmap,
    vmin=-1,
    vmax=1,
    center=0,
    fmt=".2f",
    linewidths=1,
    linecolor=BG,
    square=True,
    cbar_kws={"label": "Correlation"},
    ax=ax
)

ax.set_title(
    "Correlation Matrix of Booking Features",
    loc="left",
    fontsize=20,
    color=TEXT,
    pad=20
)

ax.set_xlabel("")
ax.set_ylabel("")
ax.tick_params(colors=MUTED, length=0)

save(fig, "correlation_heatmap.png")

print("✓ 4 visualizations saved in /visuals")
