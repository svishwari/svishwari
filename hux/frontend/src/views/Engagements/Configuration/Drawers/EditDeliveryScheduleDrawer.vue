<template>
  <Drawer v-model="localToggle" :loading="loading">
    <template #header-left>
      <div class="d-flex">
        <v-icon color="primary" size="27">mdi-clock-time-five-outline</v-icon>
        <h3 class="pl-1 text-h3 darkGrey--text">Edit delivery schedule</h3>
      </div>
    </template>

    <template #default>
      <div class="pt-2 pl-4 pr-3">
        <div class="text-h6 neroBlack--text">
          Override the default delivery schedule for this engagement and setup a
          scheduling pattern for this specific destination.
        </div>
        <div class="text-caption gray--text pt-8 pb-1">Destination</div>
        <CardHorizontal
          :title="destination.name"
          :icon="destination.type"
          hideButton
        />
      </div>
    </template>

    <template #footer-left> Left </template>

    <template #footer-right> Right </template>
  </Drawer>
</template>

<script>
import Drawer from "@/components/common/Drawer.vue"
import CardHorizontal from "@/components/common/CardHorizontal.vue"

export default {
  name: "EditDeliverySchedule",

  components: {
    Drawer,
    CardHorizontal,
  },

  props: {
    value: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return {
      loading: false,
      localToggle: false,
      destination: {
        name: "Facebook",
        type: "facebook",
      },
    }
  },

  watch: {
    value(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("input", value)
    },
  },
}
</script>
<style lang="scss" scoped></style>
