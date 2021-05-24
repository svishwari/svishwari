<template>
  <v-row class="menu-cell-wrapper">
    <v-col class="d-flex pr-0">
      <router-link
        :to="{
          name: 'AudienceInsight',
          params: { id: audienceId },
        }"
        class="text-decoration-none"
        append
      >
        <span class="primary--text"> {{ cellValue }} </span>
      </router-link>
      <v-spacer></v-spacer>
      <span class="action-icon font-weight-light float-right">
        <v-menu class="menu-wrapper" bottom offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              v-bind="attrs"
              v-on="on"
              class="mr-2 more-action"
              color="primary"
              @click="takeActions($event)"
            >
              mdi-dots-vertical
            </v-icon>
          </template>
          <v-list class="list-wrapper">
            <v-list-item-group>
              <v-list-item v-for="(item, index) in items" :key="index" disabled>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list-item-group>
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
      audienceId: null,
      cellValue: null,
      items: [
        { title: "Favorite" },
        { title: "Export" },
        { title: "Edit" },
        { title: "Duplicate" },
        { title: "Create a lookalike" },
        { title: "Delete" },
      ],
      favoriteIconColor: "default",
    }
  },
  beforeMount() {
    this.cellValue = this.getValueToDisplay(this.params)
  },
  methods: {
    getValueToDisplay(params) {
      return params.valueFormatted ? params.valueFormatted : params.value
    },
    addToFavorite() {
      if (this.favoriteIconColor == "default") {
        this.favoriteIconColor = "primary"
      } else {
        this.favoriteIconColor = "default"
      }
    },
    takeActions(evnt) {
      evnt.preventDefault()
    },
  },
  async mounted() {
    this.audienceId = this.params.data.audienceId
  },
})
</script>
<style lang="scss" scoped>
::v-deep.v-menu__content {
  .v-list-item {
    &.theme--light {
      min-height: 32px !important;
    }
  }
}
</style>
