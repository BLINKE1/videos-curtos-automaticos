import os
import sys
import json
import uuid
import time
import threading
import subprocess
from flask import Flask, render_template, request, jsonify, Response, send_from_directory

app = Flask(__name__)

jobs = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = (data or {}).get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Tema não pode ser vazio"}), 400

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "running", "messages": [], "output": None, "error": None}

    thread = threading.Thread(target=_run_pipeline, args=(job_id, topic), daemon=True)
    thread.start()

    return jsonify({"job_id": job_id})


def _run_pipeline(job_id: str, topic: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    before = set(os.listdir(OUTPUT_DIR))

    try:
        proc = subprocess.Popen(
            [sys.executable, "-u", "main.py", topic],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=BASE_DIR,
        )
        for line in proc.stdout:
            line = line.strip()
            if line:
                jobs[job_id]["messages"].append(line)

        proc.wait()

        if proc.returncode == 0:
            after = set(os.listdir(OUTPUT_DIR))
            new_files = after - before
            if new_files:
                jobs[job_id]["status"] = "done"
                jobs[job_id]["output"] = new_files.pop()
            else:
                jobs[job_id]["status"] = "error"
                jobs[job_id]["error"] = "Arquivo de saída não encontrado."
        else:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = "Erro durante a geração do vídeo."

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)


@app.route("/progress/<job_id>")
def progress(job_id):
    def stream():
        last_idx = 0
        while True:
            job = jobs.get(job_id)
            if not job:
                yield f"data: {json.dumps({'error': 'Job não encontrado'})}\n\n"
                return

            for msg in job["messages"][last_idx:]:
                yield f"data: {json.dumps({'message': msg})}\n\n"
                last_idx += 1

            if job["status"] == "done":
                yield f"data: {json.dumps({'done': True, 'output': job['output']})}\n\n"
                return
            elif job["status"] == "error":
                yield f"data: {json.dumps({'error': job['error']})}\n\n"
                return

            time.sleep(0.5)

    return Response(
        stream(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=False, port=5000, threaded=True)
