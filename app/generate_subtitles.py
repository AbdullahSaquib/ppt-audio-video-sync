
from convert_syncmap_to_srt import create_srt_from_syncmap
from sync_video_audio import make_audio_script_sync_file


script_file_path = "script.txt"
audio_path = "Take 2 raw-enhanced-v2-loud.mp3"

with open(script_file_path) as f:
    lines = f.readlines()

subtitle_lines = []

for line in lines:
    words = line.split()
    groups = [words[i:i+6] for i in range(0, len(words), 6)]
    for group in groups:
        subtitle_lines.append(" ".join(group)) 

script_path = "__temp__script__.txt"
audio_script_sync_map_path = "__temp__syncmap__.json"
with open(script_path, "w") as f:
    for line in subtitle_lines:
        f.write(line)
        f.write("\n")

make_audio_script_sync_file(audio_path, script_path, audio_script_sync_map_path)
create_srt_from_syncmap(audio_script_sync_map_path)