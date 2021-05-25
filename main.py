import pandas as pd,numpy as np,re,pathlib,warnings,argparse
warnings.filterwarnings("ignore")

from batsmen import Batsman
from bowlers import Bowlers
from fielders import Fielding

parser = argparse.ArgumentParser()
parser.add_argument("-input_path",required=True)
parser.add_argument("-output_path",required=True)
args = parser.parse_args()


def run_model(ip,op):
    obj = Batsman(ip)
    final_batsman = obj.main()

    obj = Bowlers(ip)
    final_bowlers = obj.main()

    pathlib.Path(op+ "/model_output").mkdir(exist_ok=True,parents=True)
    op_path = pathlib.Path(op)/"model_output"
    final_batsman.to_csv(op_path/"batsman_dream11_scores.csv",sep="|")
    final_bowlers.to_csv(op_path/"bowlers_dream11_scores.csv",sep="|")
    
    
    complete_data = (final_bowlers.merge(final_batsman, how="outer",
                                        left_on =["bowler","venue"],
                                        right_on = ["batsman","venue"])
                                        [["bowler","batsman", "venue","final_score_bat",
                                        "final_score_ball"]]) 
    complete_data["final_score_bat"].fillna(0,inplace=True)
    complete_data["final_score_ball"].fillna(0,inplace=True)
    complete_data["player_score"] = complete_data["final_score_bat"] + complete_data["final_score_ball"]

    for i in range(len(complete_data)):
        if pd.isnull(complete_data.loc[i,"bowler"]):
            complete_data.loc[i,"bowler"] = complete_data.loc[i,"batsman"]
        elif pd.isnull(complete_data.loc[i,"batsman"]):
            complete_data.loc[i,"batsman"] = complete_data.loc[i,"bowler"]
    complete_data.drop(columns=["bowler"],inplace=True)
    complete_data.rename(columns={"batsman":"Player"},inplace=True)
    complete_data.to_csv(op_path/"bat_ball_venue_scores.csv",sep="|")

    obj=Fielding(ip)
    obj.main()
    fielder_data = obj.fielder_career_data
    
    fielder_data.to_csv(op_path/"fielding_scores.csv",sep="|")

    final_data = (complete_data.merge(fielder_data, on = ["Player"])[["Player","venue","player_score",
                                                                      "dream11_score_field"]])
    final_data["career_dream11_score"] = round(final_data["player_score"] + final_data["dream11_score_field"],2)
    final_data = final_data[["Player","venue","career_dream11_score"]]
    final_data.to_csv(op_path/"career_scores_dream11.csv",sep="|",index=False)
    
if __name__=="__main__":
    ip = args.input_path
    op = args.output_path #r"E:\Co-Learning Lounge\Actual Data\final_test\IPL_datasets"
    run_model(ip,op)

