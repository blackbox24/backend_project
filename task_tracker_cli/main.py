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

    def __init__(self,description="",status="not done",id=None):
        if id == None:
            self.description = description
            self.status = status
            self.createdAt = str(datetime.now())
            self.updatedAt = str(datetime.now())
        else:
            self.updatedAt = datetime.now()

    def __doc__(self):
        doc = open("docs.txt","r")
        _help = doc.read()
        doc.close()
        logger.info(f"Documentation\n{_help}")

    def load_data(self):
        try:
            file = open("data.json","+r")
            data = json.load(fp=file)
            file.close()

            logger.info("Data loaded successfully")

        except json.decoder.JSONDecodeError as e:
            logger.warning(str(e))
            data = []
        return data

    def write_data(self):
        file = open("data.json","w+")
        return file
    
    def save(self,data,file,update=None):
        if update == None:
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
            data = self.load_data()
            file = self.write_data()
            self.id = len(data) + 1
            self.description = description
            self.status = "not done"
            self.createdAt = str(datetime.now())
            self.updatedAt = str(datetime.now())

            self.save(data,file)
        except json.decoder.JSONDecodeError:
            logger.warning("File is empty .. writing")
        
        except ValueError as e:
            logger.error(e)
            

    def all(self):
        data = self.load_data()
        return data
    
    def filter(self,status=""):
        data = self.load_data()
        result = []

        for dict_ in data:
            if dict_["status"] == status:
                result.append(dict_)

        return result
    
    def update(self,id,description):
        data = self.load_data()
        arr_index = 0
        while arr_index < len(data):
            if data[arr_index]["id"] == int(id):
                logger.info(f"Get id: {id}")
                data[arr_index]["description"] = description

                file = self.write_data()
                self.save(data,file,update=True)
                logger.info(f"Data updated id:{id} to {description} successfully")
                break
            
            arr_index += 1
        

    def delete(self,id):
        data = self.load_data()
        arr_index = 0
        while arr_index < len(data):
            if data[arr_index]["id"] == int(id):
                del data[arr_index]
                file = self.write_data()
                self.save(data,file,update=True)
                logger.info(f"Data deleted id:{id} successfully")
                break
            
            arr_index += 1

    def mark_in_progress(self,id):
        data = self.load_data()
        arr_index = 0
        while arr_index < len(data):
            if data[arr_index]["id"] == int(id):
                data[arr_index]["status"] = "mark in progress"
                file = self.write_data()
                self.save(data,file,update=True)
                logger.info(f"Data at id:{id} marked in progress")
                break
            
            arr_index += 1

    def mark_done(self,id):
        data = self.load_data()
        arr_index = 0
        while arr_index < len(data):
            if data[arr_index]["id"] == int(id):
                data[arr_index]["status"] = "mark in progress"
                file = self.write_data()
                self.save(data,file)
                logger.info(f"Data at id:{id} marked as done")
                break
            
            arr_index += 1


if "__main__" == __name__:
    # command 
    model = ListDataModel()
    command = sys.argv[1]
    options = sys.argv[2:]
    if command == "add":
        try:
            
            model.add(description=options[0])
        except IndexError as e:
            logger.error("python main.py add [description]")

    elif command == "list":
        try:
            
            if len(options) >= 1:
                logger.info(f"Filter by {options[0]}: {model.filter(status=options[0])}")
            else:
                logger.info(f"Data: {model.all()}")
        except IndexError as err:
            logger.error(err)

    elif command in ["help","?"]:
        model.__doc__()

    elif command == "update" and len(options) == 2:
        id = options[0]
        description = options[1]
        model.update(id=id,description=description)

    elif command == "delete" and len(options) == 1:
        model.delete(options[0])
        
    elif command == "mark-in-progress" and len(options) == 1:
        model.mark_in_progress(options[0])

    elif command == "mark-done" and len(options) == 1:
        model.mark_in_progress(options[0])

    else:
        model.__doc__()
        
    # elif command == "update":
    #     update(options)
    # elif command == "delete":
    #     delete(options)
    # elif command == "mark-in-progress":
    #     mark_in_progress()
    