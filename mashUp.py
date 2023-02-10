from youtube_search import YoutubeSearch
import streamlit as st
from pytube import YouTube
from moviepy.editor import *
from moviepy.editor import VideoFileClip,concatenate_videoclips
from moviepy.editor import concatenate_audioclips, AudioFileClip
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
import re
import zipfile
import json
import os

def downloadToAudio(singer,n):
	search_query = singer + 'video'
	output = YoutubeSearch(search_query,max_results = n).to_dict()
	for i in output:
		ytVideo = YouTube('https://www.youtube.com' + i['url_suffix'])
		vid = ytVideo.streams.filter(file_extension = 'mp4').first()
		dest = "Video_files"
		output_file = vid.download(output_path=dest)
		Path , ext = os.path.splitext(output_file)
		vid = VideoFileClip(os.path.join(Path + ".mp4"))

def trim(singer,n,i):
	folder = "Video_files/"
	clips = []
	for file in os.listdir(folder):
		if file.endwith(".mp4"):
			filePath = os.path.join(folder,file)
			subClip = VideoFileClip(filePath).subclip(0,i)
			Audio = subclip.audio
			clips.append(Audio)
	trimmed = concatenate_audioclips(clips)
	trimmed.write_audiofile('final.mp3')


def send_mail(to, content):

    email_address = "k.bisman16@gmail.com"
    email_to = to
    email_password = "dbdhbdhbf"
    # create email
    msg = EmailMessage()
    msg = MIMEMultipart("alternative")
    msg['Subject'] = "MashUp Result File"
    msg['From'] = email_address
    msg['To'] = to 

    part = MIMEText(content, "html")
    msg.attach(part)
    filename = content
    attachment= open(filename, 'rb') 
    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(attachment_package)
    text = msg.as_string()

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.sendmail(email_from, email_to, text)


def script(singer,to,num,duration):
	downloadToAudio(singer,num)
	trim(singer,num,duration)
	file = 'concat.mp3'
	send_mail(file,to)


form = st.form(key='my_form')
singer = form.text_input(label='Enter yout favourite singer',value='')
n = form.text_input(label='"\# of Videos',value=0)
dur = form.text_input(label='Duration of every video',value=0)
mailTo = form.text_input(label='Email',value='')
submit_button = form.form_submit_button(label='Submit')

folder = "Video_files"
for file in os.listdir(folder):
	filePath = os.path.join(folder,file)
	if os.path.isfile(filePath) or os.path.islink(filePath):
		os.unlink(filePath)
script(singer,mailTo,int(n),int(dur))
