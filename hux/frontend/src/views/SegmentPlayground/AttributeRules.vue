<template>
  <v-col cols="12" class="attribute-rule pt-0 pl-0 pr-0">
    <v-col cols="12" class="pa-0">
      <strong
        v-if="enableTitle"
        :class="{
          'text-body-1 black--text text--darken-4 mb-2 d-block': true,
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
    <v-col v-if="getRules.length > 0" col="12" class="pt-0 pr-0 pa-0">
      <div v-for="(rule, index) in getRules" :key="rule.id">
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
          <span class="mr-2 mb-2">Include consumers that match &nbsp;</span>
          <hux-switch
            v-model="rule.operand"
            :is-disabled="readMode ? true : false"
            class="mt-2 pt-0"
            @input="triggerSizingForRule(rule)"
          />
          <span class="mb-2"> of the following: </span>
        </div>
        <div
          v-for="(condition, ixcondition) in rule.conditions"
          :key="condition.id"
        >
          <v-col class="rule-section pa-0 mb-2 d-flex">
            <div class="pa-0 pr-2 flex-fill">
              <div
                :class="readMode ? 'readmode-condition-card' : 'condition-card'"
              >
                <div class="condition-container px-4 d-flex">
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
                        condition.operator &&
                        condition.operator.key != 'between' &&
                        condition.attribute.type === 'text'
                      "
                      v-model="condition.text"
                      class="item-text-field"
                      placeholder="Enter value"
                      required
                      @blur="triggerSizing(condition)"
                    />

                    <hux-dropdown
                      v-if="
                        condition.operator &&
                        condition.operator.key != 'between' &&
                        condition.attribute.type === 'text'
                      "
                      label="Select time"
                      :items="ruleAttributes.allowed_timedelta_types"
                      :selected="condition.delta_type"
                      data-e2e="select-time-btn"
                      @on-select="onSelect('time', condition, $event)"
                    />
                    <div
                      v-if="
                        condition.operator.key == 'between' &&
                        condition.attribute.type === 'text'
                      "
                      class="d-flex align-center mr-2"
                    >
                      <div>
                        <hux-start-date
                          :label="selectedStartDate"
                          :selected="selectedStartDate"
                          @on-date-select="onStartDateSelect($event, condition)"
                        />
                      </div>
                      <div>
                        <icon
                          class="mx-1 mt-3"
                          type="arrow"
                          :size="19"
                          color="primary"
                          variant="lighten6"
                        />
                      </div>
                      <div>
                        <hux-end-date
                          :label="selectedEndDate"
                          :selected="selectedEndDate"
                          :is-sub-menu="true"
                          :min-date="endMinDate"
                          @on-date-select="onEndDateSelect($event, condition)"
                        />
                      </div>
                    </div>

                    <span
                      v-if="
                        condition.operator &&
                        condition.attribute.type === 'text'
                      "
                      class="ml-4 text-body-1 primary--text cursor-pointer"
                      @click="
                        condition.rules && condition.rules.length > 0
                          ? addNewSubCondition(condition.rules[0].id, condition)
                          : addNewSubSection(condition)
                      "
                      >+ Product</span
                    >

                    <hux-autocomplete
                      v-if="
                        condition.operator &&
                        condition.attribute.type === 'list'
                      "
                      v-model="condition.text"
                      :options="listOptions(condition)"
                      data-e2e="auto-complete-btn"
                      :loader="loaderValue"
                      :placeholder="getPlaceHolderText(condition)"
                      @change="triggerSizing(condition)"
                      @search-update="autoSearchFunc"
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
                        :read-mode="readMode"
                        class="ml-2 mr-0"
                      />
                      <hux-slider
                        v-model="condition.range"
                        :read-only="readMode ? true : false"
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
                        :read-mode="readMode"
                        @onFinalValue="triggerSizing(condition)"
                      />
                    </div>
                  </div>
                  <div
                    v-if="!readMode"
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
          <v-col
            v-if="condition.rules && condition.rules.length > 0"
            col="12"
            class="pt-0 pr-0 pa-0"
          >
            <div v-for="sub_rule in condition.rules" :key="sub_rule.id">
              <div
                class="
                  d-flex
                  align-center
                  pa-0
                  black--text
                  text--darken-4 text-body-2
                  ml-15
                "
              >
                <span class="mr-2 mb-2">And include &nbsp;</span>
                <hux-switch
                  v-model="sub_rule.operand"
                  :is-disabled="readMode ? true : false"
                  class="mt-2 pt-0"
                  @input="triggerSizingForRule(sub_rule)"
                />
                <span class="mb-2"> of the following products: </span>
              </div>
              <div
                v-for="(sub_condition, indcondition) in sub_rule.conditions"
                :key="sub_condition.id"
              >
                <v-col class="rule-section pa-0 mb-2 d-flex">
                  <div class="pa-0 pr-2 flex-fill">
                    <div
                      :class="[
                        readMode
                          ? 'readmode-condition-card ml-15'
                          : 'condition-card ml-15',
                      ]"
                    >
                      <div class="condition-container px-4 d-flex">
                        <div class="condition-items pr-5">
                          <text-field
                            v-model="sub_condition.attribute.name"
                            class="item-text-field"
                            placeholder="Enter value"
                            required
                          />
                          <hux-dropdown
                            v-if="isTextORSelect(sub_condition)"
                            label="Select operator"
                            :items="operatorOptions(sub_condition)"
                            :selected="sub_condition.operator"
                            data-e2e="select-sub-operator-btn"
                            @on-select="
                              onSelect('operator', sub_condition, $event)
                            "
                          />

                          <hux-dropdown
                            :selected="sub_condition.text"
                            :items="ruleAttributes.products"
                            label="Select product"
                            data-e2e="select-product-btn"
                            @on-select="
                              onSelect('text', sub_condition, $event, condition)
                            "
                          />

                          <!-- <hux-autocomplete
                            v-if="
                              sub_condition.operator &&
                              sub_condition.attribute.type === 'list'
                            "
                            v-model="sub_condition.text"
                            :options="ruleAttributes.products"
                            data-e2e="auto-complete-btn"
                            :loader="loaderValue"
                            :placeholder="getPlaceHolderText(sub_condition)"
                            @change="triggerSizing(condition)"
                            @search-update="autoSearchFunc"
                          /> -->
                        </div>
                        <div
                          v-if="!readMode"
                          class="condition-actions pa-0 cursor-pointer"
                          data-e2e="remove-attr"
                          @click="
                            removeCondition(
                              sub_rule,
                              indcondition,
                              condition.rules
                            )
                          "
                        >
                          <icon type="trash" :size="18" color="black" />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div
                    class="pr-0 py-0 flex-right"
                    :class="{
                      invisible: sub_condition.attribute.key == 'product',
                    }"
                  >
                    <div class="condition-summary">
                      <span class="title text-h5">Rule Size</span>
                      <span v-if="sub_condition.awaitingSize" class="pt-2">
                        <v-progress-linear
                          indeterminate
                          buffer-value="0"
                          stream
                        />
                      </span>
                      <span v-else class="value text-h6 pt-1 text-subtitle-1">
                        {{ sub_condition.size | Numeric(false, false, true) }}
                      </span>
                    </div>
                  </div>
                </v-col>
              </div>
            </div>
          </v-col>
        </div>
        <div class="add-wrap">
          <div class="pa-0 flex-fill new-attribute">
            <div class="add-section pa-5 text-body-1 primary--text">
              <span
                class="cursor-pointer"
                data-e2e="add-another-attr"
                @click="addNewCondition(rule.id)"
              >
                <icon type="plus" color="primary" :size="12" class="mr-1" />
                New attribute
              </span>
            </div>
          </div>
          <div class="pr-0 pl-2 flex-right">
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
        <div v-if="index != lastIndex" class="col-12 seperator mt-4 mb-1 px-0">
          <hr class="black lighten-2" />
          <v-chip
            small
            class="mx-2 my-1 text-body-2"
            :text-color="readMode ? 'white' : 'primary'"
            :color="readMode ? 'black lighten-3' : 'primary lighten-3'"
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
          :text-color="readMode ? 'white' : 'primary'"
          :color="readMode ? 'black lighten-3' : 'primary lighten-3'"
          :ripple="false"
          @click.native="!readMode && addNewSection()"
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
import { v4 as uuidv4 } from "uuid"
import { cloneDeep } from "lodash"
import HuxStartDate from "@/components/common/DatePicker/HuxStartDate"
import HuxEndDate from "@/components/common/DatePicker/HuxEndDate"

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
  selection_type: "",
  delta_type: "",
}

