from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO,format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)

class Expense:
    description = ""
    amount = 0
    date = str(datetime.now())

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
        count = 0
        logger.info("Data: ")
        while count < len(results):
            print(f"{results[count]["id"]} {results[count]["date"]} {results[count]["description"]} {results[count]["amount"]}")
            count += 1
            

    def create(self):
        data = self.read_file()
        logger.info(data)
        file = self.write_file()
        data.append({
            "id":len(data)+ 1,
            "date": self.date,
            "description": self.description,
            "amount": self.amount,
        })
        json.dump(data,fp=file)
        logger.info("Successfull created expense id: "+str(len(data)+1))
    
        file.close()
    
    def update(self,id,description="",amount=0):
        data = self.read_file()
        count = 0
        while count < len(data):
            if id == data[count]["id"] and description != "" and amount != 0:                
                file = self.write_file()
                data[count]["description"] = self.description
                data[count]["amount"] = self.amount
                json.dump(data,fp=file)
                file.close()
                logger.info("Successfull updated expense description and amount at id: "+str(id))

                break
            elif id == data[count]["id"] and description != "":            
                file = self.write_file()
                data[count]["description"] = self.amount
                json.dump(data,fp=file)
                file.close()
                logger.info("Successfull updated expense description at id: "+str(id))
                break
            elif id == data[count]["id"] and amount != 0:            
                file = self.write_file()
                data[count]["amount"] = self.amount
                json.dump(data,fp=file)
                file.close()
                logger.info("Successfull updated expense amount at id: "+str(id))
                break
            

            count += 1

        
    
    def delete(self,id):
        data = self.read_file()
        count = 0
        while count < len(data):
            if id == data[count]["id"]:
                del data[count]
                file = self.write_file()
                json.dump(data,fp=file)
                file.close()
                logger.info("Successfull delete expense at id: "+str(id))
                break
            count += 1
    
    def summary(self,filter=""):
        try:
            data = self.read_file()
            total_expense = 0
            count = 0
            if filter == "":
                while count < len(data):
                    total_expense += data[count]["amount"]
                    count += 1
                logger.info(f"Total Expenses: {total_expense}")
            elif filter != "":
                while count < len(data):
                    date, ___ = data[count]["date"].split(" ")
                    # logger.info("Date: "+date)
                    __,month,_= date.split("-")
                    # logger.info(f"Month: {int(month)}")
                    if int(month) == filter:
                        total_expense += data[count]["amount"]
                    count += 1
                logger.info(f"Total Expenses for month: {filter}: ${total_expense}")
        except:
            logger.error("Failed to get summary")
            raise
        
        

