def get_creds():
    import json
    try:
        f = open('credentials.json')
        creds = json.load(f)
        return creds
    except Exception as e:
        print(e)
        return None

def get_client():
    from telethon.sync import TelegramClient

    creds=get_creds()
    if creds == None:
        return None

    if all (k in creds for k in ("phone","api_id", "api_hash")):
        client = TelegramClient(creds["phone"], creds["api_id"], creds["api_hash"])#, proxy=("socks5", '127.0.0.1', 9150))
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(creds["phone"])
            client.sign_in(creds["phone"], input('Enter the code: '))
        return client
    else:
        print("credentials.json is wrong")
        return None

def get_group_participants(client, group_name, wait=False):
    from telethon.tl.functions.channels import GetParticipantsRequest
    from telethon.tl.types import ChannelParticipantsSearch
    import time
    from random import randrange
    limit = 200
    exitWhile = False
    offset = 0
    all_participants = []
    try:
        group = client.get_entity(group_name)
        time.sleep(3.0)
        if group:#Todo: check for Channel? or Supergroup?
            while not exitWhile:
                try:
                    participants = client(GetParticipantsRequest(channel=group, filter=ChannelParticipantsSearch(''), offset=offset, limit=limit, hash=0))
                    if wait:
                        time.sleep(3.0)
                    all_participants.extend(participants.users)
                    offset += limit
                    if len(participants.users) < limit:
                        exitWhile = True
                except Exception as e:
                    print("error getting group: "+ str(e))
                    return None, None
    except Exception as e:
        print("error getting group: "+ str(e))
        return None, None

    return group, all_participants

def get_channel_messages(client, channel_name, wait=False):
    import time
    from random import randrange
    limit = 10
    try:
        channel = client.get_entity(channel_name)
        time.sleep(3.0 + randrange(20)/10)
        if channel:#Todo: check for Channel? or Supergroup?
            for message in client.iter_messages(channel):
                if not limit:
                    return
                limit -= 1
                print(message)
                if wait:
                    time.sleep(3.0 + randrange(20)/10)
    except Exception as e:
        print("error getting group: "+ str(e))

    return

def get_fwd_channel_messages(client, channel_name, limit=1, wait=False):
    import time
    from random import randrange
    from telethon import errors
    messages = []
    try:
        channel = client.get_entity(channel_name)
        time.sleep(3.0 + randrange(20)/10)
        if channel:#Todo: check for Channel? or Supergroup?
            try:
                with client.takeout() as takeout:
                    for message in client.iter_messages(channel):
                        if not limit:
                            continue
                        if message.fwd_from is not None:
                            if len(messages) and message.grouped_id == messages[-1].grouped_id:
                                messages[-1] = message
                            else:
                                messages.append(message)
                                limit -= 1
                        if wait:
                            time.sleep(3.0 + randrange(20)/10)
            except errors.TakeoutInitDelayError as e:
                print('Must wait', e.seconds, 'before takeout')
    except Exception as e:
        print("error getting group: "+ str(e))
        return None, None

    return channel, messages

def get_entity(client, id):
    try:
        entity = client.get_entity(id)
        return entity
    except Exception as e:
        print("error getting entity: "+ str(e))
        return None

def get_participants_count(client, name):
    try:
        return client.get_participants(name, limit=0).total
    except Exception as e:
        print("error getting count: "+ str(e))
        return None