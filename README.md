## 💉 COVID-19 Vaccination & Heart-Attack Mortality in Europe

A transparent, data-driven exploratory analysis using Eurostat and Our World in Data

## 📌 Project Summary

This project investigates the relationship between COVID-19 vaccination coverage and heart-attack–related mortality rates across selected European countries.

Rather than making assumptions or forcing conclusions, the analysis focuses on:

Cause-specific mortality (heart attacks only)

Population-normalized death rates

Strict data alignment

Explicit documentation of limitations

The result is a realistic example of how real-world public health data behaves — incomplete, messy, and informative if handled carefully.

## ❓ Research Question

Is there an observable association between COVID-19 vaccination coverage and heart-attack mortality rates in European countries during the COVID period?

## ⚠️ Important: This analysis explores association, not causation.

## 🗂 Data Sources
📊 Eurostat

Heart-attack deaths (ICD-10 based)

Population by country and year

## 💉 Our World in Data

COVID-19 vaccination coverage (daily → aggregated yearly)

All datasets are publicly available and unmodified at source.

## 🧪 Methodology
## 1️⃣ Heart-Attack Mortality

Filtered Eurostat data to heart-attack ICD codes

Aggregated deaths by country & year

Normalized using deaths per 100,000 population

## 2️⃣ Population Normalization

Used total population only (age = TOTAL, sex = T)

Ensured year-level alignment with mortality data

## 3️⃣ Vaccination Data Processing

Selected relevant European countries

Extracted year from daily vaccination records

Used maximum yearly vaccination percentage

Vaccination is cumulative → max is correct

Standardized country identifiers (ISO-2 codes)

## 4️⃣ Dataset Merging

Used inner joins only

No interpolation

No artificial data extension

Only real, overlapping country-year observations

## 📈 Key Findings

No evidence of an increase in heart-attack mortality during years with high vaccination coverage.

In most overlapping country-year observations, death rates were stable or lower.

A negative correlation was observed between vaccination coverage and heart-attack death rates.

🧠 These results are exploratory and should be interpreted with caution.

## ⚠️ Challenges & How They Were Solved
## 🚧 Limited Data Overlap

Heart-attack mortality data is missing for several countries after 2018–2019.

Vaccination data meaningfully begins in 2020.

Solution:
Used strict inner joins and documented reduced sample size instead of forcing alignment.

## 🌍 Country Code Inconsistencies

Eurostat uses ISO-2 codes (DE, FR, etc.)

Vaccination data uses full country names

Solution:
Created explicit country-code mappings and manually verified merges.

## ❌ Missing Countries After Merge

Some countries appeared in mortality data but disappeared after merging.

Reason:
No overlapping years between mortality and vaccination datasets.

Solution:
Verified available years per country and accepted the limitation rather than fabricating data.

## 🧠 Correlation ≠ Causation

Heart-attack mortality is affected by:

COVID infections

Healthcare access delays

Demographic structure

Reporting practices

Approach:
Results are framed strictly as associations, not causal claims.
