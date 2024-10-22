from fastapi import FastAPI
import psutil
import time
import math
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

# Memory hog variable
memory_hog = []

# Executor for CPU-intensive tasks
executor = ThreadPoolExecutor(max_workers=2)

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

# Endpoint 2: Increase memory usage by 100MB
@app.get("/memory-hog")
def memory_hogging():
    # Allocate 100MB of memory
    size = 100 * 1024 * 1024
    memory_hog.append(bytearray(size))  # Store in the list to prevent garbage collection
    return {"message": "Memory hog"}

# Function to simulate CPU-intensive task
def cpu_hog(duration: int):
    start_time = time.time()
    while time.time() - start_time < duration:
        for i in range(1_000_000):
            math.sqrt(i)

# Endpoint 3: Non-blocking CPU-intensive task (CPU Hog)
@app.get("/cpu-hog")
async def cpu_hogging():
    duration = 240  # 1 minute

    # Schedule the CPU-intensive task in the background
    asyncio.create_task(cpu_hog_task(duration))

    # Send the response immediately without waiting
    return {"message": "CPU hog task started (non-blocking)"}

# Helper function to run CPU-hog task in an executor
async def cpu_hog_task(duration):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, cpu_hog, duration)