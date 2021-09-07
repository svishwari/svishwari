<template>
  <v-col cols="12" class="attribute-rule pt-0 pl-0 pr-0">
    <v-col cols="12" class="pa-0">
      <strong
        v-if="enableTitle"
        :class="{
          'text-h5 black--text text--darken-4': true,
          'text-caption': applyCaptionStyle,
        }"
      >
        Select attribute(s) -
        <i class="text-caption black--text text--darken-1">Optional</i>
      </strong>
      <v-card v-if="rules.length == 0" tile elevation="0" class="blank-section">
        <div
          class="black--text text--darken-1 font-weight-normal new-attribute"
        >
          <span @click="addNewSection()">
            <icon class="add-icon cursor-pointer" type="add" :size="41" />
          </span>
          <span class="ml-4 no-attribute">
            You have not added any attributes, yet.
          </span>
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
            text--darken-4 text-caption
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
          col="12"
          class="rule-section pa-0 mb-2"
        >
          <v-col md="10" class="pa-0">
            <div class="condition-card">
              <div class="condition-container pl-2">
                <div class="condition-items col-10 pa-0">
                  <hux-dropdown
                    :selected="condition.attribute"
                    :items="attributeOptions()"
                    label="Select attribute"
                    @on-select="onSelect('attribute', condition, $event)"
                  />
                  <hux-dropdown
                    v-if="isText(condition)"
                    label="Select operator"
                    :items="operatorOptions(condition)"
                    :selected="condition.operator"
                    @on-select="onSelect('operator', condition, $event)"
                  />
                  <text-field
                    v-if="condition.operator && isText(condition)"
                    v-model="condition.text"
                    class="item-text-field"
                    :placeholder="getPlaceHolderText(condition)"
                    required
                    @blur="triggerSizing(condition)"
                  />
                  <hux-slider
                    v-if="condition.attribute && !isText(condition)"
                    v-model="condition.range"
                    :read-only="false"
                    :min="condition.attribute.min"
                    :max="condition.attribute.max"
                    :step="condition.attribute.steps"
                    is-range-slider
                    @onFinalValue="triggerSizing(condition)"
                  />
                </div>
                <div class="condition-actions col-2 pa-0">
                  <v-icon color="primary" @click="addNewCondition(rule.id)">
                    mdi-plus-circle
                  </v-icon>
                  <v-icon
                    color="primary"
                    @click="removeCondition(rule, ixcondition)"
                  >
                    mdi-delete-outline
                  </v-icon>
                </div>
              </div>
            </div>
          </v-col>
          <v-col md="2" class="pr-0 py-0 pl-5">
            <div class="condition-summary">
              <span class="title text-caption">Size</span>
              <span class="value text-h6 pt-1 font-weight-semi-bold">
                <v-progress-circular
                  v-if="condition.awaitingSize"
                  :value="16"
                  indeterminate
                />
                <span v-if="!condition.awaitingSize">
                  {{ condition.size | Numeric(false, false, true) }}
                </span>
              </span>
            </div>
          </v-col>
        </v-col>

        <div v-if="index != lastIndex" class="col-12 seperator mt-5 mb-1">
          <hr class="zircon" />
          <v-chip
            small
            class="mx-2 my-1 font-weight-semi-bold"
            text-color="primary"
            color="primary lighten-4"
            :ripple="false"
          >
            OR
          </v-chip>
        </div>
      </div>
      <div class="add-section-wrap">
        <v-col md="10" class="pa-0 pt-3">
          <div class="add-section pa-5">
            <span @click="addNewSection()">
              <icon
                class="add-icon cursor-pointer mt-1"
                type="add"
                :size="30"
              />
            </span>
            <span class="primary--text pl-1 add-new">New section</span>
          </div>
        </v-col>
        <v-col md="2" class="pr-0 pl-5">
          <div class="condition-summary">
            <span class="title text-caption">Result Size</span>
            <span class="value text-h6 pt-1 font-weight-semi-bold">
              <v-progress-circular
                v-if="loadingOverAllSize"
                :value="16"
                indeterminate
              />
              <span v-else>
                {{ overAllSize | Numeric(false, false, true) }}
              </span>
            </span>
          </div>
        </v-col>
      </div>
    </v-col>
  </v-col>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import HuxDropdown from "../../components/common/HuxDropdown.vue"
import HuxSlider from "../../components/common/HuxSlider.vue"
import HuxSwitch from "../../components/common/Switch.vue"
import TextField from "../../components/common/TextField.vue"
import Icon from "@/components/common/Icon"

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
    Icon,
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
    await this.getAudiencesRules()
    this.updateSizes()
  },
  methods: {
    ...mapActions({
      getRealtimeSize: "audiences/fetchFilterSize",
      getAudiencesRules: "audiences/fetchConstants",
    }),
    isText(condition) {
      return condition.attribute ? condition.attribute.type === "text" : false
    },
    /**
     * This attributeOptions is transforming the API attributeRules into the Options Array
     *
     * Segregating the Groups which are the parent key.
     * Appending the sub options next to the group label.
     *
     * Also, having an Top Priority Order to Models.
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
    operatorOptions(condition) {
      // Filter out only two options (equals and does_not_equals) for attribute type 'gender'
      if (condition.attribute.key === "gender") {
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
      let data = await this.getRealtimeSize(filterJSON)
      condition.size = data.total_customers
      condition.awaitingSize = false
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
      let data = await this.getRealtimeSize(filterJSON)
      this.$emit("updateOverview", data)
      this.overAllSize = data.total_customers
      this.loadingOverAllSize = false
    },

    onSelect(type, condition, item) {
      condition[type] = item
      if (type === "attribute") {
        condition.operator = ""
        condition.text = ""
        condition.range = [condition.attribute.min, condition.attribute.max]
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
    border: 1px solid var(--v-zircon-base);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 5px !important;
    padding: 14px 16px;
    .new-attribute {
      display: flex;
      height: 39px;
      .no-attribute {
        margin-top: 8px;
      }
    }
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
      box-shadow: 0px 3px 8px var(--v-black-lighten3);
      border-left: solid 10px var(--v-primary-lighten2);
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
              height: 32px;
              border: solid 1px var(--v-black-lighten3) !important;
              border-radius: 0;
              margin-bottom: 0;
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
          }
        }
        .condition-actions {
          text-align: end;
        }
      }
    }
    .condition-summary {
      background: var(--v-white-base);
    }
  }
  ::v-deep .add-section-wrap {
    display: flex;
    .add-section {
      background: var(--v-primary-lighten1);
      border: 1px solid var(--v-zircon-base);
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
    border: solid 1px var(--v-zircon-base);
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
    width: 130px;
  }
}
</style>
