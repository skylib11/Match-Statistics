import json
import csv
import datetime

# Load the ODI match data
def load_match_data():
    with open("odi_matches.json", "r", encoding="utf-8") as file:
        return json.load(file)

def calculate_team_vs_team_stats(matches, team1, team2):
    total_matches = 0
    team1_wins = 0
    team2_wins = 0
    win_margins = []
    match_dates = []
    
    for match in matches:
        info = match.get("info", {})
        teams = info.get("teams", [])
        outcome = info.get("outcome", {})
        winner = outcome.get("winner")
        margin = outcome.get("by", {})
        date = info.get("dates", [None])[0]
        
        if date:
            match_dates.append(date)
        
        if team1 in teams and team2 in teams:
            total_matches += 1
            if winner == team1:
                team1_wins += 1
                win_margins.append(f"{team1} won by {margin}")
            elif winner == team2:
                team2_wins += 1
                win_margins.append(f"{team2} won by {margin}")
    
    match_dates.sort()
    date_range = f"{match_dates[0]} to {match_dates[-1]}" if match_dates else "Unknown"
    
    return total_matches, team1_wins, team2_wins, win_margins, date_range

def save_team_vs_team_stats(team1, team2, total_matches, team1_wins, team2_wins, win_margins, date_range):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"team_vs_team_stats_{team1}_vs_{team2}_{timestamp}.csv"
    
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Teams", "Total Matches", f"{team1} Wins", f"{team2} Wins", "Date Range"])
        writer.writerow([f"{team1} vs {team2}", total_matches, team1_wins, team2_wins, date_range])
        
        writer.writerow([""])
        writer.writerow(["Win Margins"])
        for margin in win_margins:
            writer.writerow([margin])
    
    print(f"Head-to-Head stats saved to {output_file}")

def display_team_vs_team_stats(team1, team2, total_matches, team1_wins, team2_wins, win_margins, date_range):
    print(f"\nTEAM-VS-TEAM: {team1} vs {team2}")
    print(f"Total Matches: {total_matches}")
    print(f"{team1} Wins: {team1_wins}")
    print(f"{team2} Wins: {team2_wins}")
    print(f"Date Range: {date_range}")
    print("\nWin Margins:")
    for margin in win_margins:
        print(f"  {margin}")

if __name__ == "__main__":
    matches = load_match_data()
    team1 = "India"
    team2 = "Australia"
    total_matches, team1_wins, team2_wins, win_margins, date_range = calculate_team_vs_team_stats(matches, team1, team2)
    display_team_vs_team_stats(team1, team2, total_matches, team1_wins, team2_wins, win_margins, date_range)
    save_team_vs_team_stats(team1, team2, total_matches, team1_wins, team2_wins, win_margins, date_range)

