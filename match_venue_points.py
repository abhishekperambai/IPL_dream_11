import pandas as pd,numpy as np,re,pathlib,warnings,argparse
warnings.filterwarnings("ignore")



parser = argparse.ArgumentParser()
parser.add_argument("--team1",required=True)
parser.add_argument("--team2",required=True)
parser.add_argument("--venue",required=True)
parser.add_argument("--output_path",required=True)
args = parser.parse_args()

ip = pathlib.Path(__file__).parent

def get_players(df,list_,venue):
    final_df = []
    for player in list_:
        test = (df[(df["Player"]==player)&(df["venue"]==venue)][["Player","career_dream11_score"]])
        if len(test)>0:
            final_df.append(test.to_dict("records"))
        else:
            test = df[df["Player"]==player]
            test = test.groupby("Player",as_index=False)[["career_dream11_score"]].mean()
            if len(test)>0:
                final_df.append(test.to_dict("records"))
    return pd.DataFrame([j for i in final_df for j in i])


def get_points(t1,t2,venue):
    career_df = pd.read_csv((ip/"model_output"/"career_scores_dream11.csv"),sep="|")
    squad = pd.read_csv((ip/"data"/"IPL_2021_Squad_List.csv"),sep="|")[[t1,t2]]
    T1 = list(squad[t1])
    T2 = list(squad[t2])
    slice1 = get_players(career_df,T1,venue)
    slice2 = get_players(career_df,T2,venue)
    return slice1.append(slice2).sort_values("career_dream11_score", ascending=False)
    
if __name__=="__main__":
    t1 = args.team1
    t2 = args.team2
    venue = args.venue
    op = pathlib.Path(args.output_path)
    df = get_points(t1,t2,venue)
    df["career_dream11_score"] = round(df["career_dream11_score"],2)
    df.to_csv(op/"{}_{}.csv".format(t1,t2),sep="|",index=False)