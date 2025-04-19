import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data
df = pd.read_csv("study_log.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Total time spent per subject
subject_time = df.groupby('Subject')['Duration (mins)'].sum()
print("\nTotal Time per Subject:\n", subject_time)

# Average focus level per subject
focus_avg = df.groupby('Subject')['Focus Level (1-10)'].mean()
print("\nAverage Focus per Subject:\n", focus_avg)

# Plot: Bar chart of time per subject
subject_time.plot(kind='bar', title='Total Study Time per Subject', color='skyblue')
plt.xlabel("Subject")
plt.ylabel("Time (mins)")
plt.tight_layout()
plt.show()

# Plot: Average focus level
focus_avg.plot(kind='bar', title='Average Focus Level per Subject', color='lightgreen')
plt.xlabel("Subject")
plt.ylabel("Focus Level (1-10)")
plt.tight_layout()
plt.show()

# Weekly study time
df['Week'] = df['Date'].dt.isocalendar().week
weekly_time = df.groupby('Week')['Duration (mins)'].sum()

# Plot: Weekly progress
weekly_time.plot(kind='line', marker='o', title='Weekly Study Time')
plt.xlabel("Week Number")
plt.ylabel("Time (mins)")
plt.tight_layout()
plt.show()

# --- Weakest Subject Analysis ---
subject_time_norm = (subject_time - subject_time.min()) / (subject_time.max() - subject_time.min())
focus_avg_norm = (focus_avg - focus_avg.min()) / (focus_avg.max() - focus_avg.min())
combined_score = 0.5 * subject_time_norm + 0.5 * focus_avg_norm
weakest_subject = combined_score.idxmin()
print(f"\nWeakest Subject (needs more focus): {weakest_subject}")
print(f"Recommendation: Spend more time and effort on *{weakest_subject}*. Try shorter, focused sessions and monitor your improvement.")

# Plot: Subject strength score
combined_score.plot(kind='bar', color='coral', title='Subject Strength Score (Higher is Better)')
plt.axhline(combined_score[weakest_subject], color='red', linestyle='--', label='Weakest Subject')
plt.legend()
plt.tight_layout()
plt.show()

# ---  Daily Study Consistency ---
daily_time = df.groupby(df['Date'].dt.date)['Duration (mins)'].sum()
daily_time.plot(kind='line', marker='o', title='Daily Study Consistency', color='purple')
plt.xlabel("Date")
plt.ylabel("Time (mins)")
plt.tight_layout()
plt.show()

# --- Subject Study Frequency ---
study_counts = df['Subject'].value_counts()
study_counts.plot(kind='bar', title='Subject Study Frequency', color='orange')
plt.xlabel("Subject")
plt.ylabel("Sessions Count")
plt.tight_layout()
plt.show()

# --- Productivity Score ---
df['Productivity Score'] = df['Duration (mins)'] * df['Focus Level (1-10)']
productivity_by_day = df.groupby(df['Date'].dt.date)['Productivity Score'].sum()
productivity_by_day.plot(kind='line', marker='o', title='Daily Productivity Score', color='green')
plt.xlabel("Date")
plt.ylabel("Score")
plt.tight_layout()
plt.show()

# --- Best Day to Study ---
df['Weekday'] = df['Date'].dt.day_name()
weekday_avg = df.groupby('Weekday')['Productivity Score'].mean().sort_values()
best_day = weekday_avg.idxmax()
print(f"\nMost Productive Day: {best_day}")
weekday_avg.plot(kind='barh', title='Average Productivity by Weekday', color='skyblue')
plt.tight_layout()
plt.show()

# --- Focus Trend Over Time ---
df_sorted = df.sort_values('Date')
df_sorted.groupby('Date')['Focus Level (1-10)'].mean().plot(
    kind='line', marker='o', title='Focus Trend Over Time', color='brown'
)
plt.xlabel("Date")
plt.ylabel("Avg Focus Level")
plt.tight_layout()
plt.show()

# --- Export Summary Report ---
summary = {
    "Total Study Time": df['Duration (mins)'].sum(),
    "Average Focus Level": round(df['Focus Level (1-10)'].mean(), 2),
    "Weakest Subject": weakest_subject,
    "Most Productive Day": best_day
}
summary_df = pd.DataFrame(summary.items(), columns=["Metric", "Value"])
summary_df.to_csv("study_summary_report.csv", index=False)
print("\nSummary report saved as 'study_summary_report.csv'")