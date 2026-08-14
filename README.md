# Hotel Booking Analysis: Mobile vs Desktop Users

## Overview

This project analyzes whether mobile and desktop users behave differently when searching and booking hotels.

The dataset contains search and booking information from a hotel booking platform.

## Research Question

Do mobile users show different booking behavior compared to desktop users?

## Dataset Features Used

- is_mobile
- is_booking
- srch_ci
- srch_co
- orig_destination_distance
- srch_adults_cnt
- srch_children_cnt

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Analysis Steps

1. Data Cleaning
2. Feature Engineering
3. Exploratory Data Analysis
4. Data Visualization
5. Interpretation of Findings

## Visualizations

### Booking Rate by Device Type

visuals/booking_rate.png

### Travel Distance

visuals/distance_boxplot.png

### Stay Length

visuals/stay_length_boxplot.png

### Stay Length Distribution

visuals/stay_distribution.png

## Key Findings

- Comparison of booking rates between mobile and desktop users
- Travel distance differences
- Stay duration patterns
- Search behavior insights

## Run Locally

```bash
git clone https://github.com/yourusername/hotel-booking-mobile-vs-desktop-analysis.git

cd hotel-booking-mobile-vs-desktop-analysis

pip install -r requirements.txt

python src/analysis.py
```
