<template>
  <div class="hux-select-wrapper">
    <label class="hux-select-label mt-4 mr-3 text-body-1 black--text">
      Segments by
    </label>
    <v-select
      v-model="getDefaultSelected"
      class="hux-select"
      item-text="name"
      item-value="last"
      :items="dataItems"
      :style="`max-width: ${width}px`"
      :menu-props="{
        offsetY: true,
        nudgeBottom: '5px',
      }"
      append-icon="mdi-chevron-down"
      @change="onSelect"
    >
    </v-select>
  </div>
</template>

<script>
export default {
  name: "LinkDropdown",
  props: {
    dataList: {
      type: Array,
      required: true,
      default: () => [],
    },
    width: {
      type: [String, Number],
      required: false,
      default: 141,
    },
  },
  data: () => ({
    dataItems: [],
  }),
  computed: {
    getDefaultSelected: {
      get() {
        return this.dataItems && this.dataItems[0]
      },
      set(newName) {
        return newName
      },
    },
  },
  mounted() {
    if (this.dataList) {
      this.dataList.forEach((item) => {
        this.dataItems.push({
          name: item,
          last: item,
        })
      })
    }
  },
  methods: {
    onSelect(selectedValue) {
      this.$emit("onselect", selectedValue)
    },
  },
}
</script>
<style lang="scss" scoped>
.hux-select-wrapper {
  .hux-select-label {
    float: left;
  }
  .hux-select {
    ::v-deep .v-input__control {
      .v-input__slot {
        .v-select__slot {
          .v-select__selections {
            background-image: linear-gradient(
              to right,
              var(--v-primary-base) 40%,
              rgba(255, 255, 255, 0) 20%
            );
            background-position: bottom;
            background-size: 4px 1px;
            background-repeat: repeat-x;
            .v-select__selection {
              color: var(--v-primary-base) !important;
            }
          }
          .v-input__append-inner {
            .v-input__icon {
              .v-icon {
                color: var(--v-primary-base) !important;
              }
            }
          }
        }
      }
      .v-input__slot:before {
        border-style: none !important;
      }
    }
    &.v-input--is-focused {
      &.primary--text {
        color: transparent !important;
      }
    }
  }
}

.v-menu__content {
  .v-select-list {
    ::v-deep .v-list-item {
      min-height: 32px !important;
    }
  }
}
</style>
