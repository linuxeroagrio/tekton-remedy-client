from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

REMEDY_HOST = os.getenv("REMEDY_HOST")
REMEDY_BASEPATH = os.getenv("REMEDY_BASEPATH", "")
REMEDY_USER = os.getenv("REMEDY_USER")
REMEDY_PASS = os.getenv("REMEDY_PASS")

# Obtiene token AR-JWT
def get_jwt():
    url = f"https://{REMEDY_HOST}{REMEDY_BASEPATH}/api/jwt/login"
    resp = requests.post(url, auth=(REMEDY_USER, REMEDY_PASS), verify=False)
    resp.raise_for_status()
    return resp.text

@app.route("/healthz")
def health():
    return "ok", 200

@app.route("/ready")
def ready():
    return "ready", 200

# Crear CRQ
@app.route("/api/v1/crq", methods=["POST"])
def create_crq():
    jwt = get_jwt()
    payload = request.json
    
    remedy_url = f"https://{REMEDY_HOST}{REMEDY_BASEPATH}/api/arsys/v1/entry/CHG:ChangeInterface"
    headers = {"Authorization": f"AR-JWT {jwt}", "Content-Type": "application/json"}
    
    resp = requests.post(remedy_url, json={"values": payload}, headers=headers, verify=False)
    data = resp.json()
    
    crq_id = data.get("values", {}).get("request_id", "UNKNOWN")
    return jsonify({"crq_id": crq_id, "raw": data}), resp.status_code

# Aprobar CRQ
@app.route("/api/v1/crq/<crq_id>/approve", methods=["POST"])
def approve(crq_id):
    jwt = get_jwt()
    payload = request.json
    
    remedy_url = f"https://{REMEDY_HOST}{REMEDY_BASEPATH}/api/arsys/v1/entry/CHG:Approvals/{crq_id}"
    headers = {"Authorization": f"AR-JWT {jwt}", "Content-Type": "application/json"}
    
    resp = requests.put(remedy_url, json={"values": payload}, headers=headers, verify=False)
    return jsonify(resp.json()), resp.status_code

# Cerrar CRQ
@app.route("/api/v1/crq/<crq_id>/close", methods=["POST"])
def close_crq(crq_id):
    jwt = get_jwt()
    payload = request.json
    
    remedy_url = f"https://{REMEDY_HOST}{REMEDY_BASEPATH}/api/arsys/v1/entry/CHG:ChangeInterface/{crq_id}"
    headers = {"Authorization": f"AR-JWT {jwt}", "Content-Type": "application/json"}
    
    resp = requests.put(remedy_url, json={"values": payload}, headers=headers, verify=False)
    return jsonify(resp.json()), resp.status_code

# Subir archivo
@app.route("/api/v1/crq/<crq_id>/attachments", methods=["POST"])
def attach(crq_id):
    jwt = get_jwt()
    file = request.files['file']
    desc = request.form.get("description", "Uploaded via API")
    
    remedy_url = f"https://{REMEDY_HOST}{REMEDY_BASEPATH}/api/arsys/v1/entry/CHG:ChangeInterface"
    headers = {"Authorization": f"AR-JWT {jwt}"}
    
    files = {
        "entry": (None, f'{{"values":{{"Change ID":"{crq_id}","Description":"{desc}"}}}}', "application/json"),
        "attach1": (file.filename, file.stream, file.content_type)
    }
    
    resp = requests.post(remedy_url, files=files, headers=headers, verify=False)
    return jsonify(resp.json()), resp.status_code

# Crear tarea
@app.route("/api/v1/crq/<crq_id>/tasks", methods=["POST"])
def create_task(crq_id):
    jwt = get_jwt()
    payload = request.json
    payload["Change ID"] = crq_id
    
    remedy_url = f"https://{REMEDY_HOST}{REMEDY_BASEPATH}/api/arsys/v1/entry/TAS:Task"
    headers = {"Authorization": f"AR-JWT {jwt}", "Content-Type": "application/json"}
    
    resp = requests.post(remedy_url, json={"values": payload}, headers=headers, verify=False)
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("ADAPTER_PORT", "8080")))