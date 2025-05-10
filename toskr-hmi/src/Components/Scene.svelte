<script>
  import { Layer } from "svelte-canvas";
  
  const { scenary } = $props();

  const render = ({ context, width, height }) => {
    const scrolldiv = document.getElementById('canvas-container');
    const grid = scenary.map(row => row.map(cell => cell === 1 ? true : false));
    const area = {
      width: width - scrolldiv.clientWidth,
      height: height - scrolldiv.clientHeight,
    }

    const cellWidth = (area.width / scenary.length);  
    const cellHeight = (area.height / scenary[0].length);

    for (let i = 0; i < scenary.length; i++) {
      for (let j = 0; j < scenary[0].length; j++) {
        context.fillStyle = grid[i][j] ? 'black' : 'white';
        context.fillRect(i * cellWidth + scrolldiv.clientWidth/2 - cellWidth/2, j * cellHeight + scrolldiv.clientHeight/2 - cellHeight/2, 2*cellWidth, 2*cellHeight);
      }
    }
  };
</script>

{#if scenary}
<Layer {render} />
{/if}