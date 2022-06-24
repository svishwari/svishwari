<template>
  <v-chip
    :color="getClass(color)"
    :text-color="darkText ? 'black' : 'white'"
    class="text-subtitle-2"
    :close="removable"
    close-icon="mdi-close"
    @click="pillClicked()"
  >
    <div class="vertical-align">
      <tooltip v-if="hover" nudge-right="30" nudge-top="25">
        <template #label-content>{{ label }}</template>
        <template #hover-content>
          <div>{{ hover }}</div>
        </template>
      </tooltip>
      <span v-else>{{ label }}</span>
      <v-menu v-if="dropdown" v-model="showMenu" nudge-left="32" nudge-bottom="24">
        <template #activator="{ on, attrs }">
          <icon
            :type="showMenu ? 'Dropdown - up' : 'Dropdown - down'"
            :size="14"
            :color="darkText ? 'black-base' : 'white-base'"
            outline
            :border-color="color"
            :bg-color="color"
            :on="on"
            :bind="attrs"
            class="ml-1"
          />
        </template>
        <slot name="dropdown-menu">
          <v-list><v-list-item>menu content</v-list-item></v-list>
        </slot>
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

<style lang="scss" scoped>
.dropdown-content {
  padding: 0px;
  position: relative;
  top: 30px;
  right: 30px;
}
.vertical-align {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
