<template>
  <v-menu
    :close-on-content-click="false"
    :offset-x="isOffsetX"
    :offset-y="isOffsetY"
    :open-on-hover="isOpenOnHover"
    :transition="transition"
    :value="openMenu"
  >
    <template v-slot:activator="{ on }">
      <v-btn v-if="icon" :color="color" v-on="on">
        <v-icon>{{ icon }}</v-icon>
      </v-btn>
      <v-list-item
        v-else-if="isSubMenu"
        class="d-flex justify-space-between"
        v-on="on"
      >
        {{ name }}
        <div class="flex-grow-1"></div>
        <v-icon>mdi-chevron-right</v-icon>
      </v-list-item>
      <huxButton
        v-else
        v-bind:v-on="on"
        @click="openMenu = true"
        text
        v-bind:ButtonText="name"
        v-bind:isOutlined="true"
        width="200"
        icon=" mdi-chevron-down"
        iconPosition="right"
        class="ma-2"
      ></huxButton>
    </template>
    <v-list>
      <template v-for="(item, index) in menuItems">
        <v-divider v-if="item.isDivider" :key="index" />
        <hux-dropdown
          v-else-if="item.menu"
          :key="index"
          :name="item.name"
          :menu-items="item.menu"
          @hux-menu-click="emitClickEvent"
          :is-open-on-hover="false"
          :is-offset-x="true"
          :is-offset-y="false"
          :is-sub-menu="true"
          :selected="selected"
        />
        <v-list-item v-else :key="index" @click="emitClickEvent(item)">
          <v-list-item-title>
            {{ item.name }}
            <v-icon :color="color" v-if="selected == item.name"
              >mdi-check</v-icon
            >
          </v-list-item-title>
        </v-list-item>
      </template>
    </v-list>
  </v-menu>
</template>
<script>
import huxButton from "@/components/common/huxButton"
export default {
  name: "hux-dropdown",
  components: {
    huxButton,
  },
  props: {
    selected: String,
    name: String,
    icon: String,
    menuItems: Array,
    color: { type: String, default: "primary" },
    isOffsetX: { type: Boolean, default: false },
    isOffsetY: { type: Boolean, default: true },
    isOpenOnHover: { type: Boolean, default: false },
    isSubMenu: { type: Boolean, default: false },
    transition: { type: String, default: "scale-transition" },
  },
  methods: {
    emitClickEvent(item) {
      this.$emit("hux-menu-click", item)
      this.openMenu = false
    },
  },
  data: () => ({
    openMenu: false,
  }),
}
</script>
