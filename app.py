from flask import Flask, jsonify, render_template, request
import tracer
app = Flask(__name__)
G, LABELS, NAMES = tracer.load()

@app.get("/")
def index(): return render_template("index.html")

@app.get("/api/trace")
def api_trace():
    w = request.args.get("wallet", "").strip()
    r = tracer.trace(G, LABELS, NAMES, w)
    if r is None: return jsonify({"error": "wallet not in sample graph", "try": "0xSUSPECT"}), 404
    return jsonify(r)

if __name__ == "__main__":
    app.run(port=5002)
