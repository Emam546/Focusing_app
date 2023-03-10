import threading
import pyttsx3

def _sayer():
    while len(speakings)>0:
        for text in speakings:
            tts_engine = pyttsx3.init()
            tts_engine.say(text)
            tts_engine.runAndWait()
            speakings.remove(text)
speakings=[]
def say(text):
    if len(speakings)==0:
        speakings.append(text)
        threading.Thread(target=_sayer,daemon=True).start()
    else:
        speakings.append(text)
if __name__=="__main__":
    say("yes i am in")
    say("hey")
    say("yes i am in")
    say("hey")



