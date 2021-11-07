import sys
from pymediainfo import MediaInfo

if len(sys.argv) >= 2:
	input_filename = sys.argv[1]
	print(input_filename)
else:
	path = sys.argv[0].split('\\')
	name = path[len(path)-1]
	print("Usage:\n\t%s input_filename" % name)
	exit()

def make_command(input_filename, width, height, frame_rate):
	return "ffmpeg -i \"{input_filename}\" -f rawvideo -pix_fmt yuv420p pipe:1 | vvencapp -i - -s {width}x{height} -c yuv420 -r {frame_rate} --preset medium --qp 31 --qpa 0 -ip 64 -t {threads} -o \"{output_filename}.266\"".format(input_filename=input_filename, width=width, height=height, frame_rate=frame_rate, threads=(4 if height < 720 else 8), output_filename=input_filename.split('.')[0])

media_info = MediaInfo.parse(input_filename)

for track in media_info.tracks:
	if track.track_type == "Video":
		print("Width: %s" % track.width)
		print("Height: %s" % track.height)
		print("Frame Rate: %s" % track.frame_rate)
		command = make_command(input_filename, track.width, track.height, track.frame_rate.split('.')[0])

print(command)