from youtube_search import YoutubeSearch
import streamlit as st
from pytube import YouTube
from moviepy.editor import *
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_audioclips
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import zipfile
import re
import os

def downloadVideo(singer,n):
	search = singer + 'songs'
	output = YoutubeSearch(search,max_results = n).to_dict()
	for i in output:
		ytVideo = YouTube('https://www.youtube.com' + i['url_suffix'])
		vid = ytVideo.streams.filter(file_extension = 'mp4').first()
		vid.download(output_path=dest)

def trimToAudio(i):
	clips = []
	for file in os.listdir(dest):
			filePath = os.path.join(dest,file)
			subClip = VideoFileClip(filePath).subclip(0,i)
			Audio = subClip.audio
			clips.append(Audio)
	trimmed = concatenate_audioclips(clips)
	trimmed.write_audiofile('102017051-output.mp3')


def send_mail(to, content):

    email_address = "bkaur_be20@thapar.edu"
    email_password = "betech#compsci009"

    msg = MIMEMultipart("")
    msg['Subject'] = "MashUp Songs Of Your Favourite Singer"
    msg['From'] = email_address
    msg['To'] = to 

    attachment = open(content,'rb')
    obj = MIMEBase('application','octet-stream')
    obj.set_payload((attachment).read())
    encoders.encode_base64(obj)
    obj.add_header('Content-Disposition',"attachment; filename= "+content)
    msg.attach(obj)

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
        smtp.quit()
    print("YOUR MAIL HAS BEEN SENT SUCCESSFULLY")

def zip(file):
    final='102017051-output.zip'
    zipped=zipfile.ZipFile(final,'w')
    zipped.write(file,compress_type=zipfile.ZIP_DEFLATED)
    zipped.close()
    return final

def mainScript(singer,num,duration,to):
	downloadVideo(singer,num)
	trimToAudio(duration)
	file = '102017051-output.mp3'
	send_mail(to,zip(file))

form = st.form(key='my_form')
singer = form.text_input(label='Enter your Favourite Singer',value='')
n = form.text_input(label='Number of Videos',value=0)
dur = form.text_input(label='Duration of every Video',value=0)
mailTo = form.text_input(label='Email',value='')
submit_button = form.form_submit_button(label='Submit')
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
if submit_button:
	if not singer.strip():
		st.error('Enter Name of singer')
	elif int(n)==0:
		st.error('Enter Number of Videos')
	elif int(dur)==0:
		st.error("Enter correct Duration")
	elif not re.match(regex,mailTo):
		st.error('Enter correct Email')
	else:
		dest = "D:\predictiveAnalysis\Mashup\VidFiles"
		mainScript(singer,int(n),int(dur),mailTo)
