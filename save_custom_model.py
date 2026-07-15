# ==========================================
# SQLite Settings Writer (Custom Model Injector)
# Created by Neps
# ==========================================

import sqlite3
import base64
import sys

# =====================================================================
# CONFIGURATION: Customize your model settings here
# =====================================================================
MODEL_LABEL = "OpenRouter-Claude"           # Display name in the dropdown
BASE_URL = "http://localhost:8000/"        # Points to local_proxy.py
MAX_TOKENS = 1000000                       # Large value to avoid token limits
# =====================================================================

def encode_varint(value):
    out = bytearray()
    while value >= 0x80:
        out.append((value & 0x7f) | 0x80)
        value >>= 7
    out.append(value & 0x7f)
    return bytes(out)

def encode_field(field_number, wire_type, value):
    header = encode_varint((field_number << 3) | wire_type)
    if wire_type == 0:
        return header + encode_varint(value)
    elif wire_type == 2:
        return header + encode_varint(len(value)) + value
    else:
        raise ValueError("Unsupported wire type")

# Construct ModelFeatures
model_features_bytes = (
    encode_field(1, 0, 1) +  # zeroShotCapable = true
    encode_field(2, 0, 1) +  # supportsImages = true
    encode_field(3, 0, 1) +  # supportsToolCalls = true
    encode_field(4, 0, 1)    # supportsThinking = true
)

# Construct ModelInfo
model_info_bytes = (
    encode_field(1, 0, 326) +  # modelId = GOOGLE_GEMINI_INTERNAL_BYOM (326)
    encode_field(2, 0, 30) +   # apiProvider = API_PROVIDER_GOOGLE_EVERGREEN (30)
    encode_field(3, 2, MODEL_LABEL.encode('utf-8')) +  # chatModelName
    encode_field(4, 2, BASE_URL.encode('utf-8')) +     # modelName (URL)
    encode_field(5, 0, MAX_TOKENS) +                   # maxTokens
    encode_field(6, 2, model_features_bytes)
)

# Construct CustomModels map entry
map_entry_bytes = (
    encode_field(1, 2, MODEL_LABEL.encode('utf-8')) +
    encode_field(2, 2, model_info_bytes)
)

custom_models_bytes = encode_field(1, 2, map_entry_bytes)
custom_models_b64 = base64.b64encode(custom_models_bytes).decode('utf-8')

# Construct Topic map entry for "custom_models" key
row_bytes = encode_field(1, 2, custom_models_b64.encode('utf-8'))
topic_map_entry_bytes = (
    encode_field(1, 2, b"custom_models") +
    encode_field(2, 2, row_bytes)
)

# Open state.vscdb and update modelPreferences
db_path = r'C:\Users\nepal\AppData\Roaming\Antigravity IDE\User\globalStorage\state.vscdb'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT value FROM ItemTable WHERE key = 'antigravityUnifiedStateSync.modelPreferences'")
row = cursor.fetchone()
if not row:
    print("ERROR: modelPreferences key not found in database!")
    sys.exit(1)

existing_b64 = row[0]
existing_bytes = base64.b64decode(existing_b64)

# Append the new custom_models entry to the existing serialized protobuf
new_bytes = existing_bytes + topic_map_entry_bytes
new_b64 = base64.b64encode(new_bytes).decode('utf-8')

cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'antigravityUnifiedStateSync.modelPreferences'", (new_b64,))
conn.commit()
conn.close()

print(f"SUCCESS: Manually saved custom model '{MODEL_LABEL}' into state.vscdb!")
print(f"Endpoint: {BASE_URL}")
print(f"Max Tokens: {MAX_TOKENS}")
