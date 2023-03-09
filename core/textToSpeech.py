from playsound import playsound

class Speak:
  def __init__(self, words):
    self.words = words

  def speech(self):
    print("helo")
    for x in self.words:
      print(x)
      playsound("audio/"+ x + ".mp3")
