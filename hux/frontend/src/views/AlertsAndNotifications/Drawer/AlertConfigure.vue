<template>
  <drawer
    v-model="localDrawer"
    :content-padding="'pa-0'"
    :content-header-padding="'px-3'"
  >
    <template #header-left>
      <div v-if="getNotificationPreferences" class="d-flex align-center">
        <icon
          type="setting-gear-border"
          :size="32"
          color="black"
          class="d-block mr-2 black-border"
        />
        <h3 class="text-h2 ml-1 black--text text--darken-4">
          Configure alerts
        </h3>
      </div>
    </template>
    <template #default>
      <div class="px-6 py-4">
        <div class="text-body-1 pb-4">
          Configure if you wish to recieve Hux notifications and alerts via
          email.
        </div>
        <div class="d-flex full-alert text-body-1 pb-4">
          Do you wish to receive alerts?
          <hux-switch
            v-model="showAlerts"
            false-color="var(--v-black-lighten4)"
            :width="showAlerts ? '57px' : '60px'"
            :switch-labels="switchLabelFullAlerts"
            class="w-53"
            @input="toggleAccess($event, item)"
          />
        </div>
        <div class="pb-4">
          <text-field
            v-model="getCurrentUserEmail"
            label-text="Email"
            input-type="text"
            height="40"
            :disabled="true"
            required
          />
        </div>
      </div>
    </template>
  </drawer>
</template>

<script>
import Drawer from "@/components/common/Drawer"
import Icon from "@/components/common/Icon"
import HuxSwitch from "@/components/common/Switch.vue"
import TextField from "@/components/common/TextField.vue"
import { mapGetters } from "vuex"

export default {
  name: "AlertConfigureDrawer",
  components: {
    Drawer,
    Icon,
    HuxSwitch,
    TextField,
  },

  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
    users: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  data() {
    return {
      localDrawer: this.value,
      showAlerts: true,
      switchLabelFullAlerts: [
        {
          condition: true,
          label: "YES",
        },
        {
          condition: false,
          label: "NO",
        },
      ],
      switchLabel: [
        {
          condition: true,
          label: "OPT IN",
        },
        {
          condition: false,
          label: "OPT OUT",
        },
      ],
    }
  },

  computed: {
    ...mapGetters({
      getCurrentUserEmail: "users/getEmailAddress",
    }),

    getNotificationPreferences() {
      return {
        data_sources: ["Informational", "Success", "Error"],
        engagements: ["Informational", "Success", "Error"],
        audiences: ["Informational", "Success", "Error"],
        delivery: ["Error"],
        identity_resolution: ["Informational"],
        models: ["Informational", "Success", "Error"],
        destinations: ["Informational", "Success", "Error"],
      }
    },
  },

  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
  },
  methods: {
    toggleAccess(val) {
      this.showAlerts = val
    },
  },
}
</script>
<style lang="scss" scoped>
.black-border {
  border-radius: 50%;
  border: 0.5px solid var(--v-black-base);
}
.full-alert {
  justify-content: space-between;
  align-items: center;
  height: 40px;
}
.w-53 {
  width: 53px;
}
</style>
