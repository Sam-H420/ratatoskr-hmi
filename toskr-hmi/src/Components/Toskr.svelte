<script>
		import { Layer } from 'svelte-canvas'
		
	  const { position } = $props();

	  const render = ({ context, width, height }) => {
      const scrolldiv = document.getElementById('canvas-container');
			const [x, y] = position;
	    context.fillStyle = 'tomato';
	    context.beginPath();
      context.arc(x * (width - scrolldiv.clientWidth) + scrolldiv.clientWidth/2, y * (height - scrolldiv.clientHeight) + scrolldiv.clientHeight/2, 20, 0, 2 * Math.PI);
	    context.fill();

      scrolldiv.scrollTo({
        top: y * (height - scrolldiv.clientHeight),
        left: x * (width - scrolldiv.clientWidth),
      });
	  };
</script>

<Layer {render} />