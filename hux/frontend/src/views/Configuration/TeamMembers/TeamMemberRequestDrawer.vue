<template>
  <drawer v-model="localToggle" :width="600" :loading="loading">
    <template #header-left>
        <div class="d-flex align-center">
            <icon
                type="team-member-drawer"
                :size="32"
                class="mr-3"
            />
            <h3 class="text-h2">Request a team member to add</h3>
        </div>
    </template>

    <template #default>
        <div class="pa-6">
        <span class="body-1">Provide the information about the new team member. </span>
        </div>
    </template>

    <template #footer-left>
      <hux-button
          variant="white"
          size="large"
          :is-tile="true"
          class="mr-2 btn-border box-shadow-none"
          @click="closeDrawer"
        >
          <span class="primary--text">Cancel</span>
        </hux-button>
    </template>
    <template #footer-right>
      <div
        class="d-flex align-baseline"
      >
        <hux-button
          variant="primary"
          size="large"
          :is-tile="true"
          :is-disabled="false"
          @click="addSelectedAudiences"
        >
          Request
        </hux-button>
      </div>
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Drawer from "@/components/common/Drawer.vue"
import HuxButton from "@/components/common/huxButton.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import Icon from "@/components/common/Icon.vue"

export default {
  name: "AudiencesDrawer",

  components: {
    Drawer,
    HuxButton,
    Tooltip,
    Icon,
  },

  props: {
    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      localToggle: false,
      loading: false,
    }
  },

  computed: {
    ...mapGetters({
    }),
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },
  },

  methods: {
    ...mapActions({
    }),
    closeDrawer() {
      this.localToggle = false
      this.localSelectedAudiences = this.value
    },
  },
}
</script>

<style lang="scss" scoped>

</style>
