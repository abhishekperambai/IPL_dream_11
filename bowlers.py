import pandas as pd,numpy as np,re,pathlib,warnings
warnings.filterwarnings("ignore")
from scoring_system import ScoringSystem

class Bowlers(ScoringSystem):
    def __init__(self,ip):
        self.ip = pathlib.Path(ip)
        
    def read_datasets(self):
        self.bowlers_data = pd.read_csv(self.ip/"career_2008_2019_ball.csv", sep="|")
        self.ball_by_ball = pd.read_csv(self.ip/"IPL Ball-by-Ball 2008-2020.csv")
        self.venue_data = pd.read_csv(self.ip/"IPL Matches 2008-2020_2.csv")[["id","city","venue","date"]]
        
    def compute_dream11_score(self):
        self.bowlers_data.rename(columns={"4":"four_wi","5":"five_wi"},inplace=True)
        dict_ = self.bowlers_data.to_dict("records")
        for i in dict_:
            bowl_score = self.bowling_points(**i)
            i.update({"dream11_score_ball":bowl_score+self.economy_points(i.get("Econ"))})
        
        self.bowler_career_data = pd.DataFrame(dict_).sort_values("dream11_score_ball",ascending=False)
        
    def compute_score_per_venue(self):
        agg_bowler_data = self.ball_by_ball.groupby(["id","bowler"]).apply(lambda x:(x["is_wicket"]==1).sum()).reset_index().rename(columns={0:"wickets"})
        merged_venue=agg_bowler_data.merge(self.venue_data, on=["id"])
        merged_venue["year"] = pd.to_datetime(merged_venue["date"]).dt.year
        yr_list = [2018,2019,2020]
        merged_venue["year"] = merged_venue["year"].apply(lambda x: 0.7 if x in yr_list else 0.3)
        
        self.wickets_per_venue = merged_venue.groupby(["bowler","venue","year"],as_index=False).agg({"wickets":"sum","id":"count"})
        self.wickets_per_venue.rename(columns={"id":"matches"},inplace=True)
        self.wickets_per_venue["avg_per_venue_year"] = 25*round(self.wickets_per_venue["wickets"]/self.wickets_per_venue["matches"],2)
        
        
        
    def main(self):
        self.read_datasets()
        self.compute_dream11_score()
        self.compute_score_per_venue()
        bowler_scores = self.wickets_per_venue.merge(self.bowler_career_data,left_on=["bowler"],right_on=["Player"])
        final_bowler_scores = bowler_scores[["bowler","venue","year","wickets","matches","avg_per_venue_year","dream11_score_ball"]]
        final_bowler_scores["total_score"] = 0.25*final_bowler_scores["avg_per_venue_year"] + 0.75*(final_bowler_scores["dream11_score_ball"])
        final_bowler_scores["final_score_ball"] = final_bowler_scores["year"]*final_bowler_scores["total_score"]
        final_bowler_scores = final_bowler_scores.groupby(["bowler","venue"],as_index=False).agg({"final_score_ball":"sum","matches":"count"}) 
#         final_bowler_scores["bowling_points"] = 0.25*final_bowler_scores["avg_per_venue"] + 0.75*final_bowler_scores["dream11_score_ball"]
        return final_bowler_scores