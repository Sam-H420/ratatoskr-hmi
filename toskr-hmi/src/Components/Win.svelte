<script>
  import '../app.css';

  let { children, title, onclick, icon} = $props();
</script>

<div class="flex flex-col w-full h-full justify-start items-center overflow-hidden">
  <div class="top-content w-full flex flex-row justify-between items-center p-1 pl-4 pr-2 theme-dark-window">
    {title}
    {#if onclick}
      <button type="button" onclick={onclick} aria-label="Window Action" class="theme-dark-window-button" >
        <div class="p-2 flex flex-col justify-center items-center">
          <span class={icon}></span>
        </div>
      </button>
    {/if}
  </div>
  <div class="flex flex-grow h-full w-full justify-center items-center overflow-hidden">
    {@render children()}
  </div>
</div>