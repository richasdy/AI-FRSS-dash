import json
import math
from models import faces as model_face

def calculate_euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def find_nearest(user_embedding, db_embeddings):
    best_match = None
    smallest_distance = float('inf')

    for row in db_embeddings:
        embedding_str = row.get("embedding")
        if not embedding_str:
            continue
        known_embedding = list(map(float, embedding_str.split(",")))
        if len(known_embedding) != len(user_embedding):
            continue

        distance = calculate_euclidean_distance(user_embedding, known_embedding)
        if distance < smallest_distance:
            smallest_distance = distance
            best_match = {
                "name": row.get("name"),
                "distance": distance
            }

    return best_match

async def verify_face_handler(websocket, msg: dict):
    user_embedding = msg.get("embedding")
    print("Message received:", msg)
    print("Embedding:", user_embedding)

    if not isinstance(user_embedding, list):
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Invalid or missing 'embedding'"
        }
    )
)
        return

    try:
        results = await model_face.get_all_faces()
        match = find_nearest(user_embedding, results)

        if match:
            await websocket.send_text(json.dumps({
                "type": "recognize_face",
                "match": match["distance"] < 0.9,
                "name": match["name"],
                "distance": match["distance"]
            }
        )
    )
        else:
            await websocket.send_text(json.dumps({
                "type": "recognize_face",
                "match": False,
                "name": None,
                "distance": None
            }
        )
    )
    except Exception as e:
        print("Verify face error:", e)
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "Server error during recognition"
        }
    )
)

async def insert_face_handler(websocket, msg: dict):
    try:
        name = msg.get("name")
        embedding = msg.get("embedding")
        print("Message received:", msg)

        if not name or not isinstance(embedding, list):
            await websocket.send_text(json.dumps({
                "type": "insert_face",
                "success": False,
                "message": "Invalid name or embedding format. 'embedding' must be an array."
            }
        )
    )
            return

        embedding_string = ",".join(map(str, embedding))
        await model_face.insert_face(name, embedding_string)

        await websocket.send_text(json.dumps({
            "type": "insert_face",
            "success": True
        }
    )
)
    except Exception as e:
        print("Insert face error:", e)
        await websocket.send_text(json.dumps({
            "type": "insert_face",
            "success": False,
            "message": str(e)
        }
    )
)
