<template>
  <component :is="dynamicIcon" :width="size" :height="size"/>
</template>

<script>
export default {
  name: "logo",
  props: {
    icon: {
      type: String,
      required: true,
      default: null,
    },
    size: {
      type: String,
      required: false,
      default: "18",
    },
  },
  computed: {
    dynamicIcon() {
      return () => import(`../../assets/logos/${this.icon}.svg`)
    },
  },
}
</script>
