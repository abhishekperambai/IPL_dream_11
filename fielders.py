import pandas as pd,numpy as np,re,pathlib,warnings
warnings.filterwarnings("ignore")
from scoring_system import ScoringSystem

class Fielding(ScoringSystem):
    def __init__(self,ip):
        self.ip = pathlib.Path(ip)
        
    def read_datasets(self):
        self.bowlers_data = pd.read_csv(self.ip/"career_2008_2019_ball.csv", sep="|")
        
    def compute_dream11_score(self):
        self.bowlers_data.rename(columns={"Ct":"catch","St":"stumping"},inplace=True)
        self.bowlers_data["three_plus_catches"] = (self.bowlers_data["catch"]/3).astype(int)
        dict_ = self.bowlers_data.to_dict("records")
        for i in dict_:
            bowl_score = self.fielding_points(**i)
            i.update({"dream11_score_field":bowl_score})
        
        self.fielder_career_data = pd.DataFrame(dict_).sort_values("dream11_score_field",ascending=False)
        
    def main(self):
        self.read_datasets()
        self.compute_dream11_score()