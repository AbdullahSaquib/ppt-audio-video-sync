import json
import cv2
import numpy as np
from aeneas.executetask import ExecuteTask
from aeneas.task import Task


def is_black_or_white(pixel):
    pixel_sum = np.sum(pixel, dtype=np.uint16)  # Use a larger data type for the sum
    average_pixel_value = pixel_sum // 3  # Integer division to avoid potential overflow
    return "black" if average_pixel_value < 128 else "white"


def get_video_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    return cap.get(cv2.CAP_PROP_FPS)


def get_scenes(video_path):
    cap = cv2.VideoCapture(video_path)
    # Get frame rate to calculate timestamps
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    previous_color = None
    start_frame = 1
    scenes = []
    # Loop through each frame
    prev_frame = None
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        # Extract the bottom-right pixel (change size if needed to a region)
        height, width, _ = frame.shape
        bottom_right_pixel = frame[height - 5, width - 5]
        # Check the color of the bottom-right pixel
        current_color = is_black_or_white(bottom_right_pixel)
        # Detect scene if previous color exists and is different
        if previous_color and current_color and previous_color != current_color:
            timestamp = frame_count / fps
            ## Saving scene frames for debugging
            # cv2.imwrite(f'frame{len(scenes)+1}_1.jpg', start_frame)
            # cv2.imwrite(f'frame{len(scenes)+1}_2.jpg', frame_count-1)
            scenes.append((start_frame, frame_count - 1, timestamp))
            start_frame = frame_count
        # Update previous color
        if current_color:
            previous_color = current_color
        prev_frame = frame
    scenes.append((start_frame, frame_count, frame_count / fps))
    # Release video capture
    cap.release()
    return scenes


def make_audio_script_sync_file(audio_path, script_path, output_file):
    # sanity_scenes_equal_script_lines(video_path, script_path)
    # create Task object
    config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = audio_path
    task.text_file_path_absolute = script_path
    task.sync_map_file_path_absolute = output_file
    # process Task
    ExecuteTask(task).execute()
    # output sync map to file
    task.output_sync_map_file()


def trim_video(input_video_path, output_video_path, frames_to_keep):
    fps = get_video_fps(video_path)
    # Open the input video
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error: Could not open input video.")
        return
    # Get the width and height of the video frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # Define the codec and create VideoWriter object for the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change the codec to 'XVID' or others if needed
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    # Sort the frames to keep in ascending order
    frames_to_keep = sorted(frames_to_keep)
    curr_frame = 1  # Current frame index in the original video
    last_frame_index = -1  # Last frame index of frames_to_keep
    # Loop through the frames in the original video
    stopped = False
    while cap.isOpened() or not stopped:
        ret, frame = cap.read()
        if not ret:
            break  # End of video
        if last_frame_index < 0:
            out.write(frame)
            last_frame_index = 0
        else:
            if last_frame_index+1 >= len(frames_to_keep):
                stopped = True
                break
            frame_to_keep = frames_to_keep[last_frame_index + 1]
            while frame_to_keep == curr_frame:
                out.write(frame)
                last_frame_index += 1
                if last_frame_index >= len(frames_to_keep):
                    stopped = True
                    break
                frame_to_keep = frames_to_keep[last_frame_index]
        curr_frame += 1
    # Release video objects
    cap.release()
    out.release()
    print("Trimmed video saved at:", output_video_path)


def get_final_video_frames(video_path, audio_path, script_path):
    print("Syncing Video Started")
    print("video_path:", video_path)
    print("audio_path:", audio_path)
    print("script_path:", script_path)
    audio_script_sync_map_path = "syncmap.json"
    fps = get_video_fps(video_path)
    print("Video FPS:", fps)
    print("Creating audio and script text syncmap...", end="", flush=True)
    make_audio_script_sync_file(audio_path, script_path, audio_script_sync_map_path)
    print("DONE")
    with open(audio_script_sync_map_path) as f:
        data = json.load(f)
    print("Fetching video scenes...", end="", flush=True)
    scenes = get_scenes(video_path)
    print("DONE", len(scenes), "scenes found in video!")
    print("Identifying Scenes Frames...", end="", flush=True)
    frames = []
    for i, fragment in enumerate(data["fragments"]):
        scene = scenes[i]
        scene_start_frame = scene[0]
        scene_end_frame = scene[1]
        begin = float(fragment["begin"])
        end = float(fragment["end"])
        duration = end - begin
        frames_count = int(round(duration * fps))
        for i in range(frames_count):
            frames.append(min(scene_start_frame+i, scene_end_frame))
    print("DONE")
    print("Creating Video...", flush=True, end="")
    trim_video(video_path, "ovideo.mp4", frames)
    print("DONE")
    print("Adding audio to video...")
    combine_video_audio("ovideo.mp4", audio_path)
    return frames

def combine_video_audio(video_path, audio_path):
    from moviepy.editor import VideoFileClip, AudioFileClip
    # Load video and audio files
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    # Set the audio of the video clip to the audio file
    video = video.set_audio(audio)
    # Write the result to a new file
    video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")



def sanity_scenes_equal_script_lines(video_path, script_path):
    scenes = len(get_scenes(video_path))
    with open(script_path) as f:
        script_lines = len(f.readlines())
    try:
        assert scenes == script_lines
        print("[OK] Scenes count and script lines count matched!")
    except AssertionError:
        print(f"[Failed] Scenes={scenes}  Script Lines={script_lines}")


if __name__ == "__main__":
    # Initialize video capture
    video_path = "raw_video_1080p.mp4"  # Replace with the path to your video file
    audio_path = "Take 2 raw-enhanced-v2-loud.mp3"
    script_path = "script.txt"
    fps = 30

    # sanity_scenes_equal_script_lines(video_path, script_path)
    get_final_video_frames(video_path, audio_path, script_path)
    print(get_video_fps("output_video.mp4"))
