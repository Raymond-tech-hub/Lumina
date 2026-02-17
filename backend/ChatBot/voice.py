import pyttsx3

class Voice:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._rate = self.engine.getProperty("rate")     # default speed
        self._volume = self.engine.getProperty("volume") # default volume 0.0–1.0

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        """
        Set speaking speed. Typical range: 100-300
        """
        self._rate = value
        self.engine.setProperty("rate", self._rate)
        print(f"Speaking rate set to: {self._rate}")

    # --- Property: volume ---
    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        """
        Set volume between 0.0 and 1.0
        """
        self._volume = max(0.0, min(1.0, value))  # clamp value
        self.engine.setProperty("volume", self._volume)
        print(f"Volume set to: {self._volume}")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        print("engine spoke:", text)

if __name__ == "__main__":
    chat = Voice()

    chat.rate = 180

    chat.speak("Hello this is a voice chat from Lumina your AI tutor!, how may i be of assistant?")        

    engine = pyttsx3.init()
