<script>
  import '../app.css';

  let { children, title, onclick} = $props();
</script>

<div class="flex flex-col w-full h-full justify-start items-center">
  <div class="top-content w-full flex flex-row border-b-1 justify-between items-center p-1 pl-2 pr-2 theme-dark-window">
    {title}
    {#if onclick}
      <button type="button" onclick={onclick} aria-label="Close window">
        <div class="p-2 flex flex-col justify-center items-center">
          <span class="cuida--x-outline"></span>
        </div>
      </button>
    {/if}
  </div>
  <div class="relative flex flex-grow h-full w-full justify-center items-center">
    {@render children()}
  </div>
</div>