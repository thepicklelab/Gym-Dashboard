#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collects the live gym counts from the Cornell Connect2Concepts page and
appends one row to main_data.csv. Run by the GitHub Action every 30 minutes.

Safe to run any time: outside 7 AM-11 PM Eastern it does nothing, and it
skips readings that are stale (a gym whose "Updated" time hasn't changed).
"""

import os
from datetime import datetime

import pandas as pd
import pytz
import requests
from bs4 import BeautifulSoup as bs

import gym_helpers

URL = "https://connect2concepts.com/connect2/?type=circle&key=355de24d-d0e4-4262-ae97-bc0c78b92839&loc_status=false"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Referer": "https://example.com",
    "Connection": "keep-alive",
}

CSV_FILE = 'main_data.csv'

# website name -> the short name used in the CSV
GYM_NAMES = {'Helen Newman Fitness Center': 'Helen Newman',
             'Noyes Fitness Center': 'Noyes',
             'Teagle Down Fitness Center': 'Teagle Down',
             'Teagle Up Fitness Center': 'Teagle Up',
             'Toni Morrison Fitness Center': 'Toni Morrison'}
GYMS = list(GYM_NAMES.values())

COLUMNS = ['Day of the Week', 'Date']
for _gym in GYMS:
    COLUMNS += ['Time - ' + _gym, _gym]


def fetch_blocks():
    """Download the page and return one HTML string per gym block."""
    response = requests.get(URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = bs(response.text, 'html.parser')
    blocks = soup.find_all('div', {'style': 'text-align:center;'})
    # drop the non-gym courts
    return [str(b) for b in blocks if "Court" not in str(b)]


def build_row(blocks):
    """Turn the page blocks into one dictionary keyed by CSV column."""
    row = {c: '' for c in COLUMNS}
    for idx, block in enumerate(blocks):
        try:
            # only keep readings from today's date (skips old data when closed)
            if not gym_helpers.is_current_date(block):
                continue
            try:
                full_name = gym_helpers.get_name(block)
            except IndexError:
                full_name = None
            gym = GYM_NAMES.get(full_name)
            if gym is None and idx == 0:
                gym = 'Helen Newman'   # original behavior: first block on the page is Helen Newman
            if gym is None:
                continue               # unknown block: ignore instead of crashing
            row['Time - ' + gym] = gym_helpers.get_time(block)
            row[gym] = gym_helpers.get_count(block)
            if not row['Date']:
                row['Day of the Week'] = gym_helpers.find_day(block)
                row['Date'] = gym_helpers.get_date(block)
        except (IndexError, ValueError) as e:
            print(f"Could not read block {idx}: {e}")
    return row


def drop_stale(row, df):
    """Blank out a gym whose time is the same as its last saved reading today."""
    for gym in GYMS:
        tcol = 'Time - ' + gym
        if not row[tcol] or tcol not in df.columns:
            continue
        prev = df[(df['Date'] == row['Date']) & df[tcol].notna()]
        if not prev.empty and prev[tcol].iloc[-1] == row[tcol]:
            row[tcol] = ''
            row[gym] = ''


def append_row(row):
    exists = os.path.exists(CSV_FILE)
    if exists:
        with open(CSV_FILE, 'rb+') as f:      # make sure the file ends with a newline
            f.seek(0, os.SEEK_END)
            if f.tell() > 0:
                f.seek(-1, os.SEEK_END)
                if f.read(1) != b'\n':
                    f.write(b'\n')
    pd.DataFrame([row], columns=COLUMNS).to_csv(
        CSV_FILE, mode='a', header=not exists, index=False)


def run_gym():
    try:
        blocks = fetch_blocks()
    except requests.RequestException as e:
        print(f"Could not reach the gym page: {e}")
        return

    row = build_row(blocks)

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, dtype=str)
    else:
        df = pd.DataFrame(columns=COLUMNS)
    drop_stale(row, df)

    # only save if at least one gym has a fresh reading
    if any(row[c] != '' for c in COLUMNS[2:]):
        append_row(row)
        print("Saved a new row.")
    else:
        print("Nothing new to save.")


if __name__ == '__main__':
    hour = datetime.now(pytz.timezone('US/Eastern')).hour
    if 7 <= hour < 23:
        run_gym()
    else:
        print("Outside 7 AM-11 PM Eastern; nothing to do.")
