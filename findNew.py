import telethon_helpers as th
from telethon.tl.types import PeerChannel, PeerChat, PeerUser
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon import functions
import sys
import pandas as pd
import time
import os.path

if len(sys.argv) > 3:
    search_file_name = sys.argv[1]
    known_file_name = sys.argv[2]
    blacklist_file_name = sys.argv[3]
else:
    print("Please append keyword filename and CSV filenames for known and blacklisted entities! Terminating!")
    sys.exit()

seperator = input("enter CSV seperator character:")

from pathlib import Path

if not os.path.isfile(known_file_name):
    known_df = pd.DataFrame(columns=['tgid','name','title','about','search','count','link','group','channel'])
else:
    try:
        known_df = pd.read_csv(known_file_name, encoding='utf-8', sep=seperator)
    except Exception as e:
        print(e)
        sys.exit()

if not os.path.isfile(blacklist_file_name):
    blacklist_df = pd.DataFrame(columns=['tgid','name','title','about','search','count','link','group','channel'])
else:
    try:
        blacklist_df = pd.read_csv(blacklist_file_name, encoding='utf-8', sep=seperator)
    except Exception as e:
        print("Error with blacklist_file_name")
        print(e)
        sys.exit()

try:
    search_phrases = open(search_file_name, mode="r", encoding="utf-8")
except Exception as e:
    print("Error with search file")
    print(e)
    sys.exit()

client = th.get_client()

new_entities = []
phrases = search_phrases.readlines()
phrases = list(dict.fromkeys(phrases))#remove duplicates
for phrase in phrases:
    phrase = phrase.rstrip("\n")
    print(phrase)
    result = client(functions.contacts.SearchRequest(
        q=phrase,
        limit = 200
    ))
    #print(result.stringify())
    for entity in result.results:
        if type(entity) is PeerChannel:
            if entity.channel_id in list(known_df['tgid']) or entity.channel_id in list(blacklist_df['tgid']):
                continue
            full = client(GetFullChannelRequest(channel=entity))
            #print(full.stringify())
            time.sleep(3.0)
            new_entities.append({
                'tgid':entity.channel_id,#full.full_chat.id
                'name':str(full.chats[0].username),
                'title':str(full.chats[0].title).replace(';', ' '),
                'about':str(full.full_chat.about).replace(';', ' ').replace('\n',' '),
                'search': phrase,
                'count': str(full.full_chat.participants_count),
                'link':"https://t.me/"+str(full.chats[0].username),
                'group': 1 if full.chats[0].megagroup else 0,
                'channel': 1 if full.chats[0].broadcast else 0,
            })


for entity in new_entities:
    print("----------------------------")
    print("["+str(entity['tgid'])+"|"
        +entity['name']+"|"
        +entity['title']+"|"
        +str(entity['count'])+"|"
        +str(entity['group'])+"|"
        +str(entity['channel'])+"|"
        +entity['link']+"]")
    print(entity['about'])
    #imgdata = base64.b64decode(entity['image'])
    #image = Image.open(io.BytesIO(imgdata))
    while True:
        if entity['tgid'] in list(known_df['tgid']) or entity['tgid'] in list(blacklist_df['tgid']):
            break
        choice = input("(n)ew, (b)lacklist or (i)gnore?: ")
        if choice == 'n':
            entity['category'] = input("enter category: ")
            #entity['location'] = input("enter location: ")
            #del entity['about']
            known_df = pd.concat([known_df, pd.DataFrame.from_dict([entity])], ignore_index = True)
            known_df.to_csv(known_file_name, sep=';', encoding='utf-8', index=False)
            break
        if choice == 'b':
            del entity['about']
            blacklist_df = pd.concat([blacklist_df, pd.DataFrame.from_dict([entity])], ignore_index = True)
            blacklist_df.to_csv(blacklist_file_name, sep=';', encoding='utf-8', index=False)
            break
        if choice == 'i':
            print("ignore")
            break
        else:
            print("wrong input")