import json
import csv
import datetime
from collections import defaultdict

# Load the ODI match data
def load_match_data():
    with open("odi_matches.json", "r", encoding="utf-8") as file:
        return json.load(file)

def calculate_player_stats(matches):
    run_stats = defaultdict(int)
    wicket_stats = defaultdict(int)
    match_dates = []
    sample_deliveries = []  # Collect sample deliveries for debugging
    
    for match in matches:  # Iterate over list, not dictionary
        info = match.get("info", {})
        date = info.get("dates", [None])[0]
        if date:
            match_dates.append(date)
        
        innings = match.get("innings", [])
        for inning in innings:
            overs = inning.get("overs", [])  # Corrected structure
            for over in overs:
                deliveries = over.get("deliveries", [])
                for delivery in deliveries:
                    batsman = delivery.get("batter")
                    runs = delivery.get("runs", {}).get("batter", 0)
                    bowler = delivery.get("bowler")
                    wickets = delivery.get("wickets", [])  # Updated for multiple wickets
                    
                    if len(sample_deliveries) < 5:
                        sample_deliveries.append(delivery)  # Store first 5 deliveries for debugging
                    
                    if batsman:
                        run_stats[batsman] += runs
                    for wicket in wickets:
                        if bowler:
                            wicket_stats[bowler] += 1
    
    match_dates.sort()
    date_range = f"{match_dates[0]} to {match_dates[-1]}" if match_dates else "Unknown"
    
    return run_stats, wicket_stats, date_range, sample_deliveries

def save_player_stats(run_stats, wicket_stats, date_range):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"player_stats_{timestamp}.csv"
    
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Player", "Runs Scored", "Wickets Taken", "Date Range"])
        
        all_players = set(run_stats.keys()).union(set(wicket_stats.keys()))
        for player in all_players:
            writer.writerow([player, run_stats.get(player, 0), wicket_stats.get(player, 0), date_range])
    
    print(f"Player stats saved to {output_file}")

def display_player_stats(run_stats, wicket_stats, date_range, sample_deliveries):
    print("\nTOP PLAYERS IN ODIs")
    print(f"Data Range: {date_range}")
    
    top_scorers = sorted(run_stats.items(), key=lambda x: x[1], reverse=True)[:10]
    top_wicket_takers = sorted(wicket_stats.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print("\nTop Run-Scorers:")
    for player, runs in top_scorers:
        print(f"  {player}: {runs} runs")
    
    print("\nTop Wicket-Takers:")
    for player, wickets in top_wicket_takers:
        print(f"  {player}: {wickets} wickets")
    
    print("\nSample Deliveries (Debugging):")
    for delivery in sample_deliveries:
        print(json.dumps(delivery, indent=4))  # Pretty print JSON for clarity

if __name__ == "__main__":
    matches = load_match_data()
    run_stats, wicket_stats, date_range, sample_deliveries = calculate_player_stats(matches)
    display_player_stats(run_stats, wicket_stats, date_range, sample_deliveries)
    save_player_stats(run_stats, wicket_stats, date_range)
import json
import csv
import datetime
from collections import defaultdict

# Load the ODI match data
def load_match_data():
    with open("odi_matches.json", "r", encoding="utf-8") as file:
        return json.load(file)

def calculate_player_stats(matches):
    run_stats = defaultdict(int)
    wicket_stats = defaultdict(int)
    match_dates = []
    sample_deliveries = []  # Collect sample deliveries for debugging
    
    for match in matches:  # Iterate over list, not dictionary
        info = match.get("info", {})
        date = info.get("dates", [None])[0]
        if date:
            match_dates.append(date)
        
        innings = match.get("innings", [])
        for inning in innings:
            overs = inning.get("overs", [])  # Corrected structure
            for over in overs:
                deliveries = over.get("deliveries", [])
                for delivery in deliveries:
                    batsman = delivery.get("batter")
                    runs = delivery.get("runs", {}).get("batter", 0)
                    bowler = delivery.get("bowler")
                    wickets = delivery.get("wickets", [])  # Updated for multiple wickets
                    
                    if len(sample_deliveries) < 5:
                        sample_deliveries.append(delivery)  # Store first 5 deliveries for debugging
                    
                    if batsman:
                        run_stats[batsman] += runs
                    for wicket in wickets:
                        if bowler:
                            wicket_stats[bowler] += 1
    
    match_dates.sort()
    date_range = f"{match_dates[0]} to {match_dates[-1]}" if match_dates else "Unknown"
    
    return run_stats, wicket_stats, date_range, sample_deliveries

def save_player_stats(run_stats, wicket_stats, date_range):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"player_stats_{timestamp}.csv"
    
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Player", "Runs Scored", "Wickets Taken", "Date Range"])
        
        all_players = set(run_stats.keys()).union(set(wicket_stats.keys()))
        for player in all_players:
            writer.writerow([player, run_stats.get(player, 0), wicket_stats.get(player, 0), date_range])
    
    print(f"Player stats saved to {output_file}")

def display_player_stats(run_stats, wicket_stats, date_range, sample_deliveries):
    print("\nTOP PLAYERS IN ODIs")
    print(f"Data Range: {date_range}")
    
    top_scorers = sorted(run_stats.items(), key=lambda x: x[1], reverse=True)[:10]
    top_wicket_takers = sorted(wicket_stats.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print("\nTop Run-Scorers:")
    for player, runs in top_scorers:
        print(f"  {player}: {runs} runs")
    
    print("\nTop Wicket-Takers:")
    for player, wickets in top_wicket_takers:
        print(f"  {player}: {wickets} wickets")
    
    print("\nSample Deliveries (Debugging):")
    for delivery in sample_deliveries:
        print(json.dumps(delivery, indent=4))  # Pretty print JSON for clarity

if __name__ == "__main__":
    matches = load_match_data()
    run_stats, wicket_stats, date_range, sample_deliveries = calculate_player_stats(matches)
    display_player_stats(run_stats, wicket_stats, date_range, sample_deliveries)
    save_player_stats(run_stats, wicket_stats, date_range)

