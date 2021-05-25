# IPL_dream_11
Repository with code to rate each player and give the top 11 performing players given the teams and venue.

### Parameters
input_path  -> path to the required datasets (placed under the data directory)
output_path -> path to save the output of the model (sample output placed under the model_output directory)

### Steps to run the model
1. Command to run python "path to main.py". It generates the carrer dream 11 scores for each player at a particular venue.
2. Then run python "path to "match_venue_points.py" -team1=<team1> -team2=<team2> -venue=<venue> -output_path<path to save the output>
    a. Gives the ratings for each player from both teams in the given venue sorted in the descending order.
    b. Note: Punjab is still considered to be as KXIP instead of PBKS.
