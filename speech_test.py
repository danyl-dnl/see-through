
import pyttsx3

# Initialize the speech engine
engine = pyttsx3.init()

# Set the speaking speed
engine.setProperty("rate", 150)

# Text that we want the computer to speak
engine.say("Hello! I am Vision Scribe. I can help you identify objects around you.")

# Speak the sentence
engine.runAndWait()
