import pandas as pd

def process_fantasy_points(squad_file, fantasy_points_file, output_file):
    # Load the squad data
    squad_df = pd.read_csv(squad_file)
    fantasy_df = pd.read_csv(fantasy_points_file)
    
    # Ensure column names are consistent
    squad_player_col = "Players"  # Corrected column name for squad file
    fantasy_player_col = "Player"  # Corrected column name for fantasy points file
    points_col = "Fantasy Points"
    match_col = "Match Date"  # Adjusted based on actual column name
    
    if squad_player_col not in squad_df.columns or fantasy_player_col not in fantasy_df.columns:
        raise ValueError("Column name mismatch. Please check the player column name in both files.")
    
    # Result storage
    results = []
    
    for player in squad_df[squad_player_col]:
        # Get player's fantasy points data
        player_data = fantasy_df[fantasy_df[fantasy_player_col] == player]
        
        # Sort by match date (assuming newer dates are more recent)
        player_data = player_data.sort_values(by=match_col, ascending=False)
        
        # Get the last 10 matches
        recent_matches = player_data.head(10)
        
        # Compute total and average
        total_points = recent_matches[points_col].sum()
        average_points = recent_matches[points_col].mean()
        match_points = recent_matches[points_col].tolist()
        
        # Store results
        results.append([player, total_points, average_points] + match_points)
    
    # Create DataFrame and save
    columns = ["Player", "Total Points", "Average Points"] + [f"Match {i+1}" for i in range(10)]
    results_df = pd.DataFrame(results, columns=columns)
    results_df.to_csv(output_file, index=False)
    
    print(f"Fantasy points summary saved to {output_file}")

# Usage
squad_file = "squad.csv"
fantasy_points_file = "fantasy_points_2024.csv"
output_file = "fantasy_summary.csv"
process_fantasy_points(squad_file, fantasy_points_file, output_file)
