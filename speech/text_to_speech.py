import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
    # converts text to voice  if successful returns code 1 else 0
    def convert(self,answer):
        self.engine.setProperty("rate",95)
        self.engine.say(answer)
        if self.engine.runAndWait():
            return 1
        else:
            return 0
if __name__ == '__main__':
    t = TextToSpeech()
    t.convert("welcome everyone,my name is Shambhavi")
