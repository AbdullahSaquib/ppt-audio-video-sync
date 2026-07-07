import json
from datetime import timedelta

def convert_to_srt_time(timestamp):
    """
    Convert timestamp in the format 'seconds.milliseconds' to SRT format 'hh:mm:ss,ms'.
    """
    time_obj = timedelta(seconds=float(timestamp))
    total_seconds = int(time_obj.total_seconds())
    milliseconds = int((time_obj.total_seconds() - total_seconds) * 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def json_to_srt(json_data):
    """
    Convert JSON subtitle data to SRT format.
    """
    srt_output = []
    for idx, fragment in enumerate(json_data["fragments"], start=1):
        begin = convert_to_srt_time(fragment["begin"])
        end = convert_to_srt_time(fragment["end"])
        lines = " ".join(fragment["lines"])

        srt_output.append(f"{idx}\n{begin} --> {end}\n{lines}\n")

    return "\n".join(srt_output)


def create_srt_from_syncmap(syncmap_path="syncmap.json", output_path="output.srt"):
    with open(syncmap_path) as f:
        subtitle_data = json.load(f)
    # Convert and save to SRT
    srt_content = json_to_srt(subtitle_data)
    with open(output_path, "w", encoding="utf-8") as srt_file:
        srt_file.write(srt_content)
    print("SRT file created: output.srt")


if __name__ == "__main__":
    create_srt_from_syncmap()

