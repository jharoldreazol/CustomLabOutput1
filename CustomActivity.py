import json
import time
import requests
from ncclient import manager

router = {"host": "10.10.20.48", "port": "830","username": "developer", "password": "C1sco12345"}
config_template = open("C:/Repositories/CustomLab/ios_config.xml").read()

access_token = "MzI1NDVhMzgtMTliMy00ODM5LTljMDMtMzk3ZTg0ZDU0NDU4MzUyODRkNzQtZjE3_P0A1_5d96674f-de50-43d7-ae6b-8071b71cb457"
room_id="Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vZjFkNWZjMTAtOTljMi0xMWViLTg5YWUtZmI4MDYxZDUxNmNm"
webex_url = 'https://webexapis.com/v1/messages'
webex_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
getMessagesUrlParameters={"roomId":room_id, "max":1}

flag=True
lastMessageId=None
while flag:
    time.sleep(0.1)
    r=requests.get(webex_url,params=getMessagesUrlParameters,headers=webex_headers)
    jsonData=r.json()
    messages=jsonData['items']
    message=messages[0]
    if(lastMessageId==message['id']):
        print("No new messages")
    else:
        print("New message:"+ message['text'])
        message_received=message['text']
        lastMessageId=message['id']
        if (message['text']=="Stop"):
            flag=False
        else:
            try:

                parsed_strings=message_received.split("/")
                int_name=parsed_strings[0]
                message=parsed_strings[1]
                netconf_config = config_template.format(interface_name=int_name, interface_desc=message)
                with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False) as m:
                    device_reply = m.edit_config(netconf_config, target="running")
                    print(device_reply)
                reply_message=int_name+ "'s Description has been changed to "+message
                params = {
                    "toPersonEmail": "reazoljayharold@gmail.com",
                    "text": reply_message
                    }
                res = requests.post(webex_url, data=json.dumps(params), headers=webex_headers, verify=False)
            except:
                print(message_received +" is invalid format")


                    
    