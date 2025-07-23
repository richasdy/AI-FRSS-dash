import asyncio
import websockets
import json
import sys

async def test_websocket_connection():
    """Test basic WebSocket connection to all models"""
    models = ["intrusion", "people", "security_threats", "vehicle"]
    
    print("🚀 Testing WebSocket connections...")
    
    for model in models:
        try:
            uri = f"ws://localhost:8000/ws/detection/{model}"
            print(f"\n📡 Testing {model} model at {uri}")
            
            async with websockets.connect(uri) as websocket:
                # Wait for connection message
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                
                if data.get("type") == "connection_established":
                    print(f"✅ {model}: {data.get('message')}")
                else:
                    print(f"⚠️ {model}: Unexpected response: {data}")
                
                # Send ping test
                ping_msg = {
                    "type": "ping",
                    "timestamp": "2025-07-21T10:30:00Z"
                }
                
                await websocket.send(json.dumps(ping_msg))
                pong_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                pong_data = json.loads(pong_response)
                
                if pong_data.get("type") == "pong":
                    loaded_models = pong_data.get("loaded_models", [])
                    print(f"🏓 {model}: Pong received, loaded models: {loaded_models}")
                else:
                    print(f"❌ {model}: No pong response")
                    
        except asyncio.TimeoutError:
            print(f"⏰ {model}: Connection timeout")
        except websockets.exceptions.ConnectionRefused:
            print(f"❌ {model}: Connection refused")
        except Exception as e:
            print(f"🚨 {model}: Error - {e}")
    
    # Test multi-model endpoint
    try:
        print(f"\n🌟 Testing multi-model endpoint...")
        uri = "ws://localhost:8000/ws/detection-all"
        
        async with websockets.connect(uri) as websocket:
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(response)
            
            if data.get("type") == "connection_established":
                available_models = data.get("available_models", [])
                print(f"✅ Multi-model: Connected with models: {available_models}")
            else:
                print(f"⚠️ Multi-model: Unexpected response: {data}")
                
            # Send ping
            ping_msg = {"type": "ping", "timestamp": "2025-07-21T10:30:00Z"}
            await websocket.send(json.dumps(ping_msg))
            
            pong_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            pong_data = json.loads(pong_response)
            
            if pong_data.get("type") == "pong":
                loaded_models = pong_data.get("loaded_models", [])
                print(f"🏓 Multi-model: Pong received, loaded models: {loaded_models}")
            
    except Exception as e:
        print(f"🚨 Multi-model: Error - {e}")
    
    print(f"\n🎯 WebSocket test completed!")

if __name__ == "__main__":
    try:
        asyncio.run(test_websocket_connection())
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed: {e}")
        sys.exit(1)
