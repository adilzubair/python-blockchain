import requests
import hashlib
import time

# Set this to your server's address, e.g. "http://localhost:5000" or "http://<server-ip>:5000"
SERVER = "http://localhost:5000"

def calculate_hash(block, bits, nonce):
    header = (
        block['version'] +
        block['previous_hash'] +
        block['merkle_root'] +
        block['timestamp'] +
        format(bits, 'x') +
        str(nonce)
    )
    hash_result = hashlib.sha256(hashlib.sha256(header.encode()).digest()).hexdigest()
    return hash_result

while True:
    res = requests.get(f"{SERVER}/get_work").json()

    if res.get("status") == "solved":
        print("Block already solved. Stopping miner.")
        break

    block = res['block']
    bits = block['bits']
    target = res['target']
    nonce_start = res['nonce_start']
    nonce_end = res['nonce_end']

    print(f"Mining from {nonce_start} to {nonce_end}")

    for nonce in range(nonce_start, nonce_end):
        hash_hex = calculate_hash(block, bits, nonce)
        hash_int = int(hash_hex, 16)

        if hash_int < target:
            print(f"Solution found! Nonce: {nonce}, Hash: {hash_hex}")
            requests.post(f"{SERVER}/submit", json={
                "nonce": nonce,
                "hash_hex": hash_hex,
                "hash_int": hash_int
            })
            exit()

    print("No solution in this range. Requesting next...")