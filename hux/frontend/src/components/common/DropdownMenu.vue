<template>
  <v-menu
    v-model="DropdownValue"
    offset-y
    close-on-click
    max-width="300"
    nudge-bottom="5"
  >
    <template #activator="{ on }">
      <div class="d-flex avatar-menu" v-on="on">
        <v-btn tile class="main-button" color="white">
          {{ labelText }}
          <v-icon right dark color="primary"> {{ iconType }} </v-icon>
        </v-btn>
      </div>
    </template>
    <v-card class="mx-auto">
      <v-list min-width="300" max-width="300" tile>
        <v-list-item-group>
          <v-list-item
            v-for="(item, index) in menuItem"
            :key="index"
            @click="clicked(item)"
          >
            <v-list-item-title>{{ item.value }}</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  name: "DropdownMenu",
  props: {
    labelText: {
      type: String,
      required: false,
      default: "Select...",
    },
    iconType: {
      type: String,
      required: false,
      default: "mdi-chevron-down",
    },
    menuItem: {
      type: Array,
    },
  },
  data: function () {
    return {
      DropdownValue: this.value,
    }
  },
  methods: {
    clicked: function (item) {
      this.$emit("input", item.value)
      this.$emit("updatelabelText", item.value)
    },
  },
}
</script>
