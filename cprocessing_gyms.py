#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run locally after pulling the latest main_data.csv from GitHub.
Needs: pip install pandas matplotlib seaborn
Saves charts into a "charts" folder next to this file.
"""
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

GYMS = ['Helen Newman', 'Noyes', 'Teagle Down', 'Teagle Up', 'Toni Morrison']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
os.makedirs('charts', exist_ok=True)

df = pd.read_csv('main_data.csv', dtype=str)

# one long table: Gym, Date, Time, Count (replaces the five copy-pasted blocks)
frames = []
for gym in GYMS:
    sub = df[['Date', 'Time - ' + gym, gym]].copy()
    sub.columns = ['Date', 'Time', 'Count']
    sub['Gym'] = gym
    frames.append(sub.dropna())
data = pd.concat(frames, ignore_index=True)
if data.empty:
    raise SystemExit("No readings in main_data.csv yet.")

data['Count'] = pd.to_numeric(data['Count'])
data['datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'],
                                  format='%m/%d/%Y %I:%M %p')
data['rounded time'] = data['datetime'].dt.floor('30min')
# stale readings repeat the same gym + time, so keep one of each
data = data.drop_duplicates(subset=['Gym', 'datetime'])
data['Day'] = data['datetime'].dt.day_name()
data['Hour'] = data['datetime'].dt.hour

# 1) average count by hour, all gyms on one chart
by_hour = data.groupby(['Hour', 'Gym'])['Count'].mean().unstack()
ax = by_hour.plot(figsize=(12, 5), marker='o')
ax.set_xlabel('Hour of the day')
ax.set_ylabel('Average count')
ax.set_title('Average gym count by hour')
plt.savefig('charts/count_per_hour_all_gyms.png', dpi=300, bbox_inches='tight')
plt.close()

# 2) day-of-week x hour heatmap for each gym
for gym in GYMS:
    sub = data[data['Gym'] == gym]
    if sub.empty:
        continue
    grid = sub.pivot_table(index='Day', columns='Hour', values='Count', aggfunc='mean')
    grid = grid.reindex([d for d in DAYS if d in grid.index])
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.heatmap(grid, cmap='Reds', ax=ax, cbar_kws={'label': 'Average count'})
    ax.set_title(f'{gym}: busiest times')
    fig.savefig(f"charts/heatmap_{gym.replace(' ', '')}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)

print("Saved charts to the charts folder.")
