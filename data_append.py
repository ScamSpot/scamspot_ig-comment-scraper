import json

with open('data/comments_extracted.json', 'r', encoding='utf-8') as infile:
    comments = json.load(infile)
   
i = 0

# loop through all comments
print(len(comments))
for comment in comments:
    # skip unknown comments
    if comments[comment]['type'] == "unknown":
        continue
    
    scam = 0
    if comments[comment]['type'] == "scam":
        scam = 1
    
    text = comments[comment]['text']
    
    # remove potential user tag, check is the first character is @
    if text[0] == "@" and " " in text:
        # remove the first word
        print(text)
        text = text.split(" ", 1)[1]
        
    # replace illegal characters
    text = text.replace(',', ' ').replace('\n', ' ').replace('\r', ' ').replace('"', ' ').replace("'", ' ')
 

    # append line to csv file
    with open('data/comments-rated.csv', 'a', encoding='utf-8') as outfile:
        # number, scam, msg_length, msg
        outfile.write(str(i) + ',' + str(scam) + ',' + str(len(text)) + ',' + text + '\n' )

    i += 1
    
 
 
