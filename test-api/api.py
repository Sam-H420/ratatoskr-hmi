import asyncio
import json
import uvicorn
import cv2
import base64
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from data import ToskrData, TaskList, Task, MapData


app = FastAPI()
toskr_data = ToskrData()

laststatus = toskr_data.getStatus()

toskr_tasks = TaskList(
    [
        Task(0, "Task 1", "A", "B"),
        Task(1, "Task 2", "B", "C"),
        Task(2, "Task 3", "C", "A"),
    ]
)

last_task_list = toskr_tasks.getTasks()

# Initialize the map
map_data = MapData([
    [1,1,1,1,1,1,1,1],
    [1,0,1,1,1,0,1,1],
    [1,0,1,1,1,0,1,1],
    [1,0,1,1,1,0,1,1],
    [1,0,0,0,0,0,1,1],
    [1,0,1,1,0,1,1,1],
    [1,0,1,1,0,1,1,1],
    [1,1,1,1,1,1,1,1],
], {
    "x": 0,
    "y": 0
})

last_map_data = map_data.getMap()
last_position = map_data.getPosition()

def get_frame():
    """Get the video frame."""
    camera = cv2.VideoCapture(0)  # Open the camera
    
    while True:
        retval, im = camera.read()
        imgencode = cv2.imencode('.jpg', im)[1]
        stringData = base64.b64encode(imgencode)
        yield ({
            "event": "frame_update",
            "data": json.dumps({
                "frame": stringData.decode('utf-8')
            })
        })

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Svelte dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Dashboard API"}

@app.get("/frame")
async def frame():
    """Get the video frame."""
    camera = cv2.VideoCapture(0)  # Open the camera
    retval, im = camera.read()
    imgencode = cv2.imencode('.jpg', im)[1]
    stringData = base64.b64encode(imgencode)
    return {"frame": stringData.decode('utf-8')}

@app.get("/vid")
async def video_feed():
    """Video feed endpoint."""
    return EventSourceResponse(get_frame())

@app.get("/speed/{speed}")
async def set_speed(speed: float):
    """Set the speed of the toskr."""
    data = toskr_data.setSpeed(speed)
    return {"speed": data}

app.get("/battery/{battery}")
async def set_battery(battery: float):
    """Set the battery of the toskr."""
    data = toskr_data.setBattery(battery)
    return {"battery": data}

@app.get("/stop")
async def stop_toskr():
    """Stop the toskr."""
    data = toskr_data.setStatus(1)
    return {"status": data}

@app.get("/start")
async def start_toskr():
    """Start the toskr."""
    data = toskr_data.setStatus(0)
    return {"status": data}

@app.get("/return")
async def return_toskr():
    """Return the toskr."""
    data = toskr_data.setStatus(2)
    return {"status": data}

@app.get("/status")
async def get_status():
    """Get the current status of the toskr."""
    data = toskr_data.getStatus()
    return data

@app.get("/statusupdate")
async def status_update():
    """Stream status updates using server-sent events."""
    async def event_generator():
        while True:
            data = toskr_data.getStatus()
            global laststatus
            if data == laststatus:
                await asyncio.sleep(0.01)
                continue
            else:
                laststatus = data
                yield {
                    "event": "status_update",
                    "data": json.dumps(data)
                }
                await asyncio.sleep(0.01)
    return EventSourceResponse(event_generator())

@app.get("/current")
async def get_current_reading():
    """Get the current toskr reading."""
    data = toskr_data.getData(0)
    return data

@app.get("/stream")
async def stream_data():
    """Stream sensor data using server-sent events."""
    async def event_generator():
        time = 0
        while True:
            data = toskr_data.getData(time)  # Replace with actual time if needed
            yield {
                "event": "sensor_update",
                "data": json.dumps(data)
            }
            await asyncio.sleep(0.01)  # Update every 2 seconds
            time += 0.01

    return EventSourceResponse(event_generator())

@app.get("/tasks")
async def get_tasks():
    """Get the list of tasks."""
    tasks = toskr_tasks.getTasks()
    return {"tasks": tasks}

# ?id={task_id}&name={task_name}&start={task_start}&end={task_end}&priority={task_priority}

@app.get("/tasks/create")
async def create_task(id: int, name: str, start: str, end: str, priority: int | None = 0):
    """Create a new task."""
    toskr_tasks.addTask(Task(id, name, start, end, priority))
    return {"message": "Task created successfully"}

@app.get("/tasks/delete")
async def delete_task(id: int):
    """Delete a task."""
    toskr_tasks.removeTask(id)
    return {"message": "Task deleted successfully"}

@app.get("/tasks/update")
async def update_task(id: int, status: int):
    """Update a task's status."""
    toskr_tasks.updateTaskStatus(id, status)
    return {"message": "Task updated successfully"}

@app.get("/taskstream")
async def task_stream():
    """Stream task data using server-sent events."""
    async def event_generator():
        while True:
            global last_task_list
            if toskr_tasks.getTasks() is None or toskr_tasks.getTasks() == last_task_list:
                await asyncio.sleep(0.01)
                continue
            else:
                last_task_list = toskr_tasks.getTasks()
                tasks = toskr_tasks.getTasks()
                yield {
                    "event": "task_update",
                    "data": json.dumps({"tasks": tasks})
                }
                await asyncio.sleep(0.01)
    return EventSourceResponse(event_generator())

@app.get("/map")
async def get_map():
    """Get the map data."""
    map = map_data.getMap()
    return {"map": map}

@app.get("/mapupdates")
async def map_updates():
    """Stream map updates using server-sent events."""
    async def event_generator():
        while True:
            global last_map_data
            map = map_data.getMap()
            if map is None or map == last_map_data:
                await asyncio.sleep(0.01)
                continue
            else:
                last_map_data = map
                yield {
                    "event": "map_update",
                    "data": json.dumps({"map": map})
                }
                await asyncio.sleep(0.01)
    return EventSourceResponse(event_generator())

@app.get("/position")
async def get_position():
    """Get the current position of the toskr."""
    position = map_data.getPosition()
    return {"position": position}

@app.get("/setposition")
async def set_position(x: int, y: int):
    """Set the position of the toskr."""
    map_data.setPosition(x, y)
    return {"position": (x, y)}

@app.get("/positionupdates")
async def position_updates():
    """Stream position updates using server-sent events."""
    async def event_generator():
        while True:
            global last_position
            position = map_data.getPosition()
            if position is None or position == last_position:
                await asyncio.sleep(0.01)
                continue
            else:
                last_map_data = position
                yield {
                    "event": "position_update",
                    "data": json.dumps({"position": position})
                }
                await asyncio.sleep(0.01)
    return EventSourceResponse(event_generator())

@app.get("/ping")
async def ping():
    """stream ping updates using server-sent events."""
    async def event_generator():
        while True:
            data = "pong"
            yield {
                "event": "ping",
                "data": json.dumps(data)
            }
            await asyncio.sleep(0.01)
    return EventSourceResponse(event_generator())

@app.get("/connect")
async def connect():
    """Connect to the server."""
    async def event_generator():
        return "pong"

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)