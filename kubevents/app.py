from fastapi import FastAPI, Request
import logging

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
