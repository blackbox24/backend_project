import json
import logging

logging.basicConfig(level=logging.INFO,format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)

class Expense:
    description = ""
    amount = ""

    def __init__(self,description="",amount=0):
        self.description = description
        self.amount = amount

    def read_file(self):
        results = []
        try:
            file = open("data.json","r")
            results = json.load(fp=file)
            file.close()
        except FileNotFoundError as e:
            logger.error(e)
        except json.decoder.JSONDecodeError as e:
            logger.error(e)
        except:
            logger.error("Unable to read file")
            raise
        return results
    
    def write_file(self):
        file = open("data.json","w+")
        return file
    
    def get_all(self):
        results = self.read_file()
        if results != None:
            return results

    def create(self):
        data = self.read_file()
        logger.info(data)
        file = self.write_file()
        data.append({
            "id":len(data)+ 1,
            "description": self.description,
            "amount": self.amount,
        })
        json.dump(data,fp=file)
        logger.info("Successfull created expense id: "+str(len(data)+1))
    
        file.close()