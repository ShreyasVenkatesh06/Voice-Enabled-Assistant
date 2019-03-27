from gtts import gTTS
import speech_recognition as sr
import gtts
import os
import re
import webbrowser
import smtplib
import requests
import time
import pytemperature
from time import ctime
import vlc

def Message(audio):
    "Speak audio"

    print(audio)
    #for line in audio.splitlines():
        #os.system("espeak " + audio)

    #  tts = gTTS(text=audio, lang='en')
    #  tts.save('audio.mp3')
    #  os.system('mpg123 audio.mp3')


def myCommand():
    "Takes commands"

    sound = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready for your command')
        sound.pause_threshold = 1
        sound.adjust_for_ambient_noise(source, duration=1)
        audio = sound.listen(source)

    try:
        command = sound.recognize_google(audio).lower()
        print('You:'+command+'\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Bot: Your last command couldn\'t be heard')
        command = myCommand();

    return command


def assistant(command):
    "if statements for executing commands"
    if 'hello' in command:
    	Message('Bot: Hello, What can i do for you?')

    elif 'time' in command:
    	Message(ctime()) 

    elif 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        Message('Bot: Done!')

    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            Message('Bot: Done!')
        else:
            pass

    elif 'what\'s up' in command:
        Message('Bot: Just doing my thing')
    
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            Message('Bot: '+str(res.json()['joke']))
        else:
            Message('Bot: oops!I ran out of jokes')


    elif 'email' in command:
        Message('Who is the recipient?')
        recipient = myCommand()

        if 'Shreyas' in recipient:
            Message('What should I say?')
            content = myCommand()

            #init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)

            #identify to server
            mail.ehlo()

            #encrypt session
            mail.starttls()

            #login
            mail.login('youremail', 'yourpassword')

            #send message
            mail.sendmail('Shreyas', 'shreyou06@gmail.com', content)

            #end mail connection
            mail.close()

            Message('Email sent.')

    elif 'weather in' in command:
            api_address='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
            reg_ex = re.search('weather in (.*)', command)
            city = reg_ex.group(1)
            url = api_address + city
            json_data = requests.get(url).json()
            format_add = json_data['main']['temp']
            #print(format_add)
            x=pytemperature.k2c(format_add)
            Message(x)

    elif 'play music' in command:
        player = vlc.MediaPlayer("C:/Users/SHREYAS/Music/Green Day - Holiday.mp3")
        player.play()
            

    elif 'stop' in command:
        player.stop()
        
    else:
        Message('Bot: I don\'t know what you mean!')


Message('Bot: I am ready for your command')

#loop to continue executing multiple commands
while True:
    assistant(myCommand())
