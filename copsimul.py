import random, itertools, statistics, json
from collections import Counter


class Citizen(object):
    def __init__(self, race):
        self.race = race
        self.criminal = False
            
    
class Game(object):
    def __init__(self, grid, bias_level):
        self.grid = grid
        self.bias_level = bias_level
        self.quadrant_cop_allocation = {"nw": 9, "ne": 9, "se": 9, "sw": 9}
        self.busts_by_race = Counter({"white": 0, "black": 0})
        self.busts_by_quadrant = Counter({"nw": 0, "ne": 0, "se": 0, "sw": 0})
        self.pick_criminals()
        
    def pick_criminals(self):
        black_criminals = random.sample(self.grid.black_citizens, 24)
        white_criminals = random.sample(self.grid.white_citizens, 24)
        for criminal in black_criminals:
            criminal.criminal = True
        for criminal in white_criminals:
            criminal.criminal = True
                        
    def allocate_cops(self):
        total_busts = sum(self.busts_by_quadrant.values())
        try:
            fractions_by_quadrant = {key: self.busts_by_quadrant[key]/total_busts for key in self.busts_by_quadrant}
            cops_by_quadrant = {key: 3 + int(24 * fractions_by_quadrant[key]) for key in fractions_by_quadrant}
            remaining_cops = 24 - sum(cops_by_quadrant.values())
            if remaining_cops > 0:
                max_crime = max(self.busts_by_quadrant.values())
                top_crime_quadrants = [k for k in busts_by_quadrant if busts_by_quadrant[k] == max_crime]  # in case there are multiple quadrants with max crime level, randomly select which district to get most cops
                cops_by_quadrant[random.choice(top_crime_quadrants)] += remaining_cops
            self.quadrant_cop_allocation = cops_by_quadrant
        except ZeroDivisionError:  # account for case where nobody has been caught yet (definitely happens in first round)
            self.quadrant_cop_allocation = {"nw": 9, "ne": 9, "se": 9, "sw": 9}
            
    def bother_citizen(self, cell):
        busted = False
        prob_catch = 0.5
        race = cell.citizen.race
        if race == "black":
            prob_catch += self.bias_level
        if cell.citizen.criminal:
            roll_dice = random.random()
            if roll_dice <= prob_catch:
                busted = True
        return {"busted": busted, "race": race}

    def investigate_crimes(self):
        busts_by_race_this_round = Counter({"white": 0, "black": 0})
        busts_by_quadrant_this_round = Counter({"nw": 0, "ne": 0, "se": 0, "sw": 0})
        for quadrant in self.quadrant_cop_allocation:
            cells_to_investigate = random.sample(self.grid.quadrants[quadrant], self.quadrant_cop_allocation[quadrant])
            for cell in cells_to_investigate:
                result = self.bother_citizen(cell)
                if result["busted"]:
                    busts_by_race_this_round[result["race"]] += 1
                    busts_by_quadrant_this_round[quadrant] += 1
        self.busts_by_race += busts_by_race_this_round
        self.busts_by_quadrant += busts_by_quadrant_this_round
                                                
    def play_round(self):
        self.allocate_cops()
        self.investigate_crimes()
        
    def calculate_racial_inequality(self):
        try:
            return self.busts_by_race["black"] / self.busts_by_race["white"]
        except ZeroDivisionError:
            return self.busts_by_race["black"]  # just in case no white people ever get busted
        
    def play_all_rounds(self):
        for x in range(200):
            self.play_round()
        self.final_inequality = self.calculate_racial_inequality()
        return {"segregation_level": self.grid.segregation_level, "bias_level": self.bias_level, "final_inequality": self.final_inequality}
            

class Cell(object):
    def __init__(self, citizen, coordinates):
        self.citizen = citizen
        self.coordinates = coordinates
        
    def __getitem__(self, index):
        return self.coordinates[index]


class Grid(object):
    def __init__(self):
        self.black_citizens = [Citizen("black") for x in range(72)]
        self.white_citizens = [Citizen("white") for x in range(72)]
        coordinates = list(itertools.product(range(12), range(12)))
        allcits = self.black_citizens + self.white_citizens
        random.shuffle(allcits)
        self.cells = [Cell(x[0], x[1]) for x in zip(allcits, coordinates)]
        self.quadrants = {}
        self.quadrants["nw"] = list(filter(lambda x: x[0] < 6 and x[1] < 6, self.cells))
        self.quadrants["ne"] = list(filter(lambda x: x[0] < 6 and x[1] >= 6, self.cells))
        self.quadrants["sw"] = list(filter(lambda x: x[0] >= 6 and x[1] < 6, self.cells))
        self.quadrants["se"] = list(filter(lambda x: x[0] >= 6 and x[1] >= 6, self.cells))
        self.calculate_segregation_level()
                
    def calculate_segregation_level(self):
        black_counts = {"nw": 0, "ne": 0, "se": 0, "sw": 0}
        for quadrant, celllist in self.quadrants.items():
            for cell in celllist:
                if cell.citizen.race == "black":
                    black_counts[quadrant] += 1
        self.segregation_level = max(black_counts.values()) - min(black_counts.values())


if __name__ == "__main__":
    random.seed(90210)  # for reproducibility
    grids = []
    for x in range(1000):
        grids.append(Grid())
    bias_levels = [0, 0.1, 0.2, 0.3, 0.4]
    games = []
    for x in range(5):
        for grid in grids:
            for level in bias_levels:
                games.append(Game(grid, level))  
    raw_results = []
    for game in games:
        raw_results.append(game.play_all_rounds())
    with open("raw_simul_dump.json", 'w') as rj:
        json.dump(raw_results, rj)
    segregation = [x['segregation_level'] for x in raw_results]
    bias = [x['bias_level'] for x in raw_results]
    inequality = [x['final_inequality'] for x in raw_results]
    with open("sorted_simul_dump.json", 'w') as sj:
        json.dump({"segregation": segregation, "bias": bias, "inequality": inequality}, sj)
 