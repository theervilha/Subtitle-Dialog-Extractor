from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup

from settings import *

encoding = "iso-8859-1"# if it doesn't works, try it with "utf-8" too
with open(f'{filename}.srt', 'r', encoding=encoding) as file:
    lines = file.read().splitlines() 

def getMessagesAndtimeStamp(lines):
    data = {'messages': [], 'timeStamp':[]} 
    i = 1
    messagesByIndex = []
    while i < len(lines[1:]): 
        line = lines[i] 
        if ' --> ' in line: 
            data['timeStamp'].append(line) 
            i += 1 
            continue 
        elif line == '':
            message = ' '.join(messagesByIndex)
            messagesByIndex = []
            data['messages'].append(message) 
            i += 2 
            continue 
        messagesByIndex.append(line) 
        i += 1 

    return data

def getMessagesSplitedByDot(data):
    newData = {'message': [], 'timeStamp': []}
    messageWithoutPoint = '' 
    for i, msg in enumerate(data['messages']): 
        if '.' in msg and '...' not in msg:
            messageWithoutPoint += msg 

            endTime = data['timeStamp'][i].split(' -->')[1]
            timeStamp = f'{initTime} --> {endTime}'

            messageWithoutPoint = cleanText(messageWithoutPoint)
            newData['message'].append(messageWithoutPoint) 
            newData['timeStamp'].append(timeStamp) 
            messageWithoutPoint = '' 
        else: 
            if messageWithoutPoint == '':
                initTime = data['timeStamp'][i].split(' -->')[0]
            messageWithoutPoint += msg + ' ' 

    return newData

def cleanText(text):
    text = BeautifulSoup(text, features="html.parser").text
    text = text.lower()
    return text

def getMessagesWithinEachDelta(data, interval=5, maxlength=500):
    messages = []
    for i, (subtitle, time) in enumerate(zip(data['message'], data['timeStamp'])):
        timeInit = time.split(' -->')[0]
        if messages == []:
            initTimeConversation = timeInit
        message = cleanText(subtitle)
        messages.append(message)

        datetimeInit = datetime.strptime(timeInit, "%H:%M:%S,%f")
        try:
            nextStartTime = data['timeStamp'][i+1].split(' -->')[0]
        except IndexError: # last line
            nextStartTime = timeInit
        datetimeNextStartTime = datetime.strptime(nextStartTime, "%H:%M:%S,%f")
        delta = (datetimeNextStartTime - datetimeInit).total_seconds()

        if delta > interval:
            timeEnd = time.split(' -->')[1]
            timeStamp = f'{initTimeConversation} --> {timeEnd}'

            strMessages = ' '.join(messages)
            if len(strMessages.split()) <= maxlength:
                yield {'index_name': filename, 'items': strMessages, 'timeStamp': timeStamp}
            messages = []


data = getMessagesAndtimeStamp(lines)
data = getMessagesSplitedByDot(data)
data = getMessagesWithinEachDelta(data, interval=max_interval_without_dialog)

df = pd.DataFrame(data)
df.to_csv(f'{filename}_subtitles.csv', index=False, sep=';', encoding='utf-8')
