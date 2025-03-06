import pandas as pd
import json
from itertools import product

# Load squad data
squad_file = "squad.csv"
squad_df = pd.read_csv(squad_file)

# Ensure column names are correct
squad_df.columns = [col.strip() for col in squad_df.columns]

# Separate teams
teams = squad_df.groupby("Team")["Players"].apply(list).to_dict()

# Generate all player vs player combinations between different teams
pvp_combinations = []
for (team1, players1), (team2, players2) in product(teams.items(), repeat=2):
    if team1 != team2:
        for player1, player2 in product(players1, players2):
            pvp_combinations.append([player1, team1, player2, team2])

# Convert to DataFrame
pvp_df = pd.DataFrame(pvp_combinations, columns=["Player1", "Team1", "Player2", "Team2"])

# Load ODI match data
odi_file = "odi_matches.json"
with open(odi_file, "r") as f:
    odi_data = json.load(f)

# Extract relevant player vs player stats from nested JSON structure
match_data = []
for match in odi_data:
    for inning in match.get("innings", []):
        team = inning.get("team", "Unknown")
        for over in inning.get("overs", []):
            for delivery in over.get("deliveries", []):
                batter = delivery.get("batter", "Unknown")
                bowler = delivery.get("bowler", "Unknown")
                runs = delivery.get("runs", {}).get("total", 0)
                balls_faced = 1  # Each delivery is one ball faced
                dot_ball = 1 if runs == 0 else 0
                boundary_4 = 1 if delivery.get("runs", {}).get("batter", 0) == 4 else 0
                boundary_6 = 1 if delivery.get("runs", {}).get("batter", 0) == 6 else 0
                wickets = len(delivery.get("wickets", []))
                
                # Identify bowler's team
                bowler_team = next((t for t, players in teams.items() if bowler in players), "Unknown")
                
                match_data.append([batter, team, bowler, bowler_team, runs, balls_faced, dot_ball, boundary_4, boundary_6, wickets])

# Convert extracted data to DataFrame
odi_df = pd.DataFrame(match_data, columns=["Player1", "Team1", "Player2", "Team2", "Runs", "Balls Faced", "Dot Balls", "4s", "6s", "Wickets"])

# Aggregate all matches before merging
aggregated_stats = odi_df.groupby(["Player1", "Team1", "Player2", "Team2"], as_index=False).sum()

# Remove rows where all performance stats are zero
stats_columns = ["Runs", "Balls Faced", "Dot Balls", "4s", "6s", "Wickets"]
aggregated_stats = aggregated_stats[(aggregated_stats[stats_columns] != 0).any(axis=1)]

# Merge player stats
pvp_stats = pvp_df.merge(aggregated_stats, on=["Player1", "Team1", "Player2", "Team2"], how="left")

# Fill missing values with 0
pvp_stats.fillna(0, inplace=True)

# Calculate Economy Rate and Strike Rate
pvp_stats["Economy Rate"] = (pvp_stats["Runs"] / (pvp_stats["Balls Faced"] / 6)).replace([float("inf"), float("-inf")], 0)
pvp_stats["Strike Rate"] = ((pvp_stats["Runs"] / pvp_stats["Balls Faced"]) * 100).replace([float("inf"), float("-inf")], 0)

# Calculate Batting Average (AR) and Bowling Average (AVG)
pvp_stats["AR"] = (pvp_stats["Runs"] / pvp_stats["Wickets"]).replace([float("inf"), float("-inf"), pd.NA], 0)
pvp_stats["AVG"] = (pvp_stats["Runs"] / pvp_stats["Wickets"]).replace([float("inf"), float("-inf"), pd.NA], 0)

# Save to CSV
output_file = "player_vs_player.csv"
pvp_stats.to_csv(output_file, index=False)

print(f"Player vs Player stats saved to {output_file}")

