<script>
		import { Layer } from 'svelte-canvas'
		import { onMount } from 'svelte';
	  import { tweened } from 'svelte/motion';

	  const position = tweened([0.5, 0.5], { duration: 400 });

	  onMount(() => {
	    setInterval(() => ($position = [Math.random(), Math.random()]), 800);
	  });

	  $: render = ({ context, width, height }) => {
      const scrolldiv = document.getElementById('canvas-container');
			const [x, y] = $position;
      // const [x, y] = [0.5, 0.5]; // For testing purposes, set a fixed position
	    context.fillStyle = 'tomato';
	    context.beginPath();
      context.arc(x * (width - scrolldiv.clientWidth) + scrolldiv.clientWidth/2, y * (height - scrolldiv.clientHeight) + scrolldiv.clientHeight/2, 20, 0, 2 * Math.PI);
	    context.fill();

      scrolldiv.scrollTo({
        top: y * (height - scrolldiv.clientHeight),
        left: x * (width - scrolldiv.clientWidth),
      });

      console.log('Scroll position:', scrolldiv.scrollTop, scrolldiv.scrollLeft);
	  };
</script>

<Layer {render} />