# PPT Audio Video Sync

Sync narrated audio with exported PowerPoint videos using slide-change markers and forced alignment.

This project is for creators who build slide-based videos in PowerPoint, record narration separately, and want the final video to follow the narration timing automatically. Instead of manually adjusting slide durations, the tool detects slide changes in the exported PowerPoint video and uses the narration script plus audio to generate a synchronized output video.

It was created for the production workflow behind the [Code Collider YouTube channel](https://www.youtube.com/@codecollider). You can watch a sample video made with this approach below.

[![Sample video created with PPT Audio Video Sync](https://img.youtube.com/vi/kmJz8w5ij8Y/maxresdefault.jpg)](https://www.youtube.com/watch?v=kmJz8w5ij8Y)

## What It Does

- Detects slide changes from small black and white markers added to the PowerPoint slides.
- Aligns narration audio with a plain text narration script.
- Adjusts the exported PowerPoint video so each slide stays on screen for the matching narrated section.
- Combines the synchronized video with the narration audio.
- Can generate SRT subtitles from the narration/audio alignment.

## How It Works

1. A VBA macro adds tiny alternating black and white markers to the bottom-right corner of each slide.
2. PowerPoint exports the presentation as a regular video.
3. The Python script detects marker changes to find slide boundaries.
4. `aeneas` aligns the narration audio with the narration script.
5. The script builds a new video where slide timing follows the narration.

## Requirements

- Python 3
- PowerPoint with VBA support
- FFmpeg available on your system path
- Python dependencies from `requirements.txt`

Install Python dependencies from the project root:

```bash
pip install -r requirements.txt
```

## Narration Script Format

The narration script must be a plain text file with one line per slide.

The number of lines in the narration script should match the number of slides in the PowerPoint deck. For example, a 20-slide presentation should have a 20-line narration script.

## Usage

1. Finish creating the PowerPoint slides.
2. Open the presentation in PowerPoint.
3. Press `Alt + F11` to open Microsoft Visual Basic for Applications.
4. Right-click `VBAProject` for the presentation.
5. Choose `Insert > Module`.
6. Copy the code from `add_slide_change_identifiers` and paste it into the VBA module.
7. Save the file and press `F5` to run the macro.
8. Export the PowerPoint file as a video.
9. Copy the exported video, narration audio, and narration script into the `app/` directory.
10. In `sync_video_audio.py`, update the input file paths:

```python
video_path = "raw_video_1080p.mp4"
audio_path = "narration.mp3"
script_path = "script.txt"
```

11. Run the sync script from inside `app/`:

```bash
python sync_video_audio.py
```

The synchronized video is written as `output_video.mp4`.

## Subtitle Generation

`generate_subtitles.py` can create an SRT subtitle file from the narration script and audio alignment.

Update the script and audio paths inside `generate_subtitles.py`, then run:

```bash
python generate_subtitles.py
```

The subtitle file is written as `output.srt`.

## Output Files

The scripts may generate intermediate and output files such as:

- `syncmap.json`
- `ovideo.mp4`
- `output_video.mp4`
- `output.srt`
- `__temp__script__.txt`
- `__temp__syncmap__.json`

## Troubleshooting

- Run the scripts from inside the `app/` directory.
- Keep one narration script line per slide.
- Make sure the exported video contains the black and white slide-change markers.
- If video or audio processing fails, check that FFmpeg is installed and available on your system path.
- If you get a division by zero error in the sanity script, check that the script is being run from inside `app/`.

## Roadmap

- Add command-line arguments for video, audio, and script paths.
- Add clearer validation when input files are missing.
- Move generated files into an `output/` directory.
- Document tested operating systems and PowerPoint export settings.
