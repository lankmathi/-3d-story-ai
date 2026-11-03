import os, traceback
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from app.content import generate_story
from app.render import render

load_dotenv()
app = FastAPI(title="3D Story AI")
scheduler = BackgroundScheduler(timezone=os.getenv("TIMEZONE", "Africa/Lagos"))
STATE = {"status": "Ready", "title": "", "video": ""}

def build_short():
    try:
        story = generate_story()
        path = render(story)
        STATE.update(status="Draft generated. Review before publishing.", title=story["title"], video=path)
    except Exception as exc:
        STATE.update(status=f"Generation failed: {exc}", video="")
        traceback.print_exc()

@app.on_event("startup")
def start_scheduler():
    if os.getenv("ENABLE_SCHEDULER", "false").lower() == "true":
        for value in os.getenv("POST_TIMES", "10:00,18:00").split(","):
            hour, minute = map(int, value.strip().split(":"))
            scheduler.add_job(build_short, CronTrigger(hour=hour, minute=minute))
        scheduler.start()

@app.on_event("shutdown")
def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()

@app.get("/", response_class=HTMLResponse)
def home():
    return Path("app/index.html").read_text()

@app.get("/health")
def health():
    return {"ok": True, "status": STATE["status"]}

@app.post("/generate")
def generate():
    build_short()
    return {"status": STATE["status"], "title": STATE["title"]}

@app.get("/status")
def status():
    return STATE

@app.get("/video")
def video():
    path = Path(STATE["video"])
    if not path.exists():
        return {"error": "No video draft exists yet"}
    return FileResponse(path, media_type="video/mp4", filename="story-short.mp4")
