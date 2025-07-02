import requests
import sys
import logging
import json


logging.basicConfig(level=logging.INFO,format="%(levelname)s %(filename)s %(message)s")
logger = logging.getLogger(__name__)

class GithubActivities:
    username = ""
    data = {}
    events = ""

    # def __init__(self,username=""):
    #     self.username = username
            

    def __doc__(self):
        file = open("docs.txt","r")
        docs = file.read()
        logger.info(f"Documentation:\n{docs}")
        file.close()
        return 0;

    def make_request(self):
        response = requests.get(f"https://api.github.com/users/{self.username}/events")
        if response.status_code == 200:
            logger.info(f"Status code: {response.status_code}")
            logger.info(f"Successfully retreive {username} events")
            self.events = response.json()
    
        elif response.status_code == 404:
            logger.error(f"Status code: {response.status_code}")
            logger.error(f"Username cannot be found {self.username}")
            sys.exit()
            
        else:
            logger.error(f"Status code: {response.status_code}")
            logger.error("Unable to retreive information")
            sys.exit()

    def all_events(self):
        # logger.info(f"Retreive all events:\n{self.data}")
        return self.events

    def filter_event(self,by_type=""):
        results = []
        logger.info(f"Filtering type by {by_type}")
        for x in self.events:
            if x["type"] == by_type:
                results.append(x)

        return results


if "__main__" ==  __name__:
    github_activity = GithubActivities()
    
    try:
        username = sys.argv[1]  
        github_activity.username = username
        github_activity.make_request()

        if len(sys.argv) > 2:
            command = sys.argv[2]
            option = sys.argv[3]

            if command == "filter":
                results = github_activity.filter_event(option)
                logger.info(f"Data: {results}")
        else:
            results = github_activity.all_events()
            logger.info(f"Data: {results}")


    except IndexError as e:
        logger.error(e)
        github_activity.__doc__()

    except:
        logger.error("Unable to make api call")
        raise

    