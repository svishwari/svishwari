<template>
  <div class="text-center">
    <v-menu offset-y :min-width="130">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
        >
          Menu
        </v-btn>
      </template>
      <v-list>
        <div class="px-4 py-2">Header</div>
        <v-list-item
          v-for="(item, index) in items"
          :key="index"
          class="py-2 menu-items"
        >
          <icon 
            type="Icon Placeholder"
            :size="24"
            color="black-lighten1"
            :outline="false"
            borderColor="primary"
            bgColor="primary"
          />
          <span class="text-body-1">{{ item.title }}</span>
          <icon 
            type="Dropdown - right"
            :size="13"
            color="primary-base"
            :outline="false"
            borderColor="primary"
            bgColor="primary"
            class="temp"
          />
        </v-list-item>
        <div class="px-4 py-2">Footer</div>
      </v-list>
    </v-menu>
  </div>
</template>

<script>
import Icon from "../icons/Icon2.vue"
export default {
  name: "HuxMenu",
  components: { Icon },
  data() {
    return {
      items: [
        { title: 'Item' },
        { title: 'Item' },
        { title: 'Item' },
        { title: 'Item' },
      ],
    }
  },
}
</script>

<style lang="scss" scoped>
.menu-items {
  display: flex;
  justify-content: space-between;
}
::v-deep .v-list-item {
  height: 24px;
  max-height: 24px;
}
.temp {
  float: right;
}
</style>