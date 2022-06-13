<template>
  <v-chip
    :color="getClass(color)"
    :text-color="darkText ? 'black' : 'white'"
    class="text-subtitle-2"
    :close="removable"
    close-icon="mdi-close"
    @click="pillClicked()"
    @click:close="pillClicked()"
  >
    <tooltip v-if="hover">
      <template #label-content>{{ label }}</template>
      <template #hover-content>
        <span class="text-body-4">{{ hover }}</span>
      </template>
    </tooltip>
    <div v-else>
      {{ label }}
      <v-menu v-if="dropdown">
        <template #activator="{ on }">
          <icon
            right
            :type="showMenu ? 'chevron-down' : 'chevron-down'"
            :color="darkText ? 'black' : 'white'"
            size="12"
            class="pt-1"
            :on="on"
          />
        </template>
        <div>test</div>
        <div>test2</div>
      </v-menu>
    </div>
  </v-chip>
</template>

<script>
import tooltip from "@/components/common/Tooltip"
import icon from "../icons/Icon2.vue"

export default {
  name: "Pill",
  components: { tooltip, icon },
  props: {
    label: {
      type: String,
      required: true,
    },
    removable: {
      type: Boolean,
      required: false,
      default: false,
    },
    hover: {
      type: String,
      required: false,
    },
    dropdown: {
      type: Boolean,
      required: false,
      default: false,
    },
    color: {
      type: String,
      required: false,
      default: "primary",
    },
    darkText: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      showMenu: false,
    }
  },
  methods: {
    getClass(color) {
      return `var(--v-${color})`
    },
    pillClicked() {
      if (this.dropdown) {
        this.showMenu = !this.showMenu
      } else if (this.removable) {
        this.$emit("close")
      }
    },
  },
}
</script>
