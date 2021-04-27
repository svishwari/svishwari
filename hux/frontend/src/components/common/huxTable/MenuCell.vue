<template>
  <v-row class="menu-cell-wrapper">
    <v-col class="d-flex pr-0">
      {{ cellValue }}
      <v-spacer></v-spacer>
      <span class="action-icon font-weight-light float-right">
        <v-icon class="mr-2 action-favroite" color="primary" @click="addToFavorite($event)"> mdi-star </v-icon>
        <v-menu bottom offset-y>
          <template v-slot:activator="{ on, attrs }">
             <v-icon v-bind="attrs" v-on="on" class="mr-2 more-action" color="primary" @click="takeActions($event)"> mdi-dots-vertical </v-icon>
          </template>
          <v-list>
            <v-list-item v-for="(item, index) in items" :key="index">
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </span>
    </v-col>
  </v-row>
</template>
<script>
import Vue from "vue"
export default Vue.extend({
  name: "MenuCell",
  data() {
    return {
      cellValue: null,
      items: [
        { title: 'Export' },
        { title: 'Edit' },
        { title: 'Duplicate' },
        { title: 'Open' },
        { title: 'Pause delivery' },
        { title: 'Delete' },
      ],
    }
  },
  beforeMount() {
    this.cellValue = this.getValueToDisplay(this.params)
  },
  methods: {
    getValueToDisplay(params) {
      return params.valueFormatted ? params.valueFormatted : params.value
    },
    addToFavorite(evnt) {
      evnt.preventDefault();
    },
    takeActions(evnt) {
      evnt.preventDefault();
    }
  },
})
</script>
<style lang="scss" scoped>
.menu-cell-wrapper {
  &:hover {
    .action-icon {
      display: block;
      .action-favroite, .more-actions {
        cursor: pointer;
      }
    }
  }
  .action-icon {
    display: none;
  }
}
</style>
