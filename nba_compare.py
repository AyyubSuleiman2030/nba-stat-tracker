import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats


def get_career_stats(player_name):
    # 1. Find the player dictionary by name
    player_dict = players.find_players_by_full_name(player_name)
    if not player_dict:
        return None

    player_id = player_dict[0]['id']

    # 2. Fetch career stats using the player ID
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_totals = career.get_data_frames()[1]

    if career_totals.empty:
        return None

    # Extract total stats for percentage calculations
    gp = career_totals['GP'].iloc[0]
    pts = career_totals['PTS'].iloc[0]
    fga = career_totals['FGA'].iloc[0]
    fta = career_totals['FTA'].iloc[0]
    fg3m = career_totals['FG3M'].iloc[0]
    fg3a = career_totals['FG3A'].iloc[0]

    # 3. Calculate advanced shooting percentages
    ts_pct = (pts / (2 * (fga + 0.44 * fta))) * 100 if (fga + 0.44 * fta) > 0 else 0
    fg3_pct = (fg3m / fg3a) * 100 if fg3a > 0 else 0

    # 4. Calculate per-game averages for core in-game stats
    stats_to_track = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'FGM', 'FGA']
    averages = {}

    for stat in stats_to_track:
        averages[stat] = round(career_totals[stat].iloc[0] / gp, 1)

    averages['3P%'] = round(fg3_pct, 1)
    averages['TS%'] = round(ts_pct, 1)

    return averages


def compare_multiple_players(player_names):
    all_stats = {}

    # Fetch data for everyone in the list
    for name in player_names:
        stats = get_career_stats(name)
        if stats:
            all_stats[name] = stats
        else:
            print(f"Could not find stats for {name}. Check spelling.")

    if len(all_stats) < 2:
        print("Need at least two valid players to compare.")
        return

    print(f"\n--- CAREER STAT COMPARISON ---")

    # Build dynamic header based on the number of players
    header = f"{'Statistic':<10} | " + " | ".join([f"{name:<16}" for name in all_stats.keys()]) + " | Advantage"
    print(header)
    print("-" * len(header))

    stat_keys = list(all_stats.values())[0].keys()

    # Print each row and calculate the leader
    for stat in stat_keys:
        row = f"{stat:<10} | "

        # Isolate the current stat for all players to find the best value
        stat_values = {name: all_stats[name][stat] for name in all_stats.keys()}

        # Turnovers (TOV) are the only stat where a lower number is better
        if stat == 'TOV':
            best_val = min(stat_values.values())
        else:
            best_val = max(stat_values.values())

        # Find all players who match the best value (in case of a tie)
        best_players = [name for name, val in stat_values.items() if val == best_val]
        advantage = ", ".join(best_players) if len(best_players) == 1 else "Tie"

        for name in all_stats.keys():
            row += f"{all_stats[name][stat]:<16} | "

        row += advantage
        print(row)


# Test the tracker with three players
# --- DYNAMIC USER INPUT ---
if __name__ == "__main__":
    print("🏀 Welcome to the NBA Career Stat Tracker 🏀")
    print("Type 'done' when you are finished adding players.\n")

    player_list = []

    # Keep asking for names until the user types 'done'
    while True:
        name = input(f"Enter player {len(player_list) + 1} (or type 'done'): ").strip()

        if name.lower() == 'done':
            break

        if name:  # Make sure they didn't just hit Enter while blank
            player_list.append(name)

    # Run the comparison if they entered at least two players
    if len(player_list) >= 2:
        compare_multiple_players(player_list)
    elif len(player_list) == 1:
        print("You need at least two players to run a comparison!")
    else:
        print("No players entered. Exiting.")
