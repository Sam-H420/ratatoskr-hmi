<script>
	import '../app.css';
	import { onMount } from 'svelte';

	/** @type {import('./$types').LayoutProps} */
	let { children } = $props();

	let pingData = $state(null);
	let pingSource = $state(undefined);
  let currentReading = $state(null);
  let eventSource = $state(undefined);
	let time = $state(undefined);

	let timeMs = $state(undefined);
	let seconds = $state(undefined);
	let minutes = $state(undefined);
	let hours = $state(undefined);

  onMount(async () => {
    // Initial data fetch
		const pingResponse = await fetch('http://localhost:8000/connect');
		pingData = await pingResponse.json();

    const response = await fetch('http://localhost:8000/status');
    currentReading = await response.json();

    // Set up SSE connection
    pingSource = new EventSource('http://localhost:8000/ping');
		pingSource.addEventListener('ping', (event) => {
			pingData = JSON.parse(event.data);
			timeMs = Date.now();
			seconds = Math.floor((timeMs / 1000) % 60);
			minutes = Math.floor((timeMs / (1000 * 60)) % 60);
			hours = Math.floor((timeMs / (1000 * 60 * 60)) % 24);
			time = `${hours}:${minutes}:${seconds}`;
		});
		
		eventSource = new EventSource('http://localhost:8000/statusupdate');
    eventSource.addEventListener('status_update', (event) => {
      currentReading = JSON.parse(event.data);
    });

    return () => {
      if (eventSource) eventSource.close();
    };
  });

	function stopToskr() {
		fetch('http://localhost:8000/stop')
			.then(response => response.json())
			.then(data => {
				console.log('Stop command sent:', data);
			})
			.catch(error => {
				console.error('Error sending stop command:', error);
			});		
	}

	function startToskr() {
		fetch('http://localhost:8000/start')
			.then(response => response.json())
			.then(data => {
				console.log('Start command sent:', data);
			})
			.catch(error => {
				console.error('Error sending start command:', error);
			});		
	}

	function returnToskr() {
		fetch('http://localhost:8000/return')
			.then(response => response.json())
			.then(data => {
				console.log('Return command sent:', data);
			})
			.catch(error => {
				console.error('Error sending return command:', error);
			});		
	}
</script>

<div class="app min-h-dvh flex flex-col">
		<div class="top-content w-full flex flex-row justify-between items-center p-2 theme-dark-container">
			{#if pingData}
				<p>{time}</p>
				{:else}
				<p>Loading...</p>
			{/if}
			{#if currentReading}
				<p>Status: {currentReading.status}</p>
				{:else}
				<p>Loading...</p>
			{/if}
				<p>Ping</p>
		</div>

		<div class="flex flex-grow justify-start items-center content-stretch theme-dark-back">
				<div class="flex place-self-stretch flex-col w-20 justify-between items-center p-2 m-2 theme-dark-container">
					<div>
						<p>Logo</p>
						<p>About</p>
					</div>
					<div>
						{#if currentReading}
							{#if currentReading.status == 0}
								<button onclick={stopToskr} type="button" >Stop</button>
							{:else if currentReading.status == 1}
								<button onclick={startToskr} type="button" >Start</button>
							{:else if currentReading.status == 2}
								<button onclick={stopToskr} type="button" >Stop</button>
							{/if}
							<button onclick={returnToskr} type="button" >Return</button>
						{/if}
					</div>
				</div>
	
				<main class="flex flex-col md:flex-row place-self-stretch justify-stretch items-center m-2 w-full">
					{#if pingData}
						{@render children()}
					{:else}
						<p>Loading...</p>
					{/if}
				</main>
		</div>
</div>