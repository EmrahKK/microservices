from fastapi import FastAPI, Request
import psutil
import time
import logging
import math

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/events")
async def receive_event(request: Request):
    try:
        body = await request.json()  # Parse the JSON body
        logger.info(f"Received event: {body}")  # Log the body to the console
        return {"message": "Event received successfully"}
    except Exception as e:
        logger.error(f"Failed to process request: {e}")
        return {"error": "Invalid JSON body"}
# Endpoint 1: Service status and system information
@app.get("/status")
def get_status():
    uptime = time.time() - psutil.boot_time()
    free_memory = psutil.virtual_memory().available
    total_memory = psutil.virtual_memory().total
    cpu_count = psutil.cpu_count()

    return {
        "message": "Service is up and running",
        "uptime": f"{int(uptime)} seconds",
        "system_info": {
            "total_memory": f"{total_memory / 1024 / 1024:.2f} MB",
            "free_memory": f"{free_memory / 1024 / 1024:.2f} MB",
            "cpus": cpu_count,
        }
    }
