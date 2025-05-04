<script>
  import '../app.css';

  let { children, title} = $props();
</script>

<div class="flex flex-col w-full h-full justify-start items-center">
  <div class="top-content w-full flex flex-row border-b-1 justify-between items-center p-1 pl-2 pr-2 theme-dark-window">
    {title}
  </div>
  <div class="flex flex-grow h-full w-full justify-center items-center">
    {@render children()}
  </div>
</div>