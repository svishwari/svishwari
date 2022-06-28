<template>
  <div>
    <div class="pl-4 pt-2">{{ label }}</div>
    <v-card class="list-card">
      <v-list-item>
        <v-list-item-content>
          <div>
            <div class="list-title"><slot name="content">Content</slot></div>
            <hux-button
              class="list-button"
              :variant="disabled ? '' : 'secondary'"
              :is-disabled="disabled"
              :icon="selected ? 'check-icon' : ''"
              @click="handleClick()"
            >
              {{ getButtonText() }}
            </hux-button>
          </div>
        </v-list-item-content>
      </v-list-item>
    </v-card>
  </div>
</template>

<script>
import HuxButton from "../huxButton/huxButton2.vue"

export default {
  name: "MultiSelectListItem",
  components: { HuxButton },
  props: {
    label: {
      type: String,
      required: false,
      default: "Label",
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    selected: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  methods: {
    getButtonText() {
      return this.disabled ? "Inactive" : this.selected ? "Selected" : "Request"
    },
    handleClick() {
      this.selected = !this.selected
    },
  },
}
</script>

<style lang="scss" scoped>
.list-card {
  width: 552px;
  justify-content: center;
  margin-left: 8px;
}
.list-title {
  float: left;
  height: 40px;
  padding-top: 12px;
}
.list-button {
  float: right;
}
</style>
