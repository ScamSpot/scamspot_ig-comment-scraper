import json
import unicodedata

import modules.helper as helper

# load the extracted comments
with open('data/comments.json', 'r', encoding='utf-8') as infile:
    comments = json.load(infile)

real = 0
scam = 0
ignore = 0
unknown = 0

# loop through all comments
for comment_id in comments:
    comment = comments[comment_id]
    text = comment["text"]

    type_c = comment["type"] # real, scam, ignore
        
    # if account and username are the same, remove the message
    if comment["account"] == comment["user"]:
        type_c = "ignore"
        
    # remove all emojis from the comments 
    status, temp = helper.remove_emojis(text)
    if status:
        # print("found emoji: ", text)
        type_c = "real"
    
    # check for fancy font characters
    status, text = helper.remove_fancy_font(text)
    if status:
        print("found fancy font: ", text)
        #type_c = "scam"
    
    # make all text lowercase
    text = text.lower()
    
    # remove double spaces, leading and trailing spaces
    text = text.strip().replace("\n", " ").replace("   ", " ").replace("  ", " ")
    
    # ignore comments shorter than 2 characters
    if len(text) < 1:
        #type_c = "ignore"
        print("short comment: ", text)
            
    if type_c == "scam":
        scam += 1
    elif type_c == "real":
        real += 1
    elif type_c == "ignore":
        ignore += 1
    else:
        unknown += 1

    # add the new comment to the dictionary
    comment["text"] = text
    comment["type"] = type_c


# save the comments
with open('data/comments.json', 'w', encoding='utf-8') as outfile:
    json.dump(comments, outfile, indent=4, ensure_ascii=False)


print("real: ", real)
print("scam: ", scam)
print("ignore: ", ignore)
print("unknown: ", unknown)
    
