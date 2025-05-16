<script>
  import { Canvas, Layer } from 'svelte-canvas';
  import { tweened } from 'svelte/motion';
  import { onMount } from 'svelte';
  import { quadOut as easing } from 'svelte/easing';
  import Scene from './Scene.svelte';
  import Toskr from './Toskr.svelte';

  const serverUrl = 'http://192.168.1.16:18080';

  let area = $state({
    width: 500,
    height: 500
  });

  let scenary = $state(null);
  let toskrPos = $state(null);
  let mappingSource = $state(undefined);
  
  onMount(async () => {
    const scrolldiv = document.getElementById('canvas-container');
    const scResponse = await fetch(`/api/mapping`);
    const jsonRes = await scResponse.json();

    scenary = jsonRes;
    toskrPos = jsonRes;

    mappingSource = new EventSource(`/api/mupdates`);
    mappingSource.addEventListener('scene_update', (event) => {
      scenary = JSON.parse(event.data);
    });
    mappingSource.addEventListener('position_update', (event) => {
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
