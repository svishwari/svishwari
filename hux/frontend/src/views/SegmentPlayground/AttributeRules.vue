<template>
  <v-col cols="12" class="attribute-rule pt-0 pl-0 pr-0">
    <v-col cols="12" class="pa-0">
      <strong
        v-if="enableTitle"
        :class="{
          'text-h5 black--text text--darken-4 mb-2 d-block': true,
          '': applyCaptionStyle,
        }"
      >
        Select attribute(s) -
        <i class="text-h6 black--text text--darken-1">optional</i>
      </strong>
      <v-card
        v-if="rules.length == 0"
        tile
        elevation="0"
        class="blank-section pa-6"
      >
        <div
          class="
            text-body-1
            primary--text
            new-attribute
            d-flex
            align-center
            cursor-pointer
          "
          data-e2e="add-new-attr"
          @click="addNewSection()"
        >
          <icon type="plus" color="primary" :size="11" class="mr-2" />
          New attribute
        </div>
      </v-card>
    </v-col>
    <v-col v-if="rules.length > 0" col="12" class="pt-0 pr-0 pa-0">
      <div v-for="(rule, index) in rules" :key="rule.id">
        <div
          class="
            d-flex
            align-center
            col-12
            pa-0
            black--text
            text--darken-4 text-body-2
          "
        >
          <span class="mr-2">Match</span>
          <hux-switch
            v-model="rule.operand"
            @input="triggerSizingForRule(rule)"
          />
          of the following
        </div>

        <v-col
          v-for="(condition, ixcondition) in rule.conditions"
          :key="condition.id"
          class="rule-section pa-0 mb-2 d-flex"
        >
          <div class="pa-0 pr-2 flex-fill">
            <div class="condition-card">
              <div class="condition-container pl-2 d-fles pr-6">
                <div class="condition-items pr-5">
                  <hux-dropdown
                    :selected="condition.attribute"
                    :items="attributeOptions()"
                    label="Select attribute"
                    data-e2e="select-attr-btn"
                    @on-select="onSelect('attribute', condition, $event)"
                  />
                  <hux-dropdown
                    v-if="isTextORSelect(condition)"
                    label="Select operator"
                    :items="operatorOptions(condition)"
                    :selected="condition.operator"
                    data-e2e="select-operator-btn"
                    @on-select="onSelect('operator', condition, $event)"
                  />
                  <text-field
                    v-if="
                      condition.operator && condition.attribute.type === 'text'
                    "
                    v-model="condition.text"
                    class="item-text-field"
                    :placeholder="getPlaceHolderText(condition)"
                    required
                    @blur="triggerSizing(condition)"
                  />

                  <hux-autocomplete
                    v-if="
                      condition.operator && condition.attribute.type === 'list'
                    "
                    v-model="condition.text"
                    :options="listOptions(condition)"
                    data-e2e="auto-complete-btn"
                    @change="triggerSizing(condition)"
                  />
                  <div
                    v-if="condition.attribute && !isTextORSelect(condition)"
                    ref="hux-density-slider"
                    class="range-attribute-container"
                    :class="condition.attribute.values ? 'pt-6' : ''"
                  >
                    <hux-density-chart
                      v-if="condition.attribute.values"
                      :id="condition.id"
                      :data="condition.attribute.values"
                      :chart-dimensions="chartDimensions"
                      :min="condition.attribute.min"
                      :max="condition.attribute.max"
                      :range="condition.range"
                      class="ml-2 mr-0"
                    />
                    <hux-slider
                      v-model="condition.range"
                      :read-only="false"
                      :min="condition.attribute.min"
                      :max="condition.attribute.max"
                      :step="condition.attribute.steps"
                      :custom-label="
                        (val) => sliderLabel(condition.attribute, val)
                      "
                      :class="
                        condition.attribute.values ? 'density-slider' : ''
                      "
                      is-range-slider
                      @onFinalValue="triggerSizing(condition)"
                    />
                  </div>
                </div>
                <div
                  class="condition-actions pa-0 cursor-pointer"
                  data-e2e="remove-attr"
                  @click="removeCondition(rule, ixcondition)"
                >
                  <icon type="trash" :size="18" color="black" />
                </div>
              </div>
            </div>
          </div>
          <div class="pr-0 py-0 flex-right">
            <div class="condition-summary">
              <span class="title text-h5">Rule Size</span>
              <span v-if="condition.awaitingSize" class="pt-2">
                <v-progress-linear indeterminate buffer-value="0" stream />
              </span>
              <span v-else class="value text-h6 pt-1 text-subtitle-1">
                {{ condition.size | Numeric(false, false, true) }}
              </span>
            </div>
          </div>
        </v-col>
        <div class="add-wrap">
          <div class="pa-0 pt-2 flex-fill">
            <div class="add-section pa-5 text-body-1 primary--text">
              <span class="cursor-pointer" @click="addNewCondition(rule.id)">
                <icon type="plus" color="primary" :size="11" class="mr-2" />
                New attribute
              </span>
            </div>
          </div>
          <div class="pr-0 pt-2 pl-2 flex-right">
            <div class="condition-summary">
              <span class="title text-h5">Size</span>
              <span v-if="loadingOverAllSize" class="pt-2">
                <v-progress-linear indeterminate buffer-value="0" stream />
              </span>
              <span v-else class="value text-h6 pt-1 text-subtitle-1">
                {{ overAllSize | Numeric(false, false, true) }}
              </span>
            </div>
          </div>
        </div>
        <div v-if="index != lastIndex" class="col-12 seperator mt-5 mb-1 px-0">
          <hr class="black lighten-2" />
          <v-chip
            small
            class="mx-2 my-1 text-body-2"
            text-color="primary"
            color="primary lighten-3"
            :ripple="false"
          >
            OR
          </v-chip>
        </div>
      </div>
      <div class="col-12 seperator mt-5 mb-1">
        <hr class="black lighten-2" />
        <v-chip
          small
          class="mx-2 my-1 text-body-1 cursor-pointer"
          text-color="primary"
          color="black lighten-2"
          :ripple="false"
          @click.native="addNewSection()"
        >
          <tooltip>
            <template #label-content> + </template>
            <template #hover-content>
              <span class="text-body-2"> Add a new section </span>
            </template>
          </tooltip>
        </v-chip>
      </div>
    </v-col>
  </v-col>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import HuxDropdown from "../../components/common/HuxDropdown.vue"
