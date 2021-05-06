<template>
  <div class="text-center mt-14">
    <div class="chart-image">
       <slot name="chart-image"></slot>
    </div>
    <div class="ruler-image">
      <img src="@/assets/images/pencil-ruler.png" alt="pencil-ruler" />
    </div>
    <div class="text-subtitle-2">
        Exciting visuals are in the works!
    </div>
    <div class="text-subtitle-1">
        Hang tight as our devs work hard to update this section
    </div>
  </div>
</template>

<script>
export default {
  name: "empty-state",
}
</script>
