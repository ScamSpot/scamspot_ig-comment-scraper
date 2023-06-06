print("Starting") 

import numpy as np
import json
import matplotlib.pyplot as plt

filename = 'data/comments.json'
filename_extracted = 'data/comments_extracted.json'

# read dictionary from json file
with open(filename, 'r', encoding='utf-8') as infile:
    comments = json.load(infile)

i = 1
comments_extracted = {}

# save the id of already extracted comments
extracted_ids = []

while i <= 3000:

    # choose a random comment
    comment = np.random.choice(list(comments.keys()))

    # if the comment is not yet rated
    if (comments[comment]['type'] == "unknown" or comments[comment]['type'] == "real") and comment not in extracted_ids:
        
        print(i, "@", comments[comment]['user'], comments[comment]['text'])

        # add the new comment to the dictionary comments_extracted
        comments_extracted[comment] = comments[comment]
        
        # add the id to the list of extracted ids
        extracted_ids.append(comment)
        i = i + 1            
      
       
print("Finished, now saving")
        
#save the comments to a json file with utf-8 encoding
with open(filename_extracted, 'w', encoding='utf-8') as outfile:
    json.dump(comments_extracted, outfile, indent=4, ensure_ascii=False)
    