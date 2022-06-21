<template>
  <div>
    <plain-card title="Filter Card">
      <template #call-to-action>
        <span>
          <icon-button
            icon="filter"
            size="22"
            icon-color="primary"
            class="format-button"
            @click="handleClick()"
          />
        </span>
      </template>
      <template #filters>
        <v-container v-if="toggleFilter" class="filter-options">
          <v-row>
            <hux-button
              text-only
              variant="primary"
              @click="addFilter('Filter 1')"
              >Filter1</hux-button
            >
            <hux-button
              text-only
              variant="primary"
              @click="addFilter('Filter 2')"
              >Filter2</hux-button
            >
            <v-spacer />
            <hux-button text-only variant="primary" @click="clearFilters()"
              >Clear all</hux-button
            >
          </v-row>
          <v-row v-if="filtersAdded.length > 0">
            <pill
              v-for="(item, index) in filtersAdded"
              :key="index"
              :removable="true"
              :label="item"
              :dark-text="true"
              @close="removeFilter(item)"
            />
          </v-row>
        </v-container>
      </template>
      <template #body>
        <div>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua.
        </div>
      </template>
    </plain-card>
  </div>
</template>

<script>
import PlainCard from "../cards/PlainCard.vue"
import IconButton from "../iconButton/plainButton.vue"
import HuxButton from "../huxButton/NewButton.vue"
import Pill from "../pills/Pill.vue"

export default {
  name: "CardFilter",
  components: { PlainCard, IconButton, HuxButton, Pill },
  data() {
    return {
      toggleFilter: false,
      filtersAdded: [],
    }
  },
  methods: {
    handleClick() {
      this.toggleFilter = true // change this later
      console.log(this.toggleFilter) // clicking 2x for some reason (problem in icon button)
    },
    addFilter(label) {
      this.filtersAdded.push(label)
      console.log(this.filtersAdded)
    },
    removeFilter(label) {
      const temp = this.filtersAdded.indexOf(label)
      if (temp > -1) {
        this.filtersAdded.splice(temp, 1)
      }
    },
    clearFilters() {
      this.filtersAdded = []
    },
  },
}
</script>

<style lang="scss" scoped>
.format-button {
  margin-top: -12px;
}
.filter-options {
  border-top: 1px solid var(--v-black-lighten3);
  border-bottom: 1px solid var(--v-black-lighten3);
}
</style>
