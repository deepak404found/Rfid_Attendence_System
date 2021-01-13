import requests

def sendMsg(name):
    Message = "welcome " + name + " sir! Your Attendance Added" # our Welcome message 

    # This API is for send message by our Telegram BOT
    link = 'Your API Token Link=\"'+Message + '\"'
    r =  requests.get(link)