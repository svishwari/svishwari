<template>
  <v-alert
    :color="Type"
    text
    dismissible
    close-icon=""
    :outlined="true"
    height="56"
    width="842"
    class="pb-10 px-8 alert-centered"
  >
    <template #prepend>
      <icon :type="type" size="24" class="mr-2" />
    </template>
    <template #default>
      <div class="d-flex justify-space-between align-center">
        <span class="alert-label text-body-2">{{ label }}</span>
        <a class="alert-more-info text-h6 ml-2 mr-8" :href="to"
          >More information</a
        >
      </div>
    </template>
    <template v-slot:close="{ toggle }">
      <icon type="close-remove" class="cursor-pointer" size="10" @click.native="toggle()" />
    </template>
  </v-alert>
</template>

<script>
import Icon from "../icons/Icon2.vue"
import Button from "../huxButton/huxButton2.vue"

export default {
  name: "Banner",
  components: {
    Icon,
    Button,
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
    Type() {
      switch (this.type) {
        case "positive":
          return "var(--v-success-darken1)"

        case "negative":
          return "var(--v-error-lighten1)"

        case "warning":
          return "var(--v-warning-lighten1)"

        case "guiding":
          return "var(--v-yellow-lighten3)"

        case "offline":
          return "var(--v-black-lighten5)"

        default:
          // informative
          return "var(--v-primary-base)"
      }
    },
  },
}
</script>

<style lang="scss" scoped>
$alert-border-radius: 25px;
.alert-label {
  color: var(--v-black-base);
  max-width: 552px;
  line-height: 20px !important;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
.alert-more-info {
  color: var(--v-primary-lighten7);
  font-weight: bold;
}
.alert-centered {
  margin: 0 auto;
}
</style>
