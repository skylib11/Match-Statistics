# Match Statistics For Dream11 Fantasy Games
# Dream11 Match Statistics Analysis

## Overview
This project analyzes cricket match data from **Cricsheet JSON files** to generate statistics for Dream11 fantasy games. It includes multiple Python scripts that process match data, calculate fantasy points, and provide performance analytics for players and teams.

## Features
- Extracts and analyzes cricket data for Dream11 fantasy predictions.
- Uses **Cricsheet JSON files** as the primary data source.
- Requires the user to manually download and extract Cricsheet JSON files.
- Combines extracted JSON files using **jq**, saving them as `odi_matches.json`.
- Calculates Dream11 fantasy points based on real match performances.
- Compares player vs. player and team vs. team statistics.
- Evaluates toss and venue impact on match outcomes.
- Summarizes fantasy points across multiple matches.
- Processes squad details from CSV files.

## Files & Scripts

| File Name                     | Description |
|--------------------------------|-------------|
| `dream11_points_calculator.py` | Computes fantasy points for players based on cricket match data from Cricsheet JSON files. |
| `team_stats.py`                | Analyzes overall team performance statistics. |
| `player_stats.py`              | Extracts and evaluates individual player performance. |
| `team_vs_team_stats.py`        | Compares performance between two teams. |
| `player_vs_player.py`          | Compares performance between two players. |
| `toss_analysis.py`             | Analyzes the impact of toss outcomes on match results. |
| `venue_analysis.py`            | Studies venue-based performance trends. |
| `sum_all_fantasy_points.py`    | Aggregates and summarizes fantasy points for all players. |
| `squad.csv`                    | Contains player and team details used for analysis. |
| `odi_matches.json`             | Combined match data extracted from Cricsheet JSON files using jq. |

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/dream11-stats.git
   ```
2. Navigate to the project directory:
   ```sh
   cd dream11-stats
   ```
   ```

## Usage
1. **Download** Cricsheet JSON files from [Cricsheet](https://cricsheet.org/downloads/).
2. **Extract** the downloaded files manually.
3. **Combine** the extracted JSON files using the following `jq` command:
   ```sh
   jq -s '.' path_to_extracted_json_files/*.json > odi_matches.json
   ```
   - This will merge all extracted JSON files into `odi_matches.json`.
   - Ensure that `odi_matches.json` is placed in the same directory as the scripts.
4. Ensure that `squad.csv` is properly formatted with the required player details.
5. Run the scripts based on the required analysis:
   ```sh
   python3 dream11_points_calculator.py
   ```
   ```sh
   python3 team_stats.py
   ```
6. Review the generated insights and statistics for player and team performance.

## Privacy & Security
- This tool works **locally**, ensuring your data remains private.
- Always verify the output before sharing or using it for fantasy cricket predictions.

## Disclaimer
This project is **not affiliated with Dream11**. It is an independent tool for analyzing cricket match data to assist with Dream11 fantasy team selection. Use it responsibly and at your own discretion.

## License
MIT License

## Acknowledgment
This project, including the scripts and README, was generated with the assistance of **ChatGPT**.