const PRODUCT_NEW_CONDITION = {
  id: "",
  attribute: {
    key: "product",
    name: "Product",
    type: "list",
  },
  operator: "",
  text: "",
  range: [],
  awaitingSize: false,
  outputSummary: "0",
  size: "-",
  selection_type: undefined,
  delta_type: undefined,
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
    HuxStartDate,
    HuxEndDate,
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
    readMode: {
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
      currentData: [],
      currentCityData: [],
      selectedValue: null,
      params: {},
      loaderValue: false,
      selectedStartDate: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      selectedEndDate: "Select date",
      endMinDate: new Date(
        new Date().getTime() - new Date().getTimezoneOffset() * 60000
      ).toISOString(),
    }
  },
  computed: {
    ...mapGetters({
      ruleAttributes: "audiences/audiencesRules",
      overviewData: "customers/overview",
    }),

    lastIndex() {
      return this.rules.length - 1
    },

    ifRouteSegmentPlayground() {
      return this.$route.name === "SegmentPlayground"
    },

    getRules() {
      return this.rules
    },
  },

  async mounted() {
    this.sizeHandler()
    this.chartDimensions.height = 26
    await this.getAudiencesRules()
    this.updateSizes()
    if (this.ifRouteSegmentPlayground) {
      this.overAllSize = this.overviewData.total_customers
    }
    this.$emit("attribute-options", this)
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
      getAudiencesRulesByFields: "audiences/rulesByFields",
      attributesData: "audiences/getDensityChartData",
    }),
    sliderLabel(attribute, value) {
      if (attribute.selection_type == "value") {
        if (attribute.key === "ltv_predicted") {
          return `$${value}`
        }
        return value
      } else if (attribute.selection_type == "percentage") {
        return `${Math.floor((value / (attribute.max - attribute.min)) * 100)}%`
      }
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
        ? ["text", "list"].includes(condition.attribute.type)
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
                  subOption["key"] = key
                  return subOption
                })
              }
              if (groupKey.includes("model")) {
                _subOption["modelIcon"] = "model"
                _subOption["selected"] = "value"
                _subOption["menu"] = [
                  {
                    key: "value",
                    name: "Value",
                    type: "range",
                  },
                  {
                    key: "percentage",
                    name: "Decile percentage",
                    type: "range",
                  },
                ]
                _subOption.menu.forEach((item) => {
                  let tempobj = cloneDeep(_subOption)
                  delete tempobj.menu
                  item.model = tempobj
                })
              }
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
      if (condition.attribute.key === "city") {
        // if (this.currentCityData.length == 0) {
        //   this.selectedValue = "City"
        //   this.autoSearchFunc(condition.text)
        // }
        return this.currentCityData
      } else if (condition.attribute.key === "zip") {
        // if (this.currentData.length == 0) {
        //   this.selectedValue = "Zip"
        //   this.autoSearchFunc(condition.text)
        // }
        return this.currentData
      } else {
        return condition.attribute.options
      }
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
      } else if (condition.attribute.type === "text") {
        return Object.keys(this.ruleAttributes.text_operators)
          .map((key) => {
            if (key.includes("within_the_last") || key == "between") {
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
      } else if (condition.operator && condition.attribute.type === "text") {
        if (condition.operator.key == "between") {
          value = [this.selectedStartDate, this.selectedEndDate]
        } else {
          value = [condition.text]
        }

        type = condition.operator.key
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
                selection_type: condition.selection_type,
                delta_type: condition.delta_type.key,
              },
            ],
          },
        ],
      }

      if (condition.rules?.length > 0) {
        filterJSON.filters[0].section_filters[0].sub_filters = [
          {
            sub_section_aggregator: "All",
            sub_section_filters: [],
          },
        ]
        condition.rules[0].conditions.forEach((item) => {
          filterJSON.filters[0].section_filters[0].sub_filters[0].sub_section_filters.push(
            {
              field: item.attribute.key,
              type: item.attribute.type,
              value: item.text.key,
            }
          )
        })
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
      console.log(this.rules)
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
          } else if (
            this.rules[i].conditions[j].operator &&
            this.rules[i].conditions[j].attribute.type === "text"
          ) {
            if (this.rules[i].conditions[j].operator.key == "between") {
              value = [this.selectedStartDate, this.selectedEndDate]
            } else {
              value = [this.rules[i].conditions[j].text]
            }

            type = this.rules[i].conditions[j].operator.key
          } else {
            value = this.rules[i].conditions[j].text
            type = this.rules[i].conditions[j].operator.key
          }

          let sub_filters = []

          if (this.rules[i].conditions[j].rules?.length > 0) {
            for (let a = 0; a < this.rules[i].conditions[j].rules.length; a++) {
              let aggregatorOperand = this.rules[i].conditions[j].rules[a]
                .operand
                ? "ALL"
                : "ANY"
              let attributeRulesArray = []
              for (
                let b = 0;
                b < this.rules[i].conditions[j].rules[a].conditions.length;
                b++
              ) {
                if (this.rules[i].conditions[j].rules[a].conditions[b].text) {
                  attributeRulesArray.push({
                    field:
                      this.rules[i].conditions[j].rules[a].conditions[b]
                        .attribute.key,
                    type: this.rules[i].conditions[j].rules[a].conditions[b]
                      .operator.key,
                    value:
                      this.rules[i].conditions[j].rules[a].conditions[b].text
                        .key,
                  })
                }
              }
              let sectionObject = {
                sub_section_aggregator: aggregatorOperand,
                sub_section_filters: attributeRulesArray,
              }
              sub_filters.push(sectionObject)
            }
          }

          if (value) {
            let filterObj = {
              field: this.rules[i].conditions[j].attribute.key,
              type: type,
              value: value,
              selection_type: this.rules[i].conditions[j].selection_type,
              delta_type: this.rules[i].conditions[j].delta_type.key,
            }
            if (sub_filters.length > 0) {
              filterObj.sub_filters = sub_filters
            }
            attributeRulesArray.push(filterObj)
          }
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

    async onSelect(type, condition, item, parent = null) {
      let dataItem = item.model ? item.model : item
      condition[type] = dataItem
      if (type === "attribute") {
        this.selectedValue = dataItem.key
        if (dataItem.type == "range") {
          let data = await this.attributesData({
            field: dataItem.modelIcon ? "model" : dataItem.key,
            model: dataItem.modelIcon ? dataItem.key : null,
          })
          if (data) {
            data.key = dataItem.key
            data.selection_type = dataItem.selected
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
        condition.selection_type = dataItem.selection_type
      } else if (type === "operator") {
        condition.text = ""
        condition.range = []
        condition.awaitingSize = false
        condition.outputSummary = 0
      } else if (type == "time") {
        condition.delta_type = dataItem
        this.triggerSizing(condition)
      } else if (type == "text") {
        condition.text = item
        if (parent) this.triggerSizing(parent)
      }
      this.$forceUpdate()
    },
    addNewCondition(id) {
      const newCondition = JSON.parse(JSON.stringify(NEW_CONDITION))
      newCondition.id = uuidv4()
      const sectionFound = this.rules.filter((rule) => rule.id === id)
      if (sectionFound.length > 0) sectionFound[0].conditions.push(newCondition)
    },
    addNewSubCondition(id, condition) {
      const newSubCondition = JSON.parse(JSON.stringify(PRODUCT_NEW_CONDITION))
      newSubCondition.id = uuidv4()
      const sectionFound = condition.rules.filter((rule) => rule.id === id)
      if (sectionFound.length > 0)
        sectionFound[0].conditions.push(newSubCondition)
      this.$forceUpdate()
    },
    removeCondition(parent, child, condition_rules = null) {
      if (parent.conditions.length === 1) {
        let ruleSet =
          condition_rules && condition_rules.length > 0
            ? condition_rules
            : this.rules
        const indx = ruleSet.findIndex((rul) => rul.id === parent.id)
        ruleSet.splice(indx, 1)
      } else {
        parent.conditions.splice(child, 1)
      }
      this.getOverallSize()
    },
    getPlaceHolderText(condition) {
      switch (condition.attribute.name) {
        case "Email":
          return "example@email.com"
        case "Gender":
          return "Type male, female, or other"
        case "City":
        case "Country":
        case "State":
          return condition.attribute.name + " name"
        default:
          return condition.attribute.name
      }
    },
    addNewSection() {
      const newSection = JSON.parse(JSON.stringify(NEW_RULE_SECTION))
      newSection.id = uuidv4()
      this.rules.push(newSection)
      this.addNewCondition(newSection.id)
    },
    addNewSubSection(condition) {
      const newSection = JSON.parse(JSON.stringify(NEW_RULE_SECTION))
      newSection.id = uuidv4()
      condition.rules?.length > 0
        ? condition.rules.push(newSection)
        : (condition["rules"] = [newSection])
      this.addNewSubCondition(newSection.id, condition)
      this.$forceUpdate()
    },
    async autoSearchFunc(value) {
      if (value !== null && value !== "" && value !== undefined) {
        if (this.selectedValue === "Zip" || this.selectedValue === "City") {
          this.params.fieldType =
            this.selectedValue === "Zip"
              ? "zip_code"
              : this.selectedValue.toLowerCase()
          this.params.key = value
          if (value.length > 2 && value.length <= 8) {
            this.loaderValue = true
            let data = await this.getAudiencesRulesByFields(this.params)
            if (this.selectedValue === "Zip") {
              this.loaderValue = false
              this.currentData = [...data]
            } else if (this.selectedValue === "City") {
              this.loaderValue = false
              this.currentCityData = [...data]
            }
          }
        }
      }
      if (
        value === null ||
        value === "" ||
        value === undefined ||
        value.length < 3
      ) {
        if (this.selectedValue === "Zip") {
          this.currentData = []
        } else if (this.selectedValue === "City") {
          this.currentCityData = []
        } else {
          this.currentData = []
          this.currentCityData = []
        }
      }
    },

    onStartDateSelect(val, condition) {
      this.selectedStartDate = val
      this.selectedEndDate = null
      this.endMinDate = val
      this.triggerSizing(condition)
    },
    onEndDateSelect(val, condition) {
      if (!val) {
        this.selectedEndDate = "No end date"
      } else {
        this.selectedEndDate = val
      }
      this.triggerSizing(condition)
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
            max-width: 200px;
            margin-right: 8px;
            label {
              margin-bottom: 0 !important;
            }
          }
          .v-text-field {
            .v-input__slot {
              min-height: inherit;
              height: 40px;
              width: 200px;
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
            ::v-deep .v-input__control .v-input__slot .v-slider__thumb {
              border: none !important;
            }
          }
        }
        .condition-actions {
          flex: 0 1;
        }
      }
    }
    .readmode-condition-card {
      pointer-events: none;
      background: var(--v-white-base);
      border: 1px solid var(--v-primary-lighten1);
      box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, 0.1);
      border-left: solid 10px var(--v-black-lighten3);
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
              .v-icon {
                color: var(--v-black-lighten3) !important;
              }
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
            max-width: 200px;
            margin-right: 8px;
            label {
              margin-bottom: 0 !important;
            }
          }
          .v-text-field {
            .v-input__slot {
              min-height: inherit;
              height: 40px;
              width: 200px;
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

  ::v-deep .hux-date-picker {
    .main-button {
      height: 40px;
      width: 200px !important;
      min-width: 200px;
      margin-left: 0px !important;
      margin-right: 0px !important;
    }
  }

  .invisible {
    visibility: hidden;
  }
}
</style>
