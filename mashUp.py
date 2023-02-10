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
import os

def downloadVideo(singer,n):
	search_query = singer + 'video'
	output = YoutubeSearch(search_query,max_results = n).to_dict()
	for i in output:
		ytVideo = YouTube('https://www.youtube.com' + i['url_suffix'])
		vid = ytVideo.streams.filter(file_extension = 'mp4').first()
		dest = "D:\predictiveAnalysis\Mashup\Video_files"
		output_file = vid.download(output_path=dest)
		Path,ext = os.path.splitext(output_file)
		ext = ".mp4"
		vid = VideoFileClip(os.path.join(Path + ext))

def trimToAudio(i):
	folder = "D:\predictiveAnalysis\Mashup\Video_files"
	clips = []
	for file in os.listdir(folder):
			filePath = os.path.join(folder,file)
			subClip = VideoFileClip(filePath).subclip(0,i)
			Audio = subClip.audio
			clips.append(Audio)
	trimmed = concatenate_audioclips(clips)
	trimmed.write_audiofile('MashUp.mp3')


def send_mail(to, content):

    email_address = "k.bisman16@gmail.com"
    email_to = to
    email_password = "hadsjgadfufdd"
    # create email
    msg = EmailMessage()
    msg = MIMEMultipart("alternative")
    msg['Subject'] = "MashUp Result File"
    msg['From'] = email_address
    msg['To'] = to 

    part = MIMEText(content, "plain")
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
        smtp.sendmail(email_address, email_to, text)


def mainScript(singer,num,duration,to):
	downloadVideo(singer,num)
	trimToAudio(duration)
	file = 'MashUp.mp3'
	send_mail(to,file)

form = st.form(key='my_form')
singer = form.text_input(label='Enter your Favourite Singer',value='')
n = form.text_input(label='Number of Videos',value=0)
dur = form.text_input(label='Duration of every Video',value=0)
mailTo = form.text_input(label='Email',value='')
submit_button = form.form_submit_button(label='Submit')
if submit_button:
	if not singer.strip():
		st.error('Enter Name of singer')
	elif int(n)==0:
		st.error('Enter Number of Videos')
	elif int(dur)==0:
		st.error("Enter correct Duration")
	else:
		newFolder = "D:\predictiveAnalysis\Mashup\Video_files"
		for fileName in os.listdir(newFolder):
			filePath = os.path.join(newFolder,fileName)
		mainScript(singer,int(n),int(dur),mailTo)
