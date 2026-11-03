import os, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
OUT = Path("output")
OUT.mkdir(exist_ok=True)


def get_font(size):
    for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make_frame(description, index, path):
    colors = [(255,120,95),(255,195,70),(65,205,190),(135,130,255),(255,120,190)]
    image = Image.new("RGB", (W,H), (13,22,48))
    draw = ImageDraw.Draw(image)
    color = colors[index % len(colors)]
    draw.ellipse((150,250,930,1030), fill=color)
    draw.ellipse((285,385,795,895), fill=(250,245,230))
    draw.ellipse((420,550,500,630), fill=(20,30,55))
    draw.ellipse((580,550,660,630), fill=(20,30,55))
    draw.arc((420,600,665,800), 5, 175, fill=(20,30,55), width=20)
    draw.rounded_rectangle((90,1130,990,1740), radius=48, fill=(250,245,230))
    words, lines, line = description.split(), [], ""
    font = get_font(48)
    for word in words:
        candidate = (line + " " + word).strip()
        if draw.textbbox((0,0), candidate, font=font)[2] < 790:
            line = candidate
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    y = 1280
    for item in lines[:5]:
        box = draw.textbbox((0,0), item, font=font)
        draw.text(((W-(box[2]-box[0]))/2,y), item, font=font, fill=(20,30,55))
        y += 75
    draw.text((70,70), f"STORY {index+1}/5", font=get_font(34), fill="white")
    image.save(path)


def make_voice(text, path):
    voice = os.getenv("VOICE", "en-us+m3")
    subprocess.run(
        ["espeak-ng", "-v", voice, "-s", "145", "-p", "35", "-a", "175", "-w", str(path), text],
        check=True, capture_output=True, text=True,
    )


def render(story):
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)
        audio = tmp / "voice.wav"
        make_voice(story["narration"], audio)
        frames = []
        for i, description in enumerate(story["scenes"]):
            frame = tmp / f"frame{i}.png"
            make_frame(description, i, frame)
            frames.append(frame)
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(audio)],
            check=True, capture_output=True, text=True)
        duration = max(float(probe.stdout.strip()), 10.0)
        each = duration / len(frames)
        args, filters = [], []
        for frame in frames:
            args += ["-loop", "1", "-t", str(each), "-i", str(frame)]
        args += ["-i", str(audio)]
        for i in range(len(frames)):
            filters.append(
                f"[{i}:v]scale=1188:2112,zoompan=z='min(zoom+0.0007,1.08)':"
                f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                f"d=1:s=1080x1920:fps=30,setsar=1[v{i}]"
            )
        joined = "".join(f"[v{i}]" for i in range(len(frames)))
        filters.append(f"{joined}concat=n={len(frames)}:v=1:a=0,format=yuv420p[v]")
        output = OUT / "latest_short.mp4"
        cmd = ["ffmpeg", "-y", *args, "-filter_complex", ";".join(filters),
               "-map", "[v]", "-map", f"{len(frames)}:a", "-c:v", "libx264",
               "-preset", "veryfast", "-r", "30", "-c:a", "aac", "-shortest",
               "-movflags", "+faststart", str(output)]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return str(output)
