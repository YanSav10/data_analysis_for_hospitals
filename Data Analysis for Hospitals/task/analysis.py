# write your code here
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option('display.max_columns', 8)

general_df = pd.read_csv('test/general.csv')
prenatal_df = pd.read_csv('test/prenatal.csv')
sports_df = pd.read_csv('test/sports.csv')

prenatal_df.columns = general_df.columns
sports_df.columns = general_df.columns
df = pd.concat([general_df, prenatal_df, sports_df], ignore_index=True)
df.drop(columns="Unnamed: 0", inplace=True)

df.dropna(how="all", inplace=True)
df["gender"].replace({"man": "m", "male": "m", "woman": "f", "female": "f"}, inplace=True)
df["gender"].fillna("f", inplace=True)
df.fillna(0, inplace=True)

most_patients_hospital = df['hospital'].value_counts().idxmax()

stomach_issues_general = df[(df['hospital'] == 'general') & (df['diagnosis'] == 'stomach')].shape[0]
share_stomach_general = round(stomach_issues_general / df[df['hospital'] == 'general'].shape[0], 3)

dislocation_issues_sports = df[(df['hospital'] == 'sports') & (df['diagnosis'] == 'dislocation')].shape[0]
share_dislocation_sports = round(dislocation_issues_sports / df[df['hospital'] == 'sports'].shape[0], 3)

median_age_general = df[df['hospital'] == 'general']['age'].median()
median_age_sports = df[df['hospital'] == 'sports']['age'].median()
age_difference = abs(median_age_general - median_age_sports)

blood_tests_count = df[df['blood_test'] == 't'].groupby('hospital').size()
most_tests_hospital, most_tests_count = blood_tests_count.idxmax(), blood_tests_count.max()

plt.figure(figsize=(10, 6))
plt.hist(df['age'].dropna(), bins=[0, 15, 35, 55, 70, 80], edgecolor='black')
plt.title('Distribution of Patient Ages')
plt.xlabel('Age')
plt.ylabel('Number of Patients')
plt.grid(True)
plt.show()

age_bins = pd.cut(df['age'], bins=[0, 15, 35, 55, 70, 80])
most_common_age_group = age_bins.value_counts().idxmax()

diagnosis_counts = df['diagnosis'].value_counts()
plt.figure(figsize=(10, 6))
diagnosis_counts.plot.pie(autopct='%1.1f%%')
plt.title('Distribution of Diagnoses Among All Hospitals')
plt.ylabel('')
plt.show()

most_common_diagnosis = diagnosis_counts.idxmax()

# 3. Creating a violin plot for height distribution by hospitals
plt.figure(figsize=(10, 6))
sns.violinplot(x='hospital', y='height', data=df)
plt.title('Height Distribution by Hospital')
plt.xlabel('Hospital')
plt.ylabel('Height (cm or other units)')
plt.show()

reason_for_gaps = ("The gaps and peaks in height distribution may be due to different units of measurement or the "
                   "specialized patient groups that different hospitals treat.")


print(f"The answer to the 1st question: {most_common_age_group}")
print(f"The answer to the 2nd question: {most_common_diagnosis}")
print(f"The answer to the 3rd question: {reason_for_gaps}")
