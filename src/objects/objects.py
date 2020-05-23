import json

class CovidCase:
    def __init__(self, date, county, state, fips, cases, deaths):
        self.date = date
        self.county = county
        self.state = state
        self.fips = fips
        self.cases = cases
        self.deaths = deaths
