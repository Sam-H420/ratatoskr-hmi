<script>
  import '../app.css';
  import Win from "../Components/Win.svelte";
  import { onMount } from 'svelte';
  import NumberGauge from "../Components/NumberGauge.svelte";
  import MapCanvas from '../Components/MapCanvas.svelte';

  let currentReading = $state(null);
  let rframeData = $state(null);
  let tasks = $state(null);

  let eventSource = $state(undefined);
  let frameSource = $state(undefined);
  let tasksSource = $state(undefined);

  let messageShown = $state(false);
  let cols = $state(0);
  let rows = $state(0);

  onMount(async () => {
    // Initial data fetch
    const response = await fetch('http://localhost:8000/current');
    currentReading = await response.json();

    const rframe = await fetch('http://localhost:8000/frame');
    rframeData = await rframe.json();

    const tasksResponse = await fetch('http://localhost:8000/tasks');
    tasks = await tasksResponse.json();

    // Set up SSE connection
    eventSource = new EventSource('http://localhost:8000/stream');
    eventSource.addEventListener('sensor_update', (event) => {
      currentReading = JSON.parse(event.data);
    });

    frameSource = new EventSource('http://localhost:8000/vid');
    frameSource.addEventListener('frame_update', (event) => {
      rframeData = JSON.parse(event.data);
    });

    tasksSource = new EventSource('http://localhost:8000/taskstream');
    tasksSource.addEventListener('task_update', (event) => {
      tasks = JSON.parse(event.data);
    });

    return () => {
      if (eventSource) {
        eventSource.close();
        frameSource.close();
        tasksSource.close();
      }
    };
  });

  function createTask(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
      id: formData.get('id'),
      name: formData.get('name'),
      start: formData.get('start'),
      end: formData.get('end'),
      priority: formData.get('priority')
    };
    fetch(`http://localhost:8000/tasks/create?id=${data.id}&name=${data.name}&start=${data.start}&end=${data.end}&priority=${data.priority}`)
      .then(response => response.json())
      .then(data => {
        console.log('Task created:', data);
        messageShown = false;
      })
      .catch(error => {
        console.error('Error creating task:', error);
      });
  }
</script>

{#if messageShown}
  <div class="absolute top-0 left-0 w-full h-full flex justify-center items-center bg-[#242424b4] z-50">
    <div class="absolute flex justify-center items-center theme-dark-container rounded-md justify-self-center">
      <Win title="Add Task" onclick={() => { messageShown = !messageShown; }} icon="cuida--x-outline">
        <form onsubmit={createTask} class="flex flex-col w-full h-full justify-center items-center p-4 gap-2">
          <input type="number" name="id" placeholder="Task ID" class="theme-dark-input" />
          <input type="text" name="name" placeholder="Task Name" class="theme-dark-input" />
          <input type="text" name="start" placeholder="Start" class="theme-dark-input" />
          <input type="text" name="end" placeholder="Goal" class="theme-dark-input" />
          <input type="number" name="priority" placeholder="Priority" class="theme-dark-input" />
          <button type="submit" class="theme-dark-window-button p-2" >Add Task</button>
        </form>
      </Win>
    </div>
  </div>
{/if}

<div class="flex flex-col md:w-2/3 md:h-full w-full h-1/3">
  <div class="flex flex-row md:h-1/2 h-full w-full mb-1">
    <div class="flex w-1/2 mr-1 justify-center items-center theme-dark-container rounded-md">
      <Win title="Speed">
        <div class="flex" style="font-size: 4em;">
          {#if currentReading}
          <NumberGauge value={currentReading.speed} arrows={currentReading.speed} />
          {:else}
            <p>Loading...</p>
          {/if}
        </div>
      </Win>
    </div>
    <div class="flex w-1/2 ml-1 justify-center items-center theme-dark-container rounded-md">
      <Win title="Battery">
        <div class="flex" style="font-size: 4em;">
          {#if currentReading}
            <NumberGauge value={currentReading.battery} arrows={currentReading.battery} />
          {:else}
            <p>Loading...</p>
          {/if}
        </div>
      </Win>
    </div>
  </div>
  <div class="md:flex md:static flex-row h-1/2 w-full mt-1 hidden absolute theme-dark-container rounded-md">
    <Win title="Tasks" onclick={() => {messageShown = true;}} icon="cuida--plus-outline">
      <div class="flex h-full w-full overflow-y-scroll">
        {#if tasks}
          <ul class="flex flex-col w-full">
            {#each tasks.tasks as task}
              <li class="flex flex-row w-full justify-between items-center p-2 pl-4 border-b-1 border-[#242424]">
                <div class="flex flex-row w-full justify-start items-center">
                  {task.id}
                  <div class="flex flex-col w-full ml-5">
                    <p>{task.name}</p>
                    <p class="text-[#747474]">{task.start} - {task.end}</p>
                  </div>
                </div>
                <button onclick={() => {
                  fetch(`http://localhost:8000/tasks/delete?id=${task.id}`)
                  .then(response => response.json())
                  .then(data => {
                    console.log('Task deleted:', data);
                  })
                }} aria-label="Deelete Task" class="theme-dark-window-button">
                  <div class="p-2 flex flex-col justify-center items-center">
                    <span class="cuida--trash-outline"></span>
                  </div>
                </button>
              </li>
            {/each}
          </ul>
        {:else} 
          <p>Loading...</p>
        {/if}
      </div>
      </Win>
  </div>
</div>

<div class="flex flex-col md:w-1/3 md:h-full w-full h-full overflow-hidden">
  <div class="flex aspect-3/4 w-full mb-1 items-center justify-center theme-dark-container rounded-md">
    <Win title="Camera">
      {#if rframeData}
        <img src="data:image/jpg;base64,{rframeData.frame}" alt="">
      {/if}
    </Win>
  </div>
  <div class="relative flex w-full h-full mt-1 items-center justify-center theme-dark-container rounded-md">
    <Win title="Map">
      <MapCanvas />
    </Win>
  </div>
</div>