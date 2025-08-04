import hashlib
import time

# Simulated block header components
version = "1"
previous_hash = "0000000000000000000000000000000000000000000000000000000000000000"
merkle_root = "4a5e1e"  # fake Merkle root

# Use a fixed recent timestamp to avoid nonce exhaustion issues
timestamp = "1722750000"  # or str(int(time.time()))
bits = 0x1f00ffff

"""0x1d00ffff -- Difficulty 1, same as Bitcoin block #1"""

def bits_to_target(bits):
    """
    Convert compact difficulty format (bits) to a full 256-bit target.
    """
    exponent = bits >> 24
    coefficient = bits & 0xffffff
    target = coefficient * (1 << (8 * (exponent - 3)))
    return target

# Compute the numeric target from bits
target = bits_to_target(bits)
print(f"🎯 Target (hex): {hex(target)}")

def calculate_hash(nonce):
    """
    Construct and hash a fake block header (simplified), double SHA-256.
    """
    header = (
        version +
        previous_hash +
        merkle_root +
        timestamp +
        format(bits, 'x') +
        str(nonce)
    )
    # Double SHA-256
    hash_result = hashlib.sha256(hashlib.sha256(header.encode()).digest()).hexdigest()
    return hash_result

# Mining starts
nonce = 0
start_time = time.time()

while True:
    hash_hex = calculate_hash(nonce)
    hash_int = int(hash_hex, 16)

    # Print first few attempts
    if nonce < 5:
        print(f"Nonce: {nonce} → Hash: {hash_hex}")

    # Progress feedback every 100,000 attempts
    if nonce % 100000 == 0:
        print(f"⏳ Tried {nonce} nonces... Current hash: {hash_hex[:16]}...")

    if hash_int < target:
        print(f"\n✅ Block mined!")
        print(f"Nonce: {nonce}")
        print(f"Hash: {hash_hex}")
        break

    nonce += 1

end_time = time.time()
print(f"⏱️ Time taken: {end_time - start_time:.2f} seconds")
