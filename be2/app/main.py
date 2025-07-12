from fastapi import FastAPI, WebSocket, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from transformers import BertTokenizer, BertModel, pipeline
from PIL import Image, ImageDraw
import io
import base64
import torch

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is running! 🎉 Check /docs for endpoints."}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

tokenizer = BertTokenizer.from_pretrained('indobenchmark/indobert-base-p1')
bert_model = BertModel.from_pretrained('indobenchmark/indobert-base-p1')

object_detector = pipeline("object-detection", model="facebook/detr-resnet-50")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            inputs = tokenizer(data, return_tensors="pt")
            with torch.no_grad():
                outputs = bert_model(**inputs)
            pooled = outputs.pooler_output.detach().numpy().tolist()
            await websocket.send_text(f"Embedding shape: {len(pooled)}x{len(pooled[0])}")
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        await websocket.close()

@app.post("/encode")
async def encode_text(request: Request):
    data = await request.json()
    text = data.get("text", "")
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = bert_model(**inputs)
    pooled = outputs.pooler_output.detach().numpy().tolist()
    return {"embedding": pooled}

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    try:
        image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    except Exception as e:
        return {"error": f"Invalid image: {str(e)}"}
    results = object_detector(image)
    draw = ImageDraw.Draw(image)
    for obj in results:
        box = obj['box']
        draw.rectangle([box['xmin'], box['ymin'], box['xmax'], box['ymax']], outline="red", width=3)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.websocket("/ws-image")
async def websocket_image(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            img_bytes = base64.b64decode(data)
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            results = object_detector(image)
            draw = ImageDraw.Draw(image)
            for obj in results:
                box = obj['box']
                draw.rectangle([box['xmin'], box['ymin'], box['xmax'], box['ymax']], outline="red", width=3)
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode("utf-8")
            await websocket.send_text(img_b64)
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        await websocket.close()
