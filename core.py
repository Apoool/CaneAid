print('Hello World')

import playsound as ps
import time

with open("test.txt", "r") as f:
    content = f.readlines()

# Create a list to store the words
words = []

# Iterate over each line in the file
for line in content:
    # Remove any whitespace or newline characters
    word = line.strip()
    # Add the word to the list
    words.append(word)

# Print the list of words
print(words)
print(len(words))
ps.playsound("audio/ako.mp3")
#ps.playsound("audio/ikaw.wav")

#TRY RECURSION