from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/gs", methods=["POST"])
def gs_proxy():
    apps_script_url = (os.environ.get("https://script.google.com/macros/s/AKfycbwxndmNz7A0a6ct220RYhhPycM6m5DRfbxutA2_kWVN2p7dWQSwCLbk85Es3zUljPyy/exec") or "").strip()
    api_key = (os.environ.get("MYHRAPP2026") or "").strip()

    if not apps_script_url:
        return jsonify({"ok": False, "error": "Missing APPS_SCRIPT_URL env var"}), 500
    if not api_key:
        return jsonify({"ok": False, "error": "Missing APPS_SCRIPT_API_KEY env var"}), 500

    body = request.get_json(silent=True) or {}
    action = body.get("action")
    payload = body.get("payload", {})

    if not action:
        return jsonify({"ok": False, "error": "Missing action"}), 400

    try:
        r = requests.post(
            apps_script_url,
            json={"apiKey": api_key, "action": action, "payload": payload},
            timeout=45,
            allow_redirects=True,
        )
        return (r.text, r.status_code, {"Content-Type": "application/json; charset=utf-8"})
    except requests.RequestException as e:
        return jsonify({"ok": False, "error": f"Proxy request failed: {str(e)}"}), 502

@app.route("/healthz")
def healthz():
    return {"ok": True}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)

