<template>
  <hux-filters-drawer
    :is-toggled="localDrawer"
    header-name="Add segment"
    transition="scale-transition"
    :count="1"
    content-height="330px"
    submit-button-width="79"
    submit-button="Add"
    :style="{ transition: '0.5s', height: viewHeight }"
    :custom-validation="true"
    :enable-apply="setEnableApply"
    @clear="clear"
    @apply="apply"
    @close="close"
  >
    <div class="filter-body">
      <hux-filter-panels>
        <div class="checkboxFavorite">
          <text-field
            v-model="segmentName"
            class="mt-4 ml-5 mb-n3 input-box-Field"
            label-text="Segment name"
            placeholder="Segment"
            required
          />
        </div>
        <span v-for="(list, index) in segmentData" :key="index">
          <v-checkbox
            v-if="list.is_boolean"
            v-model="segmentDataObj[list.type + '#' + list.description]"
            color="primary lighten-6"
            class="text--base-1 px-5 withoutExpansion checkboxFavorite"
            :label="list.description"
            @change="checkboxChange(list.type + '#' + list.description)"
          ></v-checkbox>
        </span>
        <hux-filter-panels>
          <hux-filter-panel
            v-for="(data, ind) in filterData"
            :key="ind"
            :title="data.description"
          >
            <v-checkbox
              v-for="(dataVal, indx) in data.values"
              :key="indx"
              v-model="segmentDataObj[data.type + '#' + data.description]"
              multiple
              color="primary lighten-6"
              class="text--base-1"
              :label="dataVal"
              :value="dataVal"
              @change="checkboxChange(data.type + '#' + data.description)"
            ></v-checkbox>
          </hux-filter-panel>
        </hux-filter-panels>
      </hux-filter-panels>
    </div>
  </hux-filters-drawer>
</template>

<script>
import HuxFiltersDrawer from "@/components/common/FiltersDrawer"
import HuxFilterPanels from "@/components/common/FilterPanels"
import HuxFilterPanel from "@/components/common/FilterPanel"
import TextField from "@/components/common/TextField"

export default {
  name: "AddSegmentDrawer",
  components: {
    HuxFiltersDrawer,
    HuxFilterPanels,
    HuxFilterPanel,
    TextField,
  },
  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
    viewHeight: {
      type: String,
      required: false,
      default: "auto",
    },
    segmentData: {
      type: Array,
      required: false,
      default: () => [],
    },
    segmentLength: {
      type: Number,
      required: false,
      default: 1,
    },
  },
  data() {
    return {
      localDrawer: this.value,
      selectedAttributes: [],
      enableApply: false,
      segmentName: "Segment",
      // TODO: once Delete segment API is integrated
      // segmentName: "Segment" + " " + (this.segmentLength + 1),
      segmentDataObj: {},
    }
  },

  computed: {
    filterData() {
      return this.segmentData.filter((element) => !element.is_boolean)
    },
    segmentFilters() {
      const payload = []
      Object.entries(this.segmentDataObj).forEach(([key, value]) => {
        let [keyValue, descriptionValue] = key.split("#")
        payload.push({
          type: keyValue,
          description: descriptionValue,
          values: Array.isArray(value) ? value : [value.toString()],
        })
      })

      return payload
    },
    setEnableApply() {
      return Object.keys(this.segmentFilters).length > 0 ? true : false
    },
  },
  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
  },
  methods: {
    clear() {
      this.segmentName = "Segment"
      this.segmentDataObj = {}
    },
    checkboxChange(keyType) {
      if (
        !Array.isArray(this.segmentDataObj[keyType]) &&
        !this.segmentDataObj[keyType]
      ) {
        delete this.segmentDataObj[keyType]
      } else {
        if (this.segmentDataObj[keyType].length == 0) {
          delete this.segmentDataObj[keyType]
        }
      }
    },
    apply() {
      this.$emit("onSectionAction", {
        segment_name: this.segmentName,
        segment_filters: this.segmentFilters,
      })
    },
    close() {
      this.segmentName = "Segment"
      this.segmentDataObj = {}
      this.localDrawer = false
    },
  },
}
</script>
<style lang="scss" scoped>
::v-deep.v-input--selection-controls {
  margin-top: 0px !important;
  padding-top: 0px !important;
}
::v-deep.v-input--selection-controls.v-input {
  flex: 1 1 auto !important;
}
::v-deep.input__slot {
  margin: 0px !important;
}
::v-deep .v-input--selection-controls .v-input__slot {
  margin-bottom: 0px !important;
}
::v-deep.theme--light .v-messages {
  min-height: 6px !important;
  color: var(--v-black-base);
}
.clear-btn {
  padding-left: 7.9rem !important;
  padding-top: 10px;
  padding-right: 0px !important;
}
.withoutExpansion {
  height: 40px;
  align-items: center;
  margin-top: 6px !important;
}
::v-deep.theme--light .v-label {
  font-size: 16px;
  font-weight: 400;
  line-height: 22px;
  letter-spacing: 0;
  color: var(--v-black-base);
}
.checkboxFavorite {
  border-bottom: 1px solid var(--v-black-lighten2);
}
.filter-body {
  ::v-deep .v-expansion-panel-content__wrap {
    padding: 14px 24px 14px 24px !important;
  }
}
::v-deep .submit-button {
  margin-right: 110px !important;
}
::v-deep .v-expansion-panels {
  justify-content: initial !important;
}
.input-box-Field {
  width: 280px !important;
}
::v-deep .v-input--selection-controls .v-input__slot {
  margin-bottom: 0px !important;
  align-items: start;
}
::v-deep .v-input--selection-controls__input {
  margin-top: 0px !important;
}
::v-deep .hux-filters-drawer .content {
  overflow-x: hidden;
}
::v-deep .hux-filter-panels {
  span {
    .withoutExpansion {
      .v-input__control {
        .v-input__slot {
          align-items: center;
        }
      }
    }
  }
}
</style>
