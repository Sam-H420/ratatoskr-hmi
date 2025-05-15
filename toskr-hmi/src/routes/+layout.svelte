<script>
	import '../app.css';
	import { onMount } from 'svelte';
	import logo from '$lib/assets/toskr-logo.svg';
	import BarButton from '../Components/BarButton.svelte';
	import Win from '../Components/Win.svelte';

	const serverUrl = 'http://172.26.197.108:18080';

	/** @type {import('./$types').LayoutProps} */
	let { children } = $props();

	let about = $state(false);

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
		const pingResponse = await fetch(`${serverUrl}/connect`);
		pingData = await pingResponse.json();
		currentReading = pingData;

    // Set up SSE connection
    pingSource = new EventSource(`${serverUrl}/ping`);
		pingSource.addEventListener('ping', (event) => {
			pingData = JSON.parse(event.data);
			timeMs = Date.now();
			seconds = Math.floor((timeMs / 1000) % 60);
			minutes = Math.floor((timeMs / (1000 * 60)) % 60);
			hours = Math.floor((timeMs / (1000 * 60 * 60)) % 24) + 19;
			time = `${hours}:${minutes}:${seconds}`;
		});
    pingSource.addEventListener('status_update', (event) => {
      currentReading = JSON.parse(event.data);
    });

    return () => {
			if (pingSource) pingSource.close();
    };
  });

	function stopToskr() {
		fetch(`${serverUrl}/stop`);		
	}

	function startToskr() {
		fetch(`${serverUrl}/start`)
			.then(response => response.json())
			.then(data => {
				console.log('Start command sent:', data);
			})
			.catch(error => {
				console.error('Error sending start command:', error);
			});		
	}

	async function returnToskr() {
		await fetch(`${serverUrl}/return`)
			.then(response => response.json())
			.then(data => {
				console.log('Return command sent:', data);
			})
			.catch(error => {
				console.error('Error sending return command:', error);
			});		
	}
</script>

<div class="app h-dvh max-h-dvh flex overflow-hidden">
	<div class="flex flex-col h-full w-full overflow-hidden">
		{#if about}
			<div class="absolute top-0 left-0 w-full h-full flex justify-center items-center bg-[#242424b4] z-50">
				<div class="absolute flex justify-center items-center theme-dark-container rounded-md justify-self-center">
					<Win title="About" onclick={() => { about = !about; }} icon="cuida--x-outline">
						<iframe class="p-2" width="560" height="315" src="https://www.youtube.com/embed/fKopy74weus?si=pjRPMNFXNZkJtQCX" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
					</Win>
				</div>
			</div>
		{/if}
		<div class="top-content w-full min-h-10 max-h-10 flex flex-row justify-between items-center p-2 theme-dark-container">
			{#if pingData}
				<p>{time}</p>
				{:else}
				<p>Loading...</p>
			{/if}
			{#if currentReading}
				<p>
					{currentReading.status == 0 ? 'On Duty' : currentReading.status == 1 ? 'Stopped' : 'Returning...'}
				</p>
				{:else}
				<p>Loading...</p>
			{/if}
				<p>Ping</p>
		</div>
	
		<div class="flex flex-grow justify-start items-center theme-dark-back overflow-hidden">
			<div class="flex place-self-stretch flex-col w-20 justify-between items-center p-2 m-2 theme-dark-container rounded-md"> <!-- bg-gradient-to-b from-[#3e3e3e] from-0% to-[#313131] to-1% -->
				<div class="flex flex-col w-full justify-center items-center">
					<img src={logo} alt="TOSKR Logo" class="pb-2" />
					<BarButton title="About" iconClass="cuida--info-outline" onclick={() => {
						about = !about;
						console.log('About clicked');
					}} />
				</div>
				<div>
					{#if currentReading}
						{#if currentReading.status == 0}
							<BarButton title="Stop" iconClass="cuida--power-outline" onclick={stopToskr} />
							<BarButton title="Return" iconClass="cuida--loading-left-outline" onclick={returnToskr} />
						{:else if currentReading.status == 1}
							<BarButton title="Start" iconClass="cuida--power-outline text-[#80b62e]" onclick={startToskr} />
							<BarButton title="Return" iconClass="cuida--loading-left-outline" onclick={returnToskr} />
						{:else if currentReading.status == 2}
							<BarButton title="Stop" iconClass="cuida--power-outline" onclick={stopToskr} />
							<BarButton title="Return" iconClass="cuida--loading-left-outline" onclick={returnToskr} disabled="true" />
						{/if}
					{/if}
				</div>
			</div>
	
			<main class="flex flex-col md:flex-row place-self-stretch justify-stretch items-center m-2 flex-grow gap-2 overflow-hidden">
				{#if pingData}
					{@render children()}
				{:else}
					<p>Loading...</p>
				{/if}
			</main>
		</div>
	</div>
</div>