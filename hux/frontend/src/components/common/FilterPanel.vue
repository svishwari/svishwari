<template>
  <v-expansion-panel class="hux-filter-panel">
    <v-expansion-panel-header
      class="header"
      :disabled="disabled"
      :hide-actions="hideActions"
      @click="headerclick = !headerclick"
    >
      <h4
        :class="
          count == 0 && !headerclick
            ? 'text-body-1 black--text'
            : 'text-body-1 primary--text text--lighten-6'
        "
      >
        <slot name="title">{{ title }}</slot>
        <span v-if="count" class="ml-1">({{ count }})</span>
      </h4>
      <template #actions>
        <v-icon :color="count == 0 && !headerclick ? 'black' : 'blue'">
          $expand
        </v-icon>
      </template>
    </v-expansion-panel-header>

    <v-expansion-panel-content class="content">
      <slot name="default">
        <!-- filter options and selections (radio, checkbox, dropdown, etc) -->
      </slot>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import { defineComponent } from "@vue/composition-api"
export default defineComponent({
  props: {
    title: {
      type: String,
      required: true,
    },
    count: {
      type: Number,
      required: false,
      default: 0,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    hideActions: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      headerclick: false,
    }
  },
  methods: {
    // headerclick(e) {
    //   this.headerVli
    //   console.log("e.target.classList", e.target.classList)
    //   // if (e.target.classList.contains("v-expansion-panel-header--active")) {
    //   //   console.log("event closing",e)
    //   // }
    //   // else {
    //   //    console.log("event opening",e)
    //   // }
    //   // let target = e.target,
    //   //   header = ".v-expansion-panel__header"
    //   // if (target.is(header) || target.parents(header).is(header)) {
    //   //   console.log("Hello World")
    //   // }
    // },
  },
})
</script>

<style lang="scss" scoped>
$padding: 24px;
$headerHeight: 40px;
.hux-filter-panel {
  .header {
    height: $headerHeight;
    padding: 0 $padding;
    border-top: 1px solid var(--v-black-lighten2);
  }
  &:last-child {
    .header {
      border-bottom: 1px solid var(--v-black-lighten2);
    }
  }
  .content {
    ::v-deep .v-expansion-panel-content__wrap {
      padding: $padding;
    }
  }
  .openClass {
  }
}
</style>
