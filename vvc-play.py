import sys
import subprocess
import signal
from re import search

if len(sys.argv) >= 2:
	input_video_filename = sys.argv[1]
	if len(sys.argv) >= 3:
		input_audio_filename = sys.argv[2]
else:
	path = sys.argv[0].split('\\')
	name = path[len(path)-1]
	print("Usage:\n\t%s input_video_filename [input_audio_filename]" % name)
	exit()

def make_command(input_video_filename, video_size):
	#return ['vvdecapp.exe', '-b', input_video_filename, '-o', '-', '|', 'ffplay', '-f', 'rawvideo', '-pix_fmt', 'yuv420p10le', '-video_size', video_size, '-i', '-', '-fs']
	return ['vvdecapp.exe', '-b', input_video_filename, '-o', '-', '|', 'ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'yuv420p10le', '-video_size', video_size, '-i', '-', '-strict', '-1', '-f', 'yuv4mpegpipe', '-', '|', 'ffplay', '-f', 'yuv4mpegpipe', '-', '-fs', '&', 'echo', 'Done playing video']

def make_command_audio(input_video_filename, video_size, input_audio_filename):
	return ['vvdecapp.exe', '-b', input_video_filename, '-o', '-', '|', 'ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'yuv420p10le', '-video_size', video_size, '-i', '-', '-i', input_audio_filename, '-c:a', 'copy', '-strict', '-1', '-f', 'matroska', '-', '|', 'ffplay', '-', '-fs', '&', 'echo', 'Done playing video']

def get_video_size(input_video_filename):
	result = subprocess.run(['vvdecapp.exe', '-b', input_video_filename, '-f', '25'], stdout=subprocess.PIPE, universal_newlines=True, shell=True)
	for s in result.stdout.split('\n'):
		if 'SizeInfo' in s:
			return str(s).split(' ')[3]

if 'input_audio_filename' in locals():
	process = subprocess.Popen(make_command_audio(input_video_filename, get_video_size(input_video_filename), input_audio_filename), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
	while True:
		c = str(process.stdout.readline())
		if search("Broken pipe", c):
			process.send_signal(signal.CTRL_C_EVENT)
			process.terminate()
			exit()
		elif search("Done playing video", c):
			process.terminate()
			exit()
else:
	process = subprocess.Popen(make_command(input_video_filename, get_video_size(input_video_filename)), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
	while True:
		c = str(process.stdout.readline())
		if search("Broken pipe", c):
			process.send_signal(signal.CTRL_C_EVENT)
			process.terminate()
			exit()
		elif search("Done playing video", c):
			process.terminate()
			exit()