import HuxSlider from "../../components/common/HuxSlider.vue"
import HuxDensityChart from "@/components/common/Charts/DensityChart/HuxDensityChart"
import HuxSwitch from "../../components/common/Switch.vue"
import TextField from "../../components/common/TextField.vue"
import Icon from "@/components/common/Icon"
import HuxAutocomplete from "../../components/common/HuxAutocomplete.vue"
import Tooltip from "../../components/common/Tooltip.vue"

const NEW_RULE_SECTION = {
  id: "",
  operand: true,
  conditions: [],
}
const NEW_CONDITION = {
  id: "",
  attribute: "",
  operator: "",
  text: "",
  range: [],
  awaitingSize: false,
  outputSummary: "0",
  size: "-",
}

export default {
  name: "AttributeRules",
  components: {
    TextField,
    HuxSwitch,
    HuxDropdown,
    HuxSlider,
    HuxDensityChart,
    Icon,
    HuxAutocomplete,
    Tooltip,
  },
  props: {
    rules: {
      type: Array,
      required: true,
      default: () => [],
    },
    applyCaptionStyle: {
      type: Boolean,
      required: false,
      default: false,
    },
    enableTitle: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      loadingOverAllSize: false,
      overAllSize: 0,
      chartDimensions: {
        width: 0,
        height: 0,
      },
      notHistogramKeys: ["gender", "email", "Country", "State", "City", "Zip"],
    }
  },
  computed: {
    ...mapGetters({
      ruleAttributes: "audiences/audiencesRules",
    }),

    lastIndex() {
      return this.rules.length - 1
    },
  },
  async mounted() {
    this.sizeHandler()
    this.chartDimensions.height = 26
    await this.getAudiencesRules()
    this.updateSizes()
  },

  created() {
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.sizeHandler)
  },

  updated() {
    this.sizeHandler()
  },

  methods: {
    ...mapActions({
      getRealtimeSize: "audiences/fetchFilterSize",
      getAudiencesRules: "audiences/fetchConstants",
      attributesData: "audiences/getDensityChartData",
    }),
    sliderLabel(attribute, value) {
      if (attribute.key === "ltv_predicted") {
        return `$${value}`
      }
      return value
    },
    sizeHandler() {
      if (this.$refs["hux-density-slider"]) {
        if (this.$refs["hux-density-slider"][0]) {
          this.chartDimensions.width =
            this.$refs["hux-density-slider"][0].clientWidth
        }
      }
    },

    isTextORSelect(condition) {
      return condition.attribute
        ? condition.attribute.type === "text" ||
            condition.attribute.type === "list"
        : false
    },
    /**
     * This attributeOptions is transforming the API attributeRules into the Options Array
     *
     * Segregating the Groups which are the parent key.
     * Appending the sub options next to the group label.
     *
     * Also, having an Top Priority Order to Models.
     *
     * @returns {Array} options array
     */
    attributeOptions() {
      if (this.ruleAttributes.rule_attributes) {
        const options = []
        const masterAttributes = this.ruleAttributes.rule_attributes
        Object.keys(masterAttributes).forEach((groupKey) => {
          const _group_items = []
          const order = groupKey.includes("model") ? 0 : 1
          const group = {
            name: groupKey.replace("_", " "),
            isGroup: true,
          }
          _group_items.push(group)
          _group_items.push(
            ...Object.keys(masterAttributes[groupKey]).map((key) => {
              const _subOption = masterAttributes[groupKey][key]
              const hasSubOptins = Object.keys(_subOption).filter(
                (item) => !!_subOption[item]["name"]
              )
              if (hasSubOptins.length > 0) {
                _subOption["menu"] = hasSubOptins.map((key) => {
                  const subOption = _subOption[key]
                  subOption["key"] = subOption.name
                  return subOption
                })
              }
              if (groupKey.includes("model")) _subOption["modelIcon"] = true
              _subOption.key = key
              return _subOption
            })
          )
          _group_items.forEach((item) => (item["order"] = order))
          options.push(..._group_items)
        })
        return options.sort(function (a, b) {
          return a.order - b.order
        })
      } else return []
    },
    listOptions(condition) {
      return condition.attribute.options
    },
    operatorOptions(condition) {
      // Filter out only two options (equals and does_not_equals) for attribute type 'gender'
      if (
        condition.attribute.type === "list" ||
        condition.attribute.key === "gender"
      ) {
        return Object.keys(this.ruleAttributes.text_operators)
          .map((key) => {
            if (key.includes("equal")) {
              return {
                key: key,
                name: this.ruleAttributes.text_operators[key],
              }
            }
          })
          .filter(Boolean)
      } else {
        return Object.keys(this.ruleAttributes.text_operators).map((key) => ({
          key: key,
          name: this.ruleAttributes.text_operators[key],
        }))
      }
    },
    async triggerSizing(condition, triggerOverallSize = true) {
      condition.awaitingSize = true
      if (triggerOverallSize) {
        this.getOverallSize()
      }
      let value = null
      let type = null
      if (condition.attribute.type === "range") {
        value = [...condition.range]
        type = "range"
      } else {
        value = condition.text
        type = condition.operator.key
      }
      let filterJSON = {
        filters: [
          {
            section_aggregator: "ALL",
            section_filters: [
              {
                field: condition.attribute.key,
                type: type,
                value: value,
              },
            ],
          },
        ],
      }
      try {
        let data = await this.getRealtimeSize({
          filter: filterJSON,
          overall: false,
        })
        condition.size = data.total_customers
        condition.awaitingSize = false
      } catch (error) {
        condition.size = 0
        condition.awaitingSize = false
      }
    },

    async triggerSizingForRule(rule) {
      for (let i = 0; i < rule.conditions.length; i++) {
        let triggerOverallSize = rule.conditions.length - 1 === i ? true : false
        this.triggerSizing(rule.conditions[i], triggerOverallSize)
      }
    },

    updateSizes() {
      this.rules.forEach((rule) => {
        this.triggerSizingForRule(rule)
      })
    },

    async getOverallSize() {
      this.$emit("loadingOverAllSize", true)
      this.loadingOverAllSize = true
      let filterJSON = {
        filters: [],
      }
      for (let i = 0; i < this.rules.length; i++) {
        let aggregatorOperand = this.rules[i].operand ? "ALL" : "ANY"
        let attributeRulesArray = []
        for (let j = 0; j < this.rules[i].conditions.length; j++) {
          let value = null
          let type = ""
          if (this.rules[i].conditions[j].attribute.type === "range") {
            value = [...this.rules[i].conditions[j].range]
            type = "range"
          } else {
            value = this.rules[i].conditions[j].text
            type = this.rules[i].conditions[j].operator.key
          }
          attributeRulesArray.push({
            field: this.rules[i].conditions[j].attribute.key,
            type: type,
            value: value,
          })
        }
        let sectionObject = {
          section_aggregator: aggregatorOperand,
          section_filters: attributeRulesArray,
        }
        filterJSON.filters.push(sectionObject)
      }
      try {
        let data = await this.getRealtimeSize({
          filter: filterJSON,
          overall: true,
        })
        this.$emit("updateOverview", data)
        this.overAllSize = data.total_customers
        this.$emit("loadingOverAllSize", false)
        this.loadingOverAllSize = false
      } catch (error) {
        this.overAllSize = 0
        this.$emit("loadingOverAllSize", false)
        this.loadingOverAllSize = false
      }
    },

    async onSelect(type, condition, item) {
      let dataItem = item
      condition[type] = item
      if (type === "attribute") {
        if (!this.notHistogramKeys.includes(item.key)) {
          let data = await this.attributesData({
            field: item.modelIcon ? "model" : item.key,
            model: item.modelIcon ? item.key : null,
          })
          if (data) {
            data.key = item.key
            dataItem = data
          }
        }
        condition[type] = dataItem
        condition.operator = ""
        condition.text = ""
        condition.type = dataItem.type
        condition.options = dataItem.options
        condition.range = [dataItem.min, dataItem.max]
        condition.awaitingSize = false
        condition.outputSummary = 0
      } else if (type === "operator") {
        condition.text = ""
        condition.range = []
        condition.awaitingSize = false
        condition.outputSummary = 0
      }
    },
    addNewCondition(id) {
      const newCondition = JSON.parse(JSON.stringify(NEW_CONDITION))
      newCondition.id = Math.floor(Math.random() * 1024).toString(16)
      const sectionFound = this.rules.filter((rule) => rule.id === id)
      if (sectionFound.length > 0) sectionFound[0].conditions.push(newCondition)
    },
    removeCondition(parent, child) {
      if (parent.conditions.length === 1) {
        const indx = this.rules.findIndex((rul) => rul.id === parent.id)
        this.rules.splice(indx, 1)
      } else {
        parent.conditions.splice(child, 1)
      }
      this.getOverallSize()
    },
    getPlaceHolderText(condition) {
      switch (condition.attribute.key) {
        case "email":
          return "example@email.com"
        case "gender":
          return "Type male, female, or other"
        case "City":
        case "Country":
        case "State":
          return condition.attribute.key + " name"
        default:
          return condition.attribute.key
      }
    },
    addNewSection() {
      const newSection = JSON.parse(JSON.stringify(NEW_RULE_SECTION))
      newSection.id = Math.floor(Math.random() * 1024).toString(16)
      this.rules.push(newSection)
      this.addNewCondition(newSection.id)
    },
  },
}
</script>

