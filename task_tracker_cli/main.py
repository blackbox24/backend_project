import logging
import sys
import os
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(asctime)s %(message)s")
logger = logging.getLogger(__name__)

logger.info("Logging started")
logger.info(f"Filename: {sys.argv[0]}")
logger.info(f"command: {sys.argv[1]}")


# Model
class ListDataModel:
    id:int = 0
    description:str
    status:str 
    createdAt:datetime
    updatedAt:datetime

    def __init__(self,description="",status="mark in progress",id=None):
        if id == None:
            self.description = description
            self.status = status
            self.createdAt = str(datetime.now())
            self.updatedAt = str(datetime.now())
        else:
            self.updatedAt = datetime.now()
    
    def load_data(self):
        try:
            file = open("data.json","+r")
            data = json.load(fp=file)
            file.close()

            logger.info("Data loaded successfully")
            logger.info(f"Data: {data}")

            file = open("data.json","w+")


        except json.decoder.JSONDecodeError as e:
            logger.warning(str(e))
            data = []
        return data,file
    
    def save(self,data,file):
        
        data.append({
            "id":self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        })
        
        json.dump(data,fp=file)

        file.close()
        return data

    # Add items in list
    def add(self,description):
        try:
            # auto increment
            data, file = self.load_data()
            self.id = len(data) + 1
            self.description = description
            self.status = "mark in progress"
            self.createdAt = str(datetime.now())
            self.updatedAt = str(datetime.now())

            self.save(data,file)
        except json.decoder.JSONDecodeError:
            logger.warning("File is empty .. writing")
            

    def update(self,id,description):
        logger.info(f"data updated id:{id} to {description}")

    def delete(self,id):
        logger.info(f"data deleted id:{id}")

    def mark_in_progress(self):
        logger.info("status set to mark in progress")

    def mark_done(self):
        logger.info("status as to done")


if "__main__" == __name__:
    # command 
    command = sys.argv[1]
    options = sys.argv[2:]
    if command == "add":
        model = ListDataModel(description=options[0])
        model.add(description=options[0])
    # elif command == "update":
    #     update(options)
    # elif command == "delete":
    #     delete(options)
    # elif command == "mark-in-progress":
    #     mark_in_progress()
    