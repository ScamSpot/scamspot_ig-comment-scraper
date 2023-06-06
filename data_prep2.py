import json
import unicodedata

import modules.helper as helper

# load the extracted comments
with open('data/comments_extracted.json', 'r', encoding='utf-8') as infile:
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
    # type_c = "unknown"
    
    
    if type_c == "unknown":
        # check for fancy font characters
        status, text = helper.remove_fancy_font(text)
        if status:
            #type_c = "scam"
            print("found fancy font: ", text)
            
        # check for common spam phrases
        status = helper.check_for_spam_phrases(text)
        if status:
            print("found spam phrase: ", text)
            type_c = "scam"
            
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
with open('data/comments_extracted.json', 'w', encoding='utf-8') as outfile:
    json.dump(comments, outfile, indent=4, ensure_ascii=False)


print("real: ", real)
print("scam: ", scam)
print("ignore: ", ignore)
print("unknown: ", unknown)
    
