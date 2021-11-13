# VVC-Tools

Just some python wrappers for calling [vvenc](https://github.com/fraunhoferhhi/vvenc) and [vvdec](https://github.com/fraunhoferhhi/vvdec)

You will need to have vvencapp for vvc-encode.py, and vvdecapp for vvc-play.py

ffmpeg is required for both and ffplay is also needed for vvc-play.py

# Note
While vvc-play.py calls vvdecapp directly vvc-encode.py simply prints the command for you to run incase you want to change it before starting the encode.
