from dataclasses import dataclass, field
import requests
import os
from random import choice

USER_AGENT = [
    r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
]

OUTPUT_DIR = "./daily_data/"

NYT_1 = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

NYT_2 = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

COVID_1 = "https://covidtracking.com/api/v1/states/daily.csv"

NYT_1_FP = "nyt_states.csv"

NYT_2_FP = "nyt_counties.csv"

COVID_1_FP = "covid_tracking.csv"

URLS = [NYT_1, NYT_2, COVID_1]

PATHS = [NYT_1_FP, NYT_2_FP, COVID_1_FP]

@dataclass
class Collector():
    urls: list 
    paths: list 
    output_dir = OUTPUT_DIR
    user_agents: list = None
    proxies: dict = None
    clear_dir: bool = True
    to_csv: bool = True
        
    def collect(self):
        
        self.prep()
        
        targets = zip(self.urls, self.paths)
        
        for url, path in targets:
            
            agent = self.random_agent()
            
            try:
                response = requests.get(url, headers = {

                "User-Agent" : agent

            },

                proxies = self.proxies)
            
                response.raise_for_status()

            except HTTPError:

                raise

            except RequestException:

                raise

            else:
                
                try:
                
                    with open(path, "wb") as f:

                        f.write(response.content)
                        
                except Exception as e:
                    
                    print("Could not collect {}: {}".format(url, e))
                    
        print("All data collected")
                
    def prep(self):
        
        if not os.path.exists(self.output_dir):
            
            os.makedirs(self.output_dir)
            
        if self.clear_dir:
            
            self.paths = [os.path.join(self.output_dir, path) for path in self.paths]
            
            for path in self.paths:
                
                try:
                    if os.path.isfile(path) or os.path.islink(path):
                        
                        os.unlink(path)
                        
                except Exception as e:
                    
                    print("Failed to delete {}: {}".format(path, e))
    
    def random_agent(self):
        
        if self.user_agents and isinstance(self.user_agents, list):
        
            return(choice(self.user_agents))

        return(choice(USER_AGENT))

if __name__ == "__main__":

    collector = Collector(URLS, PATHS)

    collector.collect()