# Telegram semiautomatic search
Search for Telegram Groups and Channels using a List of Keywords

# Usage
## initial
- create a telegram application with your tg account: https://core.telegram.org/api/obtaining_api_id
- insert your telegram api credentials into credentials.json
- optional: create an environment
- install requirements: `pip install -r requirements.txt`
- create a txt-file with your search terms

## the script
`python ./findNew.py searchterms.txt found-channels.csv blacklist.csv`
- searchterms.txt is the textfile containing the searchterms
- found-channels.csv is a filename for your channel-collection, it will be created when not existing
- blacklist.csv is a filename of excluded channels, it will be created when not existing

The script searches for each search term via the api 
The search results are then cleansed of duplicates, already known entries and entries from the blacklist.
Remaining search results are presented individually and can be added to the collection (a), referred to the blacklist (b) or ignored (i)
