import pandas as pd,numpy as np,re,pathlib,warnings
warnings.filterwarnings("ignore")
from scoring_system import ScoringSystem


class Batsman(ScoringSystem):
    def __init__(self,ip):
        self.ip = pathlib.Path(ip)
        
    def read_datasets(self):
        self.batsman_data = pd.read_csv(self.ip/"career_2008_2019_bat.csv",sep="|")
        self.ball_by_ball = pd.read_csv(self.ip/"IPL Ball-by-Ball 2008-2020.csv")
        self.venue_data = pd.read_csv(self.ip/"IPL Matches 2008-2020_2.csv")[["id","city","venue","date"]]
        
    def compute_dream11_score(self):
        self.batsman_data["boundaries"] = self.batsman_data["4s"] + self.batsman_data["6s"]
        self.batsman_data.rename(columns={"Runs":"runs","6s":"sixes","50":"half_cen","100":"cen"},inplace=True)
        dict_ = self.batsman_data.to_dict("records")
        for i in dict_:
            bat_score = self.batting_points(**i)
            i.update({"dream11_score_bat":bat_score+self.strike_rate_points(i.get("SR"))})
        
        self.batsman_career_data = pd.DataFrame(dict_).sort_values("dream11_score_bat",ascending=False)
        
    def compute_score_per_venue(self):
        agg_batsman_data = self.ball_by_ball.groupby(["id","batsman"],as_index=False)[["batsman_runs"]].sum()
        merged_venue=agg_batsman_data.merge(self.venue_data, on=["id"])
        merged_venue["year"] = pd.to_datetime(merged_venue["date"]).dt.year
        yr_list = [2018,2019,2020]
        merged_venue["year"] = merged_venue["year"].apply(lambda x: 0.7 if x in yr_list else 0.3)
        
        self.runs_per_venue = merged_venue.groupby(["batsman","venue","year"],as_index=False).agg({"batsman_runs":"sum","id":"count"})
        self.runs_per_venue.rename(columns={"id":"matches"},inplace=True) 
        self.runs_per_venue["avg_per_venue_year"] = round(self.runs_per_venue["batsman_runs"]/self.runs_per_venue["matches"],2)
        
    def main(self):
        self.read_datasets()
        self.compute_dream11_score()
        self.compute_score_per_venue()
        batsman_scores = self.runs_per_venue.merge(self.batsman_career_data,left_on=["batsman"],right_on=["Player"])
        final_batsman_scores = batsman_scores[["batsman","venue","year","matches","avg_per_venue_year","dream11_score_bat"]]
        
        final_batsman_scores["total_score"] = 0.25*final_batsman_scores["avg_per_venue_year"] + 0.75*(final_batsman_scores["dream11_score_bat"])
        final_batsman_scores["final_score_bat"] = final_batsman_scores["year"]*final_batsman_scores["total_score"]
        final_batsman_scores = final_batsman_scores.groupby(["batsman","venue"],as_index=False).agg({"final_score_bat":"sum","matches":"count"}) 
        return final_batsman_scores