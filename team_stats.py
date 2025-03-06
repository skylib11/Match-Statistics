import json
import csv
import datetime
from collections import defaultdict

# Load the ODI match data

def load_match_data():
    with open("odi_matches.json", "r", encoding="utf-8") as file:
        return json.load(file)

def calculate_team_stats(matches):
    team_stats = defaultdict(lambda: {"matches": 0, "wins": 0, "batting_first_wins": 0, "chasing_wins": 0})
    match_dates = []
    
    for match in matches:
        info = match.get("info", {})
        teams = info.get("teams", [])
        outcome = info.get("outcome", {})
        winner = outcome.get("winner")
        toss = info.get("toss", {})
        toss_winner = toss.get("winner")
        decision = toss.get("decision")
        date = info.get("dates", [None])[0]
        
        if date:
            match_dates.append(date)
        
        for team in teams:
            team_stats[team]["matches"] += 1
        
        if winner:
            team_stats[winner]["wins"] += 1
            if winner == toss_winner:
                if decision == "bat":
                    team_stats[winner]["batting_first_wins"] += 1
                else:
                    team_stats[winner]["chasing_wins"] += 1
    
    match_dates.sort()
    date_range = f"{match_dates[0]} to {match_dates[-1]}" if match_dates else "Unknown"
    
    return team_stats, date_range

def save_team_stats(team_stats, date_range):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"team_stats_{timestamp}.csv"
    
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Team", "Matches Played", "Wins", "Batting First Wins", "Chasing Wins", "Data Range"])
        
        for team, stats in team_stats.items():
            writer.writerow([team, stats['matches'], stats['wins'], stats['batting_first_wins'], stats['chasing_wins'], date_range])
    
    print(f"Stats saved to {output_file}")

def display_team_stats(team_stats, date_range):
    print("\nODI TEAM STATS")
    print(f"Data Range: {date_range}")
    for team, stats in team_stats.items():
        print(f"\n{team}")
        print(f"Matches Played: {stats['matches']}")
        print(f"Wins: {stats['wins']}")
        print(f"Batting First Wins: {stats['batting_first_wins']}")
        print(f"Chasing Wins: {stats['chasing_wins']}")

if __name__ == "__main__":
    matches = load_match_data()
    team_stats, date_range = calculate_team_stats(matches)
    display_team_stats(team_stats, date_range)
    save_team_stats(team_stats, date_range)

