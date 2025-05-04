<script>
  import Win from "../Components/Win.svelte";
  import { onMount } from 'svelte';
  import NumberGauge from "../Components/NumberGauge.svelte";

  let currentReading = $state(null);
  let rframeData = $state(null);
  let tasks = $state(null);
  // let mapData = $state(null);
  // let toskrPos = $state(null);

  let eventSource = $state(undefined);
  let frameSource = $state(undefined);
  let tasksSource = $state(undefined);
  // let mapSource = $state(undefined);
  // let toskrPosSource = $state(undefined);

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

    // const mapResponse = await fetch('http://localhost:8000/map');
    // mapData = await mapResponse.json();

    // const toskrPosResponse = await fetch('http://localhost:8000/position');
    // toskrPos = await toskrPosResponse.json();

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

    // mapSource = new EventSource('http://localhost:8000/mapupdates');
    // mapSource.addEventListener('map_update', (event) => {
    //   mapData = JSON.parse(event.data);
    // });

    // toskrPosSource = new EventSource('http://localhost:8000/positionupdates');
    // toskrPosSource.addEventListener('position_update', (event) => {
    //   toskrPos = JSON.parse(event.data);
    // });

    // add toskr position to map
    // if (mapData && toskrPos) {
    //   cols = mapData.map[0].length;
    //   rows = mapData.map.length;
    //   mapData.map[toskrPos.position.x][toskrPos.position.y] = 2;
    // }

    return () => {
      if (eventSource) {
        eventSource.close();
        frameSource.close();
        tasksSource.close();
        // mapSource.close();
        // toskrPosSource.close();
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

<!-- add task form popup -->
{#if messageShown}
  <div class="absolute top-0 left-0 w-full h-full opacity-80 flex justify-center items-center theme-dark-back">
    <div>
      <h2>Add Task</h2>
      <form onsubmit={createTask} >
        <input type="number" name="id" placeholder="Task ID" />
        <input type="text" name="name" placeholder="Task Name" />
        <input type="text" name="start" placeholder="Start" />
        <input type="text" name="end" placeholder="Goal" />
        <input type="number" name="priority" placeholder="Priority" />
        <button type="submit" >Add Task</button>
      </form>
    </div>
  </div>
{/if}

<div class="flex flex-col md:w-2/3 md:h-full w-full h-1/3 mr-1">
  <div class="flex flex-row md:h-1/2 h-full w-full mb-1">
    <div class="flex w-1/2 mr-1 justify-center items-center theme-dark-container">
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
      <div class="flex w-1/2 ml-1 justify-center items-center theme-dark-container">
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
    <div class="md:flex md:static flex-row h-1/2 w-full mt-1 hidden absolute theme-dark-container">
      <Win title="Tasks">
          {#if tasks}
            <button onclick={() => {
              messageShown = true;
            }} >Add Task</button>
            <ul>
              {#each tasks.tasks as task}
                <li>
                  {task.name}
                  <button onclick={() => {
                    fetch(`http://localhost:8000/tasks/delete?id=${task.id}`)
                    .then(response => response.json())
                    .then(data => {
                      console.log('Task deleted:', data);
                    })
                  }}>Delete</button>
                </li>
              {/each}
            </ul>
          {:else}
            <p>Loading...</p>
          {/if}
        </Win>
    </div>
  </div>

<div class="flex flex-col md:w-1/3 md:h-full w-full h-full ml-1">
  <div class="flex aspect-4/3 w-full mb-1 items-center justify-center theme-dark-container">
    <Win title="Camera">
      {#if rframeData}
        <img src="data:image/jpg;base64,{rframeData.frame}" alt="">
      {/if}
    </Win>
  </div>
  <div class="flex h-full w-full mt-1 items-center justify-center theme-dark-container">
    <Win title="Map">
      <div></div>
      <!-- {#if mapData}
        <div id="map" class="grid grid-rows-{rows} grid-cols-{cols} h-full w-full">
          {#each mapData.map as row}
            {#each row as cell}
              <div class="block h-full w-full {cell === 0 ? 'bg-white' : cell === 1 ? 'bg-black' : 'bg-red-500'}"></div>
            {/each}
          {/each}
        </div>
      {/if} -->
    </Win>
  </div>
</div>