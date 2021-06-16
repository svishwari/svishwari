<template>
  <div class="hux-dropdown">
    <v-menu
      :close-on-content-click="false"
      :offset-x="isOffsetX"
      :offset-y="isOffsetY"
      :open-on-hover="isOpenOnHover"
      :transition="transition"
      max-width="300"
      close-on-click
      v-model="openMenu"
      class="hux-dropdown"
    >
      <template #activator="{ on }">
        <!-- <v-btn v-if="icon" :color="color" v-on="on">
        <v-icon>{{ icon }}</v-icon>
      </v-btn> -->
        <v-list-item
          v-if="isSubMenu"
          class="d-flex justify-space-between"
          v-on="on"
        >
          {{ optionSelected["name"] || label }}
          <div class="flex-grow-1"></div>
          <v-icon>mdi-chevron-right</v-icon>
        </v-list-item>
        <huxButton
          v-else
          :v-on="on"
          @click="openMenu = true"
          text
          :isOutlined="true"
          width="200"
          icon=" mdi-chevron-down"
          iconPosition="right"
          tile
          class="ma-2 main-button"
        >
          {{ optionSelected["name"] || label }}
        </huxButton>
      </template>
      <v-list>
        <template v-for="(item, index) in items">
          <v-divider v-if="item.isDivider" :key="index" />
          <span v-if="item.isGroup" :key="item.name" class="group_name">{{
            item.name
          }}</span>
          <hux-dropdown
            v-else-if="item.menu"
            :key="index"
            :label="item.name"
            :items="item.menu"
            @on-select="onSelect"
            :is-open-on-hover="false"
            :is-offset-x="true"
            :is-offset-y="false"
            :is-sub-menu="true"
            :selected="selected"
          />
          <v-list-item v-else :key="index" @click="onSelect(item)">
            <v-list-item-title>
              <v-icon v-if="item.icon">{{ item.icon }}</v-icon>
              {{ item.name }}
              <v-icon :color="color" v-if="optionSelected.name == item.name"
                >mdi-check</v-icon
              >
            </v-list-item-title>
          </v-list-item>
        </template>
      </v-list>
    </v-menu>
  </div>
</template>
<script>
import huxButton from "@/components/common/huxButton"
export default {
  name: "hux-dropdown",
  components: {
    huxButton,
  },
  computed: {
    optionSelected() {
      const filteredOption = this.items.filter(
        (item) => item.key === this.selected
      )
      return filteredOption.length > 0 ? filteredOption[0] : this.label
    },
  },
  props: {
    selected: {
      type: [Object, String],
    },
    label: {
      type: String,
      required: true,
      default: "Select Option",
    },
    icon: String,
    items: Array,
    color: { type: String, default: "primary" },
    isOffsetX: { type: Boolean, default: false },
    isOffsetY: { type: Boolean, default: true },
    isOpenOnHover: { type: Boolean, default: false },
    isSubMenu: { type: Boolean, default: false },
    transition: { type: String, default: "scale-transition" },
  },
  methods: {
    onSelect(item) {
      this.$emit("on-select", item)
      this.openMenu = false
    },
  },
  data: function () {
    return {
      openMenu: this.value,
    }
  },
}
</script>

<style lang="scss" scoped>
.hux-dropdown {
  .main-button {
    height: 36px;
    min-width: 64px;
    padding: 0 16px;
  }
}
</style>
