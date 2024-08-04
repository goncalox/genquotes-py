import os
import subprocess
import groq_obtain_quote

def create_generated_video():

    background_image = './assets/background.jpeg'
    background_music = './assets/ambient.mp3'
    generated_video = './output/generated_video.mp4'  # Output video path
    font_file = './assets/OpenSans.ttf'

    quote1_file_path = './temp_text_files/quote1.txt'
    quote2_file_path = './temp_text_files/quote2.txt'
    author_file_path = './temp_text_files/author.txt'

    os.makedirs(os.path.dirname(quote1_file_path), exist_ok=True)
    os.makedirs(os.path.dirname(generated_video), exist_ok=True)

    first_text_overlay = ""
    second_text_overlay = ""
    third_text_overlay = ""
    author_text_overlay = ""
    video_length = 15

    if os.path.exists(quote2_file_path)==False:
        video_length = 10

    # Define the y positions dynamically
    first_text_y = "3*h/4-text_h-50"
    second_text_y = "3*h/4"
    author_text_y = "h/5"

    if os.path.exists(quote1_file_path):
        first_text_overlay = (
            f"drawtext=textfile='{quote1_file_path}':fontfile='{font_file}':fontsize=50:fontcolor=black:"
            f"box=1:boxcolor=white@0.9:boxborderw=10:x=(w-text_w)/2:y={first_text_y}:enable='between(t,0,{video_length})'"
        )

    if os.path.exists(quote2_file_path):
        second_text_overlay = (
            f"drawtext=textfile='{quote2_file_path}':fontfile='{font_file}':fontsize=50:fontcolor=black:"
            f"box=1:boxcolor=white@0.9:boxborderw=10:x=(w-text_w)/2:y={second_text_y}:enable='between(t,5,{video_length})'"
        )

    if os.path.exists(author_file_path):
        author_text_overlay = (
            f"drawtext=textfile='{author_file_path}':fontfile='{font_file}':fontsize=60:fontcolor=black:"
            f"box=1:boxcolor=white@0.9:boxborderw=10:x=(w-text_w)/2:y={author_text_y}:enable='between(t,{video_length-5},{video_length})'"
        )

    zoom_in = "zoompan=z='zoom+0.001':d=2000:s=1080x1920:y=(ih/2)-(ih/zoom/2)"
    zoom_in_center = "zoompan=z='zoom+0.001':d=2000:s=1080x1920:x=(iw/2)-(iw/zoom/2):y=(ih/2)-(ih/zoom/2)"
    zoom_out = "zoompan=z='if(eq(on,1),1.1,zoom-0.001)':d=1000:s=1080x1920:x=(iw/2)-(iw/zoom/2):y=(ih/2)-(ih/zoom/2)"
    padding = "pad=width=iw+50:height=ih+50:x=25:y=25:color=white"
    noise = "noise=alls=50:allf=t+u"

    # Define the slight zoom and pan effect to mimic camera shake
    PI = 3.141592653589793
    frame_rate = 30  # Adjust this based on your actual frame rate
    camera_shake = f"zoompan=z='zoom+0.001*sin(2*{PI}*on/{frame_rate}/2)':s=1080x1920:x='iw/2-(iw/zoom/2)+20*sin(2*{PI}*on/{frame_rate}/0.5)':y='ih/2-(ih/zoom/2)+20*sin(2*{PI}*on/{frame_rate}/0.5)':d=1"

    # Add motion blur using tblend
    motion_blur = "tblend=all_mode=average,tblend=all_mode=lighten,tblend=all_mode=darken"

    # Combine non-empty filters
    filters = [camera_shake, noise, motion_blur, padding]
    if first_text_overlay:
        filters.append(first_text_overlay)
    if second_text_overlay:
        filters.append(second_text_overlay)
    if author_text_overlay:
        filters.append(author_text_overlay)

    filter_complex = ",".join(filters)

    ffmpeg_command = [
        'ffmpeg', '-y', '-loop', '1', '-i', background_image,
        '-i', background_music,
        '-vf', f"scale=1080:1920,{filter_complex}",
        '-c:v', 'libx264', '-t', str(video_length), '-pix_fmt', 'yuv420p',
        '-shortest', generated_video
    ]

    result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error executing FFmpeg command for generated video: {result.stderr.decode()}")
    else:
        print(f"Generated video created successfully: {generated_video}")

if __name__ == "__main__":
    groq_obtain_quote
    create_generated_video()
