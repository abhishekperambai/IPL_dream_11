class ScoringSystem:
    def __init__(self):
        pass
    
    def batting_points(self,**params): # eliminated 30+ run points reward 
        total = 0
        total = params.get("runs",0) + params.get("boundaries",0) \
        + 2*(params.get("sixes",0)) + 8*(params.get("half_cen",0)) \
        + 16*(params.get("cen",0)) - 2*(params.get("ducks",0))
        try:
            return round(total/params.get("Inns",1),2)
        except ZeroDivisionError:
            return 0
        
    def bowling_points(self,**params): # eliminated 3 wicket haul points reward
        total = 0
        total = 25*params.get("Wkts",0) + 12*params.get("Mdns",0) \
        + 8*params.get("four_wi",0) + 16*params.get("five_wi",0)
        try:
            return round(total/(params.get("Inns")),2)
        except ZeroDivisionError:
            return 0
    
    def fielding_points(self,**params):
        total = 0
        total = 8*params.get("catch",0) + 4*params.get("three_plus_catches",0)\
        + 12*params.get("stumping",0) #+ 12*params.get("direct_hit",0) \
        #+ 6*params.get("no_direct_hit",0)
        try:
            return round(total/(params.get("Mat")),2)
        except ZeroDivisionError:
            return 0
    
    def economy_points(self,er):
        if er<=5:
            return 6
        elif er>5 and er<= 6:
            return 4
        elif er>6 and er<=7:
            return 2
        elif er>7 and er<=10:
            return 0
        else:
            return -3
    
    def strike_rate_points(self,sr):
        if sr >=170:
            return 6
        elif sr>=150 and sr<170:
            return 4
        elif sr>=130 and sr <150:
            return 2
        elif sr>=100 and sr<130:
            return 0
        else:
            return -3