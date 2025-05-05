<script>
  import '../app.css';

  let { disabled, onclick, title, iconClass } = $props();
</script>

{#if disabled}
  <button class="theme-dark-bar-button" type="button" disabled>
    <div class="p-2 flex flex-col justify-center items-center">
      <span class={iconClass}></span>
      {#if title}
        <p>{title}</p>
      {/if}
    </div>
  </button>
{:else}
  <button onclick={onclick} class="theme-dark-bar-button" type="button" >
    <div class="p-2 flex flex-col justify-center items-center">
      <span class={iconClass}></span>
      {#if title}
        <p>{title}</p>
      {/if}
    </div>
  </button>
{/if}