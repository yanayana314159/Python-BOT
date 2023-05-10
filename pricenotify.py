from calendar import SATURDAY
import requests
import json
from datetime import datetime
today = datetime.now()
hour = today.hour
url="https://www.gaitameonline.com/rateaj/getrate"
list=[]
dict={}
path="former.txt"
def SendToDiscord(Sentcontents):
  webhook_url = ''
 
  main_content = {
    "content": Sentcontents
    }
  requests.post(webhook_url,main_content)

with open(path) as f:
    str_data=f.read()
    price=json.loads(str_data)

def mainroot():
    try:
        data=requests.get(url) 
        data=data.json()
        essense=data["quotes"]
        for i in range(len(data["quotes"])):
            if (essense[i]["currencyPairCode"]=="USDJPY"):
                dict["USDJPY"]=essense[i]["bid"]
            if (essense[i]["currencyPairCode"]=="GBPJPY"):
                dict["GBPJPY"]=essense[i]["bid"]



        usddiff=round(float(dict["USDJPY"])-float(price["USDJPY"]),2)
        gbpdiff=round(float(dict["GBPJPY"])-float(price["GBPJPY"]),2)
        print(usddiff,gbpdiff)
        text=f"USDJPY:{usddiff*100}pips GBPJPY:{gbpdiff*100}pips"
        if (abs(usddiff*100>=20)) or (abs(gbpdiff*100>=20)) :
            senttext="大きな変動があったよ！\n"+text
        else:
            senttext=text+"\n10minutes"
        SendToDiscord(senttext)
    #ディスコードに通知後、書き込む
        with open(path,mode="w") as p:
            p.write(json.dumps(dict))
    
    except Exception as e:
        print("エラーです")

def main():
    if (hour>=20) and (today.strftime("%A")=="Friday"):
        print("おやすみです")
    elif today.strftime("%A")=="Saturday":
        print("おやすみです")
    elif (hour<=20) and (today.strftime("%A")=="Sunday"):
        print("おやすみです")
    else:
        mainroot()

# print(today.strftime("%A"))



if __name__ == "__main__":
    main()
