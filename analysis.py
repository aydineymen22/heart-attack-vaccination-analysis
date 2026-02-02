import pandas as pd

path = "../data/raw/heart_attack_deaths_eurostat.csv"

df = pd.read_csv(path)


df_clean = df[['geo', 'TIME_PERIOD', 'icd10', 'OBS_VALUE']].copy()
df_clean = df_clean.rename(columns={
    'geo': 'country',
    'TIME_PERIOD': 'year',
    'icd10': 'icd_code',
    'OBS_VALUE': 'deaths'
})



df_agg = df_clean.groupby(['country','year'], as_index=False).agg({'deaths':'sum'})


pop = pd.read_csv("../data/raw/population_eurostat.csv")


pop_total = pop[
    (pop['age'] == 'TOTAL') &
    (pop['sex'] == 'T')
]


pop_total = pop_total[['geo', 'TIME_PERIOD', 'OBS_VALUE']]

pop_total.columns = ['country', 'year', 'population']


df_merged = pd.merge(df_agg, pop_total, on=['country', 'year'], how='inner')

df_merged['death_rate_per_100k'] = (df_merged['deaths'] / df_merged['population']) * 100000

df_merged['country'] = df_merged['country'].replace({
    'Germany': 'DE',
    'France': 'FR',
    'Italy': 'IT',
    'Spain': 'ES',
    'Netherlands': 'NL',
    'Poland': 'PL',
    'Turkey': 'TR',
    'United Kingdom': 'UK',
    'GB': 'UK'
})


df_merged['period'] = df_merged['year'].apply(
    lambda x: 'pre_covid' if x <= 2019 else 'covid_period')


period_summary = (
    df_merged
    .groupby('period')['death_rate_per_100k']
    .mean()
    .reset_index()
)


country_period = (
    df_merged
    .groupby(['country', 'period'])['death_rate_per_100k']
    .mean()
    .reset_index()
)


country_wide = country_period.pivot(
    index='country',
    columns='period',
    values='death_rate_per_100k'
).reset_index()


country_wide['change'] = (
    country_wide['covid_period'] - country_wide['pre_covid']
)




vacc = pd.read_csv("../data/raw/vaccinations.csv")

countries_of_interest = [
    'Germany',
    'Spain',
    'France',
    'Italy',
    'Netherlands',
    'Poland',
    'Turkey',
    'United Kingdom'
]

# Filter to relevant countries only
vacc_filtered = vacc[vacc['location'].isin(countries_of_interest)].copy()

# Extract year from date
vacc_filtered['year'] = pd.to_datetime(vacc_filtered['date']).dt.year

# Keep only relevant columns
vacc_reduced = vacc_filtered[
    [
        'location',
        'year',
        'people_vaccinated_per_hundred',
        'people_fully_vaccinated_per_hundred'
    ]
]

# Rename columns for clarity
vacc_reduced.columns = [
    'country_name',
    'year',
    'vaccinated_pct',
    'fully_vaccinated_pct'
]

# Aggregate to yearly values (vaccination accumulates → max is correct)
vacc_yearly = (
    vacc_reduced
    .groupby(['country_name', 'year'])
    .max()
    .reset_index()
)


country_map = {
    'Germany': 'DE',
    'Spain': 'ES',
    'France': 'FR',
    'Italy': 'IT',
    'Netherlands': 'NL',
    'Poland': 'PL',
    'Turkey': 'TR',
    'United Kingdom': 'UK'
}


vacc_yearly['country'] = vacc_yearly['country_name'].map(country_map)


df_full = pd.merge(
    df_merged,
    vacc_yearly[['country', 'year', 'vaccinated_pct', 'fully_vaccinated_pct']],
    on=['country', 'year'],
    how='inner'
)

print(df_merged.groupby('country')['year'].unique())
print(vacc_yearly.groupby('country')['year'].unique()
)

df_full.to_csv("../data/processed/heart_attack_deaths_vaccination.csv", index=False)


import matplotlib.pyplot as plt

plt.figure()
plt.scatter(
    df_full["vaccinated_pct"],
    df_full["death_rate_per_100k"]
)

plt.xlabel("Vaccinated population (%)")
plt.ylabel("Death rate per 100k")
plt.title("Vaccination Rate vs Death Rate (All-Cause Mortality)")

plt.show()
plt.savefig("../figures/vaccination_vs_death_rate_all_cause.png")
###############################



plt.scatter(
    df_full["vaccinated_pct"],
    df_full["death_rate_per_100k"]
)

for _, row in df_full.iterrows():
    plt.text(
        row["vaccinated_pct"],
        row["death_rate_per_100k"],
        row["country"],
        fontsize=8
    )

plt.xlabel("Vaccinated population (%)")
plt.ylabel("Death rate per 100k")
plt.title("Vaccination vs Death Rate by Country")

plt.show()
plt.savefig("../figures/vaccination_vs_death_rate_by_country.png")
###############################


for country in df_full["country"].unique():
    subset = df_full[df_full["country"] == country]
    plt.plot(
        subset["year"],
        subset["death_rate_per_100k"],
        marker='o',
        label=country
    )

plt.xlabel("Year")
plt.ylabel("Death rate per 100k")
plt.title("Death Rate Trend by Country")
plt.legend()
plt.show()
plt.savefig("../figures/death_rate_trends.png")
##############################

fig, ax1 = plt.subplots()

country = "ES"  # change if you want
subset = df_full[df_full["country"] == country]

ax1.plot(subset["year"], subset["death_rate_per_100k"], marker='o')
ax1.set_xlabel("Year")
ax1.set_ylabel("Death rate per 100k")

ax2 = ax1.twinx()
ax2.plot(subset["year"], subset["vaccinated_pct"], linestyle='--', marker='s')
ax2.set_ylabel("Vaccinated %")

plt.title(f"{country}: Vaccination vs Death Rate Over Time")
plt.show()
plt.savefig("../figures/vaccination_vs_death_rate.png")