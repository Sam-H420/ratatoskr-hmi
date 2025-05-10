<script>
  import { Canvas, Layer } from 'svelte-canvas';
  import { tweened } from 'svelte/motion';
  import { onMount } from 'svelte';
  import { quadOut as easing } from 'svelte/easing';
  import Scene from './Scene.svelte';
  import Toskr from './Toskr.svelte';

  const position = tweened([0.5, 0.5], { duration: 400, easing });

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
  
  onMount(() => {
    const scrolldiv = document.getElementById('canvas-container');

    const handleResize = () => {
      area.width = 500 + scrolldiv.clientWidth;
      area.height = 500 + scrolldiv.clientHeight;
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  });

</script>

<div id="canvas-container" class="h-full w-full items-start justify-start flex overflow-scroll">
  <Canvas width={area.width} height={area.height} style="border: 1px solid black; background-color: black;" layerEvents={ true }>
    <Scene scenary={grid} />
    <Toskr />
  </Canvas>
</div>