<style lang="scss" scoped>
.attribute-rule {
  ::v-deep .blank-section {
    background: var(--v-primary-lighten1);
    border: 1px solid var(--v-black-lighten2);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 5px !important;
  }
  .flex-fill {
    flex: 1 0;
  }
  .flex-right {
    flex: 0 1;
  }
  ::v-deep .seperator {
    position: relative;
    hr {
      border-style: solid;
    }
    .v-chip {
      position: absolute;
      top: 0;
      left: 50%;
    }
  }
  ::v-deep .rule-section {
    display: flex;
    .condition-card {
      background: var(--v-white-base);
      border: 1px solid var(--v-primary-lighten1);
      box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, 0.1);
      border-left: solid 10px var(--v-primary-lighten6);
      display: flex;
      align-items: center;
      height: 60px;
      .condition-container {
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 26px;
        .condition-items {
          display: flex;
          align-items: center;
          width: 100%;
          flex: 1 0;
          .range-attribute-container {
            width: 100%;
            .density-slider {
              position: relative;
              top: -20px;
            }
          }
          .hux-dropdown {
            .v-btn__content {
              color: var(--v-black-darken1);
            }
            button {
              margin: 0 8px 0 0 !important;
              min-width: 170px !important;
            }
          }
          .avatar-menu {
            margin-right: 20px;
            max-width: 200px;
            border: solid 1px var(--v-black-lighten3);
            flex-grow: 1;
            button {
              width: 100%;
              justify-content: left;
              min-width: unset;
              box-shadow: none !important;
              height: 30px;
              .v-btn__content {
                justify-content: space-between;
                text-overflow: ellipsis;
              }
            }
          }
          .item-text-field {
            flex-grow: 1;
            label {
              margin-bottom: 0 !important;
            }
          }
          .v-text-field {
            .v-input__slot {
              min-height: inherit;
              height: 40px;
              border: solid 1px var(--v-black-lighten3) !important;
              border-radius: 0;
              margin-bottom: 0;
              box-shadow: inherit;
              fieldset {
                border: 0;
              }
            }
            .v-text-field__details {
              display: none;
            }
          }
          .hux-range-slider {
            .v-messages {
              display: none;
            }
            .v-slider--horizontal {
              margin-right: 0px !important;
              .v-slider__track-container {
                width: 101%;
              }
            }
          }
        }
        .condition-actions {
          flex: 0 1;
        }
      }
    }
    .condition-summary {
      background: var(--v-white-base);
    }
  }
  ::v-deep .add-wrap {
    display: flex;
    .add-section {
      background: var(--v-primary-lighten1);
      border: 1px solid var(--v-black-lighten2);
      border-radius: 5px;
      display: flex;
      align-items: center;
      height: 60px;
      .add-new {
        margin-bottom: 6px;
      }
    }
  }
  ::v-deep .condition-summary {
    border: solid 1px var(--v-black-lighten2);
    border-radius: 10px;
    background: var(--v-primary-lighten1);
    padding: 10px 15px;
    display: flex;
    flex-direction: column;
    .title {
      line-height: 16px;
    }
    .value {
      line-height: 19px;
    }
    width: 97px;
    height: 60px;
  }
}
</style>
