import sys
import subprocess
import os
import signal
from re import search

if len(sys.argv) >= 2:
	input_video_filename = sys.argv[1]
	if len(sys.argv) >= 3:
		input_audio_filename = sys.argv[2]
	#print(input_video_filename)
else:
	path = sys.argv[0].split('\\')
	name = path[len(path)-1]
	print("Usage:\n\t%s input_video_filename" % name)
	exit()

def make_command(input_video_filename, video_size):
	#return "vvdecapp.exe -b \"{input_video_filename}\" -o - | ffmpeg -f rawvideo -pix_fmt yuv420p10le -video_size {video_size} -i - -strict -1 -f yuv4mpegpipe - | ffplay -f yuv4mpegpipe -".format(input_video_filename=input_video_filename, video_size=video_size,)
	return ['vvdecapp.exe', '-b', input_video_filename, '-o', '-', '|', 'ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'yuv420p10le', '-video_size', video_size, '-i', '-', '-strict', '-1', '-f', 'yuv4mpegpipe', '-', '|', 'ffplay', '-f', 'yuv4mpegpipe', '-', '-fs']
def make_command_audio(input_video_filename, video_size, input_audio_filename):
	#return "vvdecapp.exe -b \"{input_video_filename}\" -o - | ffmpeg -f rawvideo -pix_fmt yuv420p10le -video_size {video_size} -i - -strict -1 -f yuv4mpegpipe - | ffplay -f yuv4mpegpipe -".format(input_video_filename=input_video_filename, video_size=video_size,)
	return ['vvdecapp.exe', '-b', input_video_filename, '-o', '-', '|', 'ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'yuv420p10le', '-video_size', video_size, '-i', '-', '-i', input_audio_filename, '-c:a', 'copy', '-strict', '-1', '-f', 'matroska', '-', '|', 'ffplay', '-', '-fs']

def get_video_size(input_video_filename):
	result = subprocess.run(['vvdecapp.exe', '-b', input_video_filename, '-f', '25', '|', 'grep', 'SizeInfo'], stdout=subprocess.PIPE, shell=True)
	return str(result.stdout).split(' ')[3]

#print("Video size is: %s\n" % get_video_size(input_video_filename))

if 'input_audio_filename' in locals():
	process = subprocess.Popen(make_command_audio(input_video_filename, get_video_size(input_video_filename), input_audio_filename), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True, shell=True)
	while True:
		c = str(process.stdout.readline())
		if search("Broken pipe", c):
			process.terminate()
			exit()
else:
	process = subprocess.run(make_command(input_video_filename, get_video_size(input_video_filename)), shell=True)
	while True:
		c = str(process.stdout.readline())
		if search("Broken pipe", c):
			process.terminate()
			exit()