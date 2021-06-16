<template>
  <v-col cols="12" class="attribute-rule pt-0 pl-0 pr-0">
    <v-col cols="12" class="pr-0">
      <strong class="text-h5 neroBlack--text">
        Select attribute(s) - <i style="font-size: 12px">Optional</i>
      </strong>
      <v-card
        tile
        elevation="0"
        class="mt-2 blank-section"
        v-if="rules.length == 0"
      >
        <div class="gray--text font-weight-normal">
          You have not added any attributes, yet!
        </div>
        <v-icon
          size="30"
          class="add-icon"
          color="primary"
          @click="addNewSection()"
        >
          mdi-plus-circle
        </v-icon>
      </v-card>
    </v-col>
    <v-col col="12" v-if="rules.length > 0" class="pt-0 pr-0">
      <div v-for="(rule, index) in rules" :key="`rule-${index}`">
        <div class="d-flex align-center mb-2 col-12 pa-0">
          <span class="mr-2">Match</span>
          <huxSwitch v-model="rule.operand" :switchLabels="switchOptions" />
          of the following
        </div>

        <div
          v-for="(condition, ixcondition) in rule.conditions"
          :key="`${index}-ruleCondition-${ixcondition}`"
          class="rule-section mb-2"
        >
          <div class="condition-card col-10 pa-0">
            <div class="condition-container">
              <div class="condition-items col-10 pa-0">
                <hux-dropdown
                  :selected="condition.attribute"
                  :label="fetchDropdownLabel(condition, 'attribute')"
                  @on-select="onSelect('attribute', condition, $event)"
                  :items="attributeOptions"
                />
                <hux-dropdown
                  :label="fetchDropdownLabel(condition, 'operator')"
                  :selected="condition.operator"
                  @on-select="onSelect('operator', condition, $event)"
                  :items="operatorOptions"
                  v-if="isText(condition)"
                />
                <TextField
                  v-if="condition.operator"
                  v-model="condition.text"
                  placeholder="Text"
                  required
                  class="item-text-field"
                />
              </div>
              <div class="condition-actions col-2 pa-0">
                <v-icon @click="addNewCondition(rule.id)" color="primary"
                  >mdi-plus-circle</v-icon
                >
                <v-icon
                  @click="removeCondition(rule, ixcondition)"
                  color="primary"
                  >mdi-delete-outline</v-icon
                >
              </div>
            </div>
          </div>
          <div class="condition-summary col-2">
            <span class="title text-caption">Size</span>
            <span class="value text-h6 pt-1 font-weight-semi-bold">{{
              condition.outputSummary
            }}</span>
          </div>
        </div>

        <div class="col-12 seperator mt-5 mb-1" v-if="index != lastIndex">
          <hr />
          <v-chip
            small
            class="mx-2 my-1 font-weight-semi-bold"
            text-color="primary"
            color="pillBlue"
            :ripple="false"
          >
            OR
          </v-chip>
        </div>
      </div>
      <div class="add-section-wrap">
        <div class="add-section pl-4 col-10">
          <v-btn icon color="primary" @click="addNewSection()">
            <v-icon>mdi-plus-circle</v-icon>
          </v-btn>
          <span class="primary--text pl-1">New section</span>
        </div>
        <div class="condition-summary col-2">
          <span class="title text-caption">Result Size</span>
          <span class="value text-h6 pt-1 font-weight-semi-bold">35.6M</span>
        </div>
      </div>
    </v-col>
  </v-col>
</template>

<script>
import { mapGetters } from "vuex"
import HuxDropdown from "../../components/common/HuxDropdown.vue"
import huxSwitch from "../../components/common/Switch.vue"
import TextField from "../../components/common/TextField.vue"

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
  outputSummary: "-",
}

export default {
  name: "AttributeRules",
  components: {
    TextField,
    huxSwitch,
    HuxDropdown,
  },
  props: {
    rules: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  data() {
    return {
      switchOptions: [
        {
          condition: true,
          label: "ALL",
        },
        {
          condition: false,
          label: "ANY",
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      ruleAttributes: "audiences/audiencesRules",
    }),
    attributeOptions() {
      const options = []
      const masterAttributes = this.ruleAttributes.rule_attributes
      Object.keys(masterAttributes).forEach((groupKey) => {
        const _group_items = []
        const order = groupKey.includes("model") ? 0 : 1
        const group = {
          name: groupKey,
          isGroup: true,
        }
        _group_items.push(group)
        _group_items.push(
          ...Object.keys(masterAttributes[groupKey]).map((key) => {
            const _subOption = masterAttributes[groupKey][key]
            const hasSubOptins = Object.keys(_subOption).filter((item) =>
              _subOption[item].hasOwnProperty("name")
            )
            if (hasSubOptins.length > 0) {
              _subOption["menu"] = hasSubOptins.map((key) => _subOption[key])
              hasSubOptins.forEach((key) => delete _subOption[key])
            }
            return _subOption
          })
        )
        _group_items.forEach((item) => (item["order"] = order))
        options.push(..._group_items)
      })
      return options.sort(function (a, b) {
        return a.order < b.order
      })
    },
    operatorOptions() {
      return Object.keys(this.ruleAttributes.text_operators).map((key) => ({
        key: key,
        name: this.ruleAttributes.text_operators[key],
      }))
    },
    lastIndex() {
      return this.rules.length - 1
    },
  },
  methods: {
    operandLabel(rule) {
      return rule.operand ? "AND" : "OR"
    },
    isText(condition) {
      return condition.attribute ? condition.attribute[type] === "text" : false
    },
    onSelect(type, cond, item) {
      cond[type] = item
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
    },
    addNewSection() {
      const newSection = JSON.parse(JSON.stringify(NEW_RULE_SECTION))
      newSection.id = Math.floor(Math.random() * 1024).toString(16)
      this.rules.push(newSection)
      this.addNewCondition(newSection.id)
    },
    fetchDropdownLabel(condition, type) {
      const prefix = "Select "
      return condition[type] ? condition[type] : prefix + type
    },
  },
}
</script>

<style lang="scss" scoped>
.attribute-rule {
  ::v-deep .blank-section {
    background: var(--v-background-base);
    border: 1px solid var(--v-zircon-base);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 5px !important;
    padding: 14px 16px;
  }
  ::v-deep .seperator {
    position: relative;
    hr {
      border-style: solid;
      border-color: var(--v-zircon-base);
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
      border: 1px solid var(--v-background-base);
      box-shadow: 0px 3px 8px var(--v-lightGrey-base);
      border-left: solid 10px var(--v-aliceBlue-base);
      display: flex;
      align-items: center;
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
          .avatar-menu {
            margin-right: 20px;
            max-width: 200px;
            border: solid 1px var(--v-lightGrey-base);
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
              border: solid 1px var(--v-lightGrey-base) !important;
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
      background: var(--v-background-base);
      border: 1px solid var(--v-zircon-base);
      border-radius: 5px;
      display: flex;
      align-items: center;
    }
  }
  ::v-deep .condition-summary {
    border: solid 1px var(--v-zircon-base);
    border-radius: 10px;
    margin-left: 15px;
    background: var(--v-background-base);
    padding: 10px 15px;
    display: flex;
    flex-direction: column;
    width: 120px;
    .title {
      line-height: 16px;
    }
    .value {
      line-height: 19px;
    }
  }
}
</style>
