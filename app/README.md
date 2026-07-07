After you are done with making PPT slides.
Press Alt + F11 to open Microsoft Visual Basics for Application, right click on VBAProject (ppt) > Insert > Module
Copy code from add_slide_change_identifiers and paste in MS VBA, save the file, and press F5 to run it, this will add black and white boxes in bottom left alternatively. Export PPT to video. 
Copy the video file, audio file, and script file into this app directory
In sync_video_audio.py, change video_path, audio_path, and script_path according to file names you moved and run the file

ISSUES
1. If you get division by zero error in sanity script, check that you are running script from inside app/.