import pandas as pd
import numpy as np

# ============================================
# SCHRITT 1: CSV-Datei laden
# ============================================
df = pd.read_csv('data/expedia_data.csv')  # Pfad anpassen!

# ============================================
# SCHRITT 2: Erster Überblick
# ============================================
print("=" * 50)
print("DATEN ÜBERBLICK")
print("=" * 50)

print("\n1. Erste 5 Zeilen:")
print(df.head())

print("\n2. Daten-Informationen:")
print(df.info())

print("\n3. Missing Values pro Spalte:")
print(df.isna().sum())

print("\n4. Statistische Übersicht:")
print(df.describe())

print("\n5. Duplikate:")
print(f"Anzahl Duplikate: {df.duplicated().sum()}")

# ============================================
# SCHRITT 3: Data Cleaning
# ============================================
print("\n" + "=" * 50)
print("DATA CLEANING")
print("=" * 50)

# 3.1 Missing Values behandeln
print("\n3.1 Missing Values behandeln...")

# Beispiel: travel_distance mit Median füllen
if 'travel_distance' in df.columns:
    median_distance = df['travel_distance'].median()
    df['travel_distance'] = df['travel_distance'].fillna(median_distance)
    print(f"  - travel_distance: Missing Values mit Median gefüllt ({median_distance:.2f})")

# Rows mit Missing Values in wichtigen Spalten entfernen
wichtige_spalten = ['device', 'is_booking']  # Spalten-Namen anpassen!
df = df.dropna(subset=wichtige_spalten)
print(f"  - Rows mit Missing Values in {wichtige_spalten} entfernt")

# 3.2 Ausreißer behandeln
print("\n3.2 Ausreißer behandeln...")

# travel_distance: IQR-Methode
if 'travel_distance' in df.columns:
    Q1 = df['travel_distance'].quantile(0.25)
    Q3 = df['travel_distance'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df['travel_distance'] = df['travel_distance'].clip(lower=lower_bound, upper=upper_bound)
    print(f"  - travel_distance: Ausreißer gecapped ({lower_bound:.2f} bis {upper_bound:.2f})")

# stay_length: Auf 1-30 Tage beschränken
if 'stay_length' in df.columns:
    df['stay_length'] = df['stay_length'].clip(lower=1, upper=30)
    print("  - stay_length: Auf 1-30 Tage beschränkt")

# 3.3 Daten-Typen und Konsistenz
print("\n3.3 Daten-Typen und Konsistenz...")

# device_type standardisieren
if 'device' in df.columns:
    df['device'] = df['device'].str.strip().str.title()
    print("  - device: Bereinigt (strip + title)")

# is_booking als int sicherstellen
if 'is_booking' in df.columns:
    df['is_booking'] = df['is_booking'].astype(int)
    print("  - is_booking: Zu int konvertiert")

# 3.4 Duplikate entfernen
print("\n3.4 Duplikate entfernen...")
vorher = len(df)
df = df.drop_duplicates()
nachher = len(df)
print(f"  - {vorher - nachher} Duplikate entfernt")

# ============================================
# SCHRITT 4: Ergebnis speichern
# ============================================
print("\n" + "=" * 50)
print("ERGEBNIS")
print("=" * 50)

print(f"\nUrsprüngliche Rows: {vorher}")
print(f"Bereinigte Rows: {nachher}")
print(f"Verbleibende Missing Values: {df.isna().sum().sum()}")

# Bereinigte Daten speichern
df.to_csv('data/expedia_data_cleaned.csv', index=False)
print("\n✓ Bereinigte Daten gespeichert als: data/expedia_data_cleaned.csv")

# ============================================
# SCHRITT 5: Für Analyse verwenden
# ============================================
# Ab hier kannst du mit df weiterarbeiten für deine Analyse
print("\n" + "=" * 50)
print("BEREIT FÜR ANALYSE!")
print("=" * 50)

# Beispiel: Erste Analyse
print("\nBooking-Rate nach Device:")
print(df.groupby('device')['is_booking'].mean())
