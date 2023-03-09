print('Hello World')

from playsound import playsound 
from core.textToSpeech import Speak


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

test = Speak(words)

test.speech()

# Print the list of words
print(words)
print(len(words))
#ps.playsound("audio/ikaw.wav")

