'''
Small CLI tool to annotate comments as scam or real.
'''

import json
import keyboard
from time import sleep
import os
import msvcrt
import webbrowser
import io
from PIL import Image
import urllib.request
import PIL
print("Starting") 


import numpy as np
import matplotlib.pyplot as plt
old_url = ""
plt.ion()

filename = 'data/comments_extracted.json'

# read dictionary from json file
with open(filename, 'r', encoding='utf-8') as infile:
    comments = json.load(infile)

i = 0
text_just_shown = ""

# loop through all comments
for comment in comments:

# endless loop
#while True:

    # choose a random comment
    #comment = np.random.choice(list(comments.keys()))

    # if the comment is not yet rated
    if comments[comment]['type'] == "unknown": # and "#" in comments[comment]['text']:
        os.system('cls')
        
        url = comments[comment]['url']
        if url != old_url:
            print('-- @' + comments[comment]['account'] + ' --')
            
            # a = np.array(PIL.Image.open(urllib.request.urlopen(url)))
            
            a = np.array(PIL.Image.open('data/images/' + comments[comment]['media'] + '.jpg'))
            plt.imshow(a)
            plt.show()
            
            plt.pause(0.1)
            plt.clf()
            
            old_url = url

        #print("Just rated: ", text_just_shown)
        
        text = comments[comment]['text']
        print("@", comments[comment]['user'], text)
        text_just_shown = text
      
        while True:
            print('\nIs this a scam message? y/n')
            ch = msvcrt.getch()
            if ch in b'\x00':
                ch = msvcrt.getch()
            if ch == b'\x1b' or ch == b'\x03' or ch == b'q':
                print('Stopping..')
                exit()
            if ch == b'y':
                print("Scammer!")
                comments[comment]['type'] = "scam"
                break
            if ch == b'n' or ch == b'\r':
                print("Good comment")
                comments[comment]['type'] = "real"
                break
            else:
                print(f'Invalid key pressed: {ch}')
        
        i += 1

        
        # save only after every 10th comment to reduce loading time
        if i > 10:
            #save the comments to a json file with utf-8 encoding
            with open(filename, 'w', encoding='utf-8') as outfile:
                json.dump(comments, outfile, indent=4, ensure_ascii=False)
            
            i = 0