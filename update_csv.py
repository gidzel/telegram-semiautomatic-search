import telethon_helpers as th
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputChannel
from telethon.errors.rpcerrorlist import ChannelPrivateError
import pandas as pd
import sys
from numpy import int64
import numpy as np
import time

if len(sys.argv) > 1:
    entities_file_name = sys.argv[1]
else:
    print("Please append CSV filenames for entities! Terminating!")
    sys.exit()

seperator = ';'#input("enter CSV seperator character:")

client = th.get_client()
creds = th.get_creds()

try:
    entities_df = pd.read_csv(entities_file_name, encoding='utf-8', sep=seperator)
except Exception as e:
    print(e)
    sys.exit()

entities_df = entities_df.drop_duplicates(subset=['name'])

if 'access_hash' not in entities_df.columns:
    entities_df['access_hash'] = np.nan

if 'about' not in entities_df.columns:
    entities_df['about'] = ""

pd.options.display.float_format = '{:,.0f}'.format

for index, row in entities_df.iterrows():
    #entity = th.get_entity(client, row['name'])
    entity = None
    # if pd.notna(row['access_hash']):
    #     entity = client(GetFullChannelRequest(InputChannel(int("{0:.0f}".format(row['tgid'])), int("{0:.0f}".format(row['access_hash'])))))
    #     if row['tgid'] != creds["api_id"]:
    #         print("API ID MISMATCH! check credentials.json!")
    # else:
    try:
        entity = client(GetFullChannelRequest(row['name']))
    except ChannelPrivateError as e:
        print(row['name'], " is private")
        #continue
    except ValueError as e:
        print(e)
        #continue
    time.sleep(3.1)
    if entity:
        #member_count = th.get_participants_count(client, row['name'])
        #time.sleep(3.1)
        print("update "+row['name'])
        entities_df.loc[index,'name'] = str(entity.chats[0].username)
        entities_df.loc[index,'tgid'] = "{0:.0f}".format(int(entity.full_chat.id))
        entities_df.loc[index,'count'] = "{0:.0f}".format(int(entity.full_chat.participants_count))
        entities_df.loc[index,'link'] = 'https://t.me/'+str(entity.chats[0].username)
        entities_df.loc[index,'title'] = str(entity.chats[0].title)
        entities_df.loc[index,'access_hash'] = "{0:.0f}".format(int(entity.chats[0].access_hash))
        entities_df.loc[index,'api_id'] = creds["api_id"]
        entities_df.loc[index,'about'] = str(entity.full_chat.about).replace(';','').replace('\n',' ')
        #entities_df.loc[index,'location'] = "DE"
        if entity.chats[0].broadcast:
            entities_df.loc[index,'group'] = 0
            entities_df.loc[index,'channel'] = 1
        else:
            entities_df.loc[index,'group'] = 1
            entities_df.loc[index,'channel'] = 0

        entities_df.to_csv(entities_file_name+".csv", sep=';', encoding='utf-8', index=False, float_format='%.0f')
        #time.sleep(3.1)
    else:
        print("delete "+row['name'])
        entities_df.drop(index, inplace=True)

print("length: "+str(len(entities_df.index)))
entities_df = entities_df.drop_duplicates(subset=['tgid'])
print("length after drop_duplicates: "+str(len(entities_df.index)))
entities_df.to_csv(entities_file_name+".csv", sep=';', encoding='utf-8', index=False, float_format='%.0f',columns = ['name','location','category','count','tgid','link','title','group','channel','access_hash','about','api_id','diff'])