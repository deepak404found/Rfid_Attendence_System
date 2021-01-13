from flask import Flask, json #pip isntall flask
from datetime import date, datetime 
from pymongo import MongoClient #pip install pymongo
import xlsxwriter #pip install xlsxwriter
from teleBot import * # import teleBot and access your Telegram BOT

#connecting to our data base
client = MongoClient('Your MongoDB token.')
mydatabase = client['Data Base name.']
myCollection = mydatabase["Collection Name."]

app = Flask(__name__)

filename = "Attendence.json"

# user's recents time data
recents = {"UID":"time"}

#user's data
users = [
    {
    "name":"Deepak Yadu",
    "UID":"138213210128",
    "emailID":"deepak@oceanparrot.com",
    },
    {
    "name":"Aman Singh",
    "UID":"10224920441",
    "emailID":"aman@oceanparrot.com",
    }
]

#connected devices
devices =['dev101', 'dev102', 'dev103', '1fc7f0bcf657e828',"2c4f3c61aa79d533"]

#this fuction converts our Attendence data to exlsheeet 
def addData():
    workbook = xlsxwriter.Workbook('Attendence.xlsx') # which is the filename that we want to create. 
    worksheet = workbook.add_worksheet() # worksheet via the add_worksheet() method. 
    now = datetime.now()

    allData = myCollection.find()
         
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    
    #Write some data headers.
    worksheet.write('A1', 'Time', bold)
    worksheet.write('B1', 'Name', bold)
    worksheet.write('C1', 'Email', bold)
    worksheet.write('D1', 'Uid', bold)

    row = 1
    # Some data we want to write to the worksheet. 
    for data in allData:
        
        # Start from the first cell. Rows and 
        # columns are zero indexed. 
        col = 0
        # Convert the date string into a datetime object.
        data['Time'] = (data['Time']).strftime("%d/%m/%Y %H:%M:%S")
        print(data["Time"])
        # Iterate over the data and write it out row by row. 
        keys = [x for x in data.keys()]
        for item in keys[1:]:
            values = data[item]
            #writing data in exlwrite
            worksheet.write_string(row, col, values)
            col += 1
        row += 1 

    workbook.close() 


@app.route('/')
def main():
    return "Connected! Hurray"

#taking entry after receive GET, POST request on our API
@app.route('/entry/<string:UID>/<string:DeviceID>', methods=['GET', 'POST'])
def entry(UID, DeviceID): 
    print(UID, DeviceID)  
    #checking DeviceID in our devices data 
    if DeviceID in devices :
        #checking user's UID in our user data
        for user in users:
            if user['UID'] == UID:
                print(recents)
                #checking user's recents entry time in our user's recents time data
                if UID in recents.keys():
                    print(recents[UID])
                    print((datetime.now() - recents[UID]).total_seconds())
                    #adding Attendence if user's recents entry time is less than 60 seconds
                    if (datetime.now() - recents[UID]).total_seconds() >= 60:
                        with open(filename, 'a') as file:
                            data = { 
                                "Time": now,
                                "Name": user['name'],
                                "Email": user['emailID'],
                                "UID" : user['UID']
                            }
                            json.dump(data, file)
                            file.write('\n')
                            file.close()
                        myCollection.insert_one(data) #inserting data on our MongoDB
                        addData() #calling addData function  
                        recents[UID] = datetime.now()  
                        sendMsg(user["name"]) #sending message to our telegram group
                        return "Attendance Added"
                    #if user's recents entry time is greater then 60 seconds, we return some message
                    else: 
                        return "Wait for some seconds"
                # if user is not in user's recents data then takeing new Attendence
                else:
                    with open(filename, 'a') as file:
                        now = datetime.now()
                        data = { 
                            "Time": now,
                            "Name": user['name'],
                            "Email": user['emailID'],
                            "UID" : user['UID']
                        }
                        json.dump(data, file)
                        file.write('\n')
                        file.close()
                    myCollection.insert_one(data)
                    addData()
                    recents[UID] = datetime.now() 
                    sendMsg(user["name"])   
                    return "Attendance Added"
        # if user's UID is not in our user's data
        else:
            return "Invalid UID detected"
    # if devices id is not in our devices data
    else:
          return "Invalid Device ID"

if __name__ == "__main__" :
    app.run(host="0.0.0.0", port=8888)