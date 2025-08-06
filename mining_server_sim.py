import time
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# Block data (simplified for this example)
block_data = {
    "version": "1",
    "previous_hash": "0" * 64,
    "merkle_root": "4a5e1e",
    "timestamp": "1722750000",
    "bits": 0x1f00ffff  
}

def bits_to_target(bits):
    exponent = bits >> 24
    coefficient = bits & 0xffffff
    return coefficient * (1 << (8 * (exponent - 3)))


target = int(0x00000000FFFF0000000000000000000000000000000000000000000000000000 // 0.005)

# Shared state
nonce_counter = 0
nonce_step = 100000

lock = threading.Lock()
found_solution = False
start_time = time.time()

@app.route("/get_work", methods=["GET"])
def get_work():
    global nonce_counter
    if found_solution:
        return jsonify({"status": "solved"})

    with lock:
        start = nonce_counter
        end = nonce_counter + nonce_step
        nonce_counter += nonce_step

    response = {
        "block": block_data,
        "nonce_start": start,
        "nonce_end": end,
        "target": target
    }
    return jsonify(response)

@app.route("/submit", methods=["POST"])
def submit():
    global found_solution
    data = request.get_json()
    if data['hash_int'] < target:
        found_solution = True
        end_time = time.time()
        print("✅ Block mined!")
        print(f"Nonce: {data['nonce']}")
        print(f"Hash: {data['hash_hex']}")
        print(f"⏱️ Time taken: {end_time - start_time:.2f} seconds")
        return jsonify({"status": "accepted"})
    return jsonify({"status": "rejected"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

