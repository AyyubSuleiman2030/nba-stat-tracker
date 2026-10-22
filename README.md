# 🏀 NBA Career Stat Tracker

## Overview
The NBA Career Stat Tracker is a Python-based data science tool that fetches live, up-to-date player statistics directly from the NBA's official database. It processes career totals into per-game averages, calculates advanced shooting metrics, and generates a dynamic side-by-side comparison of multiple players to determine statistical advantages.

## Features
* **Live Data Extraction:** Utilizes the `nba_api` to pull real-time JSON data from NBA.com.
* **Advanced Metrics:** Automatically calculates True Shooting Percentage (TS%) and 3-Point Percentage (3P%) using career attempt and make totals.
* **Dynamic Comparison:** Accepts interactive user input to compare an unlimited number of players at once.
* **Automated Advantage Logic:** Evaluates all provided players to highlight the statistical leader in each core category (PTS, REB, AST, STL, BLK, TOV, TS%).

## Technologies Used
* **Python** (Core logic and API requests)
* **pandas** (Data manipulation and DataFrame extraction)
* **nba_api** (Endpoint communication)

## How to Run
1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install pandas nba_api