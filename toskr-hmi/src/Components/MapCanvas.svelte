<script>
  import { Canvas, Layer } from 'svelte-canvas';
  import { tweened } from 'svelte/motion';
  import { onMount } from 'svelte';
  import { quadOut as easing } from 'svelte/easing';
  import Scene from './Scene.svelte';
  import Toskr from './Toskr.svelte';

  const serverUrl = 'http://172.26.197.108:18080';
  // const position = tweened([0.5, 0.5], { duration: 400, easing });

  const grid = Array.from({ length: 8 }, () => Array(8).fill(0));
  // Randomly set some cells to 1
  for (let i = 0; i < 10; i++) {
    const x = Math.floor(Math.random() * 8);
    const y = Math.floor(Math.random() * 8);
    grid[x][y] = 1;
  }

  let area = $state({
    width: 500,
    height: 500
  });

  let scenary = $state(null);
  let scenarySource = $state(undefined);

  let toskrPos = $state(null);
	let toskrPosSource = $state(undefined);
  
  onMount(async () => {
    const scrolldiv = document.getElementById('canvas-container');
    const scResponse = await fetch(`${serverUrl}/scenary`);
    scenary = await scResponse.json();

    const toskResponse = await fetch(`${serverUrl}/toskr`);
    toskrPos = await toskResponse.json();

    // scenarySource = new EventSource(`${serverUrl}/sceneupdates`);
    // scenarySource.addEventListener('scene_update', (event) => {
    //   scenary = JSON.parse(event.data);
    // });

    toskrPosSource = new EventSource(`${serverUrl}/positionupdates`);
    toskrPosSource.addEventListener('position_update', (event) => {
      toskrPos = JSON.parse(event.data);
    });

    const handleResize = () => {
      area.width = 500 + scrolldiv.clientWidth;
      area.height = 500 + scrolldiv.clientHeight;
    };
    window.addEventListener('resize', handleResize);
    handleResize();


    return () => {
      window.removeEventListener('resize', handleResize);
      if (scenarySource) {
        scenarySource.close();
      }
      if (toskrPosSource) {
        toskrPosSource.close();
      }
    };
  });

</script>

<div id="canvas-container" class="h-full w-full items-start justify-start flex overflow-scroll">
  <Canvas width={area.width} height={area.height} style="border: 1px solid black; background-color: black;" layerEvents={ true }>
    {#if scenary}
      <Scene scenary={scenary.map} />
    {/if}
    {#if toskrPos}
      <Toskr position={[toskrPos.toskr[0]/scenary.map.length, toskrPos.toskr[1]/scenary.map[0].length]} />
    {/if}
  </Canvas>
</div>
