<template>
  <div class="hux-select-wrapper">
    <label class="hux-select-label mt-6 mr-3"> Segments by </label>
    <v-select
      v-model="getDefaultSelected"
      class="hux-select"
      item-text="name"
      item-value="last"
      :items="dataItems"
      @change="onSelect"
    >
    </v-select>
  </div>
</template>

<script>
export default {
  name: "HuxSelect",
  props: {
    dataList: {
      type: Array,
      required: true,
      default: () => [],
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
  methods: {
    onSelect(selectedValue) {
      this.$emit("onselect", selectedValue)
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
}
</script>
<style lang="scss" scoped>
.hux-select-wrapper {
  .hux-select-label {
    float: left;
  }
  .hux-select {
    width: 195px;
    ::v-deep .v-input__control {
      .v-input__slot {
        .v-select__slot {
          .v-select__selections {
            .v-select__selection {
              margin-bottom: 0 !important;
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
        border-width: unset !important;
        border-style: none !important;
        border-color: var(--v-primary-base) !important;
        border-bottom-style: dotted !important;
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
