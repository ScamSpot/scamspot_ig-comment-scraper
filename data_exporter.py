'''
Converts the json file to a csv file, ready to be used to train the model.
'''
import json

filename = 'comments-rating.json'

# read dictionary from json file
with open(filename, 'r', encoding='utf-8') as infile:
    comments = json.load(infile)

i = 0

# loop through all comments
for comment in comments:
    type = comments[comment]['type']
    
    # if type is 'scam' set type to 1, if type is 'real' set type to 0
    if type == 'scam':
        type = 1
    elif type == 'real':
        type = 0
    else:
        continue
    

    if type == 0 or type == 1:
        text = comments[comment]['text']
        text = text.replace('\n', ' ')
        text = text.replace(',', '.')
        
        # append line to csv file
        with open('comments-rating.csv', 'a', encoding='utf-8') as outfile:
            # number, spam, msg_length, msg
            outfile.write(str(i) + ',' + str(type) + ',' + str(len(text)) + ',' + text + '\n' )
