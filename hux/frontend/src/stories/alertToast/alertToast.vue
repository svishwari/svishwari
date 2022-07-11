<template>
  <v-alert
    :color="'var(--v-' + bgColor + ')'"
    text
    dismissible
    :outlined="true"
    height="56"
    width="842"
    class="px-8 alert-centered"
  >
    <template #prepend>
      <icon
        :type="type == 'Informative' ? 'Error & Warning' : type"
        :size="24"
        :color="
          type == 'Guide' || type == 'Error & Warning'
            ? 'black-lighten6'
            : 'white-base'
        "
        :bg-color="bgColor"
        :border-color="bgColor"
        outline
        class="mr-2"
      />
    </template>
    <template #default>
      <div class="d-flex align-center">
        <span class="alert-label text-body-2">{{ label }}</span>
        <a class="alert-more-info text-h6 ml-2 mr-8" :href="to"
          >More information</a
        >
      </div>
    </template>
    <template v-slot:close="{ toggle }">
      <icon
        type="Close & Remove"
        color="black"
        class="cursor-pointer"
        size="16"
        @click.native="toggle()"
      />
    </template>
  </v-alert>
</template>

<script>
import Icon from "../icons/Icon2.vue"

export default {
  name: "AlertToast",
  components: {
    Icon,
  },
  props: {
    label: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      required: false,
      default: "warning",
    },
    to: {
      type: String,
      required: false,
      default: "/",
    },
  },
  data: () => ({
    alertToast: true,
  }),
  computed: {
    bgColor() {
      switch (this.type) {
        case "Checkmark":
          return "success-darken1"

        case "Error":
          return "error-lighten1"

        case "Error & Warning":
          return "warning-lighten1"

        case "Guide":
          return "yellow-lighten3"

        case "Offline":
          return "black-lighten5"

        default:
          // informative
          return "primary-base"
      }
    },
  },
}
</script>

<style lang="scss" scoped>
$alert-border-radius: 25px;
.alert-label {
  color: var(--v-black-base);
  line-height: 20px !important;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
.alert-more-info {
  color: var(--v-primary-lighten7);
  font-weight: bold;
  line-height: 20px;
}
.alert-centered {
  margin: 0 auto;
}
</style>
