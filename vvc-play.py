import sys
import subprocess

if len(sys.argv) >= 2:
	input_video_filename = sys.argv[1]
	#print(input_video_filename)
else:
	path = sys.argv[0].split('\\')
	name = path[len(path)-1]
	print("Usage:\n\t%s input_video_filename" % name)
	exit()

def make_command(input_video_filename, video_size):
	#return "vvdecapp.exe -b \"{input_video_filename}\" -o - | ffmpeg -f rawvideo -pix_fmt yuv420p10le -video_size {video_size} -i - -strict -1 -f yuv4mpegpipe - | ffplay -f yuv4mpegpipe -".format(input_video_filename=input_video_filename, video_size=video_size,)
	return ['vvdecapp.exe', '-b', input_video_filename, '-o', '-', '|', 'ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'yuv420p10le', '-video_size', video_size, '-i', '-', '-strict', '-1', '-f', 'yuv4mpegpipe', '-', '|', 'ffplay', '-f', 'yuv4mpegpipe', '-', '-fs']

def get_video_size(input_video_filename):
	result = subprocess.run(['vvdecapp.exe', '-b', input_video_filename, '-f', '25', '|', 'grep', 'SizeInfo'], stdout=subprocess.PIPE, shell=True)
	return str(result.stdout).split(' ')[3]

#print("Video size is: %s\n" % get_video_size(input_video_filename))

subprocess.run(make_command(input_video_filename, get_video_size(input_video_filename)), shell=True)