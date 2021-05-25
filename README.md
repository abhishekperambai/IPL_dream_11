# IPL_dream_11
Repository with code to rate each player and give the top 11 performing players given the teams and venue.

### Parameters
input_path  -> path to the required datasets (placed under the data directory)
output_path -> path to save the output of the model (sample output placed under the model_output directory)

### Steps to run the model
1. cmd ==> python "path to main.py" --input_path=<input_path> --output_path=<output_path>. It generates the carrer dream 11 scores for each player at a particualr venue.
2. Then run "match_venue_points.py"
    a. Takes input as the IPL_squad_list from data folder and career_dream11_scores.csv from the model_output_folder along with teams and venue. (Note: Punjab is still considered to be as KXIP instead of PBKS)
    b. Gives the ratings for each player from both teams in the given venue sorted in the descending order.
