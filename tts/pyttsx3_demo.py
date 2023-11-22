import pyttsx3

# https://www.jb51.net/article/283155.htm
rate = 200  # 速率
volume = 0.9  # 音量

engine = pyttsx3.init()
engine.setProperty('rate', rate)
engine.setProperty('volume', volume)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # voices[1].id 是中文

engine.say("你好, 这段语音合成的效果如何?")

engine.runAndWait()
engine.stop()
