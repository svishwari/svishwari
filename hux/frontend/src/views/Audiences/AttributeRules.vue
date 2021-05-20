<template>
  <v-col cols="12" class="attribute-rule pt-0 pl-0 pr-0">
    <v-col cols="12" class="pr-0">
      <strong class="text-h5 neroBlack--text"
        >Select attribute(s) - <i style="font-size: 12px">Optional</i></strong
      >
      <v-card
        tile
        elevation="0"
        class="mt-2 blank-section"
        v-if="rules.length == 0"
      >
        <v-card-actions class="pr-0">
          <v-list-item class="grow">
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-1 font-weight-normal"
                >You have not added any attributes, yet!</v-list-item-title
              >
            </v-list-item-content>
            <v-row align="center" justify="end">
              <v-icon
                size="30"
                class="add-icon"
                color="primary"
                @click="addNewSection()"
              >
                mdi-plus-circle
              </v-icon>
            </v-row>
          </v-list-item>
        </v-card-actions>
      </v-card>
    </v-col>
    <v-col col="12" v-if="rules.length > 0" class="pr-0">
      <div
        v-for="(rule, index) in rules"
        :key="`rule-${index}`"
        class="rule-section"
      >
        <span class="section-title mb-2"
          >Match
          <huxSwitch
            v-model="rule.operand"
            :switchLabels="switchOptions"
          ></huxSwitch>
          of the following
        </span>
        <div
          class="col-12 row pt-0 pb-2 pr-0"
          v-for="(condition, ixcondition) in rule.conditions"
          :key="`${index}-ruleCondition-${ixcondition}`"
        >
          <div class="condition-card col-10 d-flex align-center">
            <div class="options col-sm-10 d-flex align-center">
              <DropdownMenu
                v-model="condition.attribute"
                :labelText="fetchDropdownLabel(condition, 'attribute')"
                :menuItem="attributeOptions"
                class="col-sm-4"
              ></DropdownMenu>
              <DropdownMenu
                v-model="condition.operator"
                :labelText="fetchDropdownLabel(condition, 'operator')"
                :menuItem="conditionOptions"
                v-if="condition.attribute"
              ></DropdownMenu>
              <text-field
                v-model="condition.text"
                placeholder="Text"
                v-if="condition.operator"
              ></text-field>
            </div>
            <div
              class="actions col-sm-2 d-flex align-center justify-content-end"
            >
              <v-btn icon color="primary" @click="addNewCondition(rule.id)">
                <v-icon>mdi-plus-circle</v-icon>
              </v-btn>
              <v-btn
                icon
                color="primary"
                @click="removeCondition(rule, ixcondition)"
              >
                <v-icon>mdi-delete-outline</v-icon>
              </v-btn>
            </div>
          </div>
          <div class="col-2 pt-0 pr-0 pb-0">
            <div class="condition-summary">
              <span class="title">Size</span>
              <span>{{ condition.outputSummary }}</span>
            </div>
          </div>
        </div>
        <div class="col-12 row seperator mt-5 mb-1" v-if="index != lastIndex">
          <hr />
          <v-chip :ripple="false">OR</v-chip>
        </div>
        <div class="add-section-wrap" v-if="index == lastIndex">
          <v-col col="12" class="row pr-0">
            <div class="add-section col-10">
              <v-btn icon color="primary" @click="addNewSection()">
                <v-icon>mdi-plus-circle</v-icon>
              </v-btn>
              <span>New section</span>
            </div>
            <div class="col-2 pt-0 pr-0 pb-0">
              <div class="condition-summary">
                <span class="title">Result Size</span>
                <span>35,645,000</span>
              </div>
            </div>
          </v-col>
        </div>
      </div>
    </v-col>
  </v-col>
</template>

<script>
import DropdownMenu from "../../components/common/DropdownMenu.vue"
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
    DropdownMenu,
    TextField,
    huxSwitch,
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
      attributeOptions: [{ value: "Name" }],
      conditionOptions: [
        { value: "Contains" },
        { value: "Does not contain" },
        { value: "Equals" },
        { value: "Does not equal" },
      ],
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
    lastIndex() {
      return this.rules.length - 1
    },
  },
  methods: {
    operandLabel(rule) {
      return rule.operand ? "AND" : "OR"
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

<style lang="scss">
.attribute-rule {
  .blank-section {
    background: var(--v-background-base);
    border: 1px solid var(--v-zircon-base);
    box-sizing: border-box;
    border-radius: 5px !important;
    .text-subtitle-1 {
      color: var(--v-gray-base);
    }
  }
  .rule-section {
    .section-title {
      display: flex;
      align-items: center;
      font-size: 12px;
      line-height: 16px;
      font-weight: normal;
      .v-input {
        margin-left: 15px;
      }
    }
    .condition-card {
      background: var(--v-white-base);
      border: 1px solid var(--v-background-base);
      box-sizing: border-box;
      box-shadow: 0px 3px 8px var(--v-lightGrey-base);
      border-left: solid 10px var(--v-aliceBlue-base);
      min-height: 60px;
      max-height: 60px;
      padding: 16px 14px 19px 14px;
      padding-left: 16px;
      justify-content: space-between;
      .options {
        display: flex;
        align-items: center;
        .avatar-menu {
          display: block;
          margin-right: 20px;
          min-width: 180px;
          border: solid 1px var(--v-lightGrey-base);
          button {
            width: 100%;
            justify-content: left;
            box-shadow: none !important;
            .v-btn__content {
              justify-content: space-between;
            }
          }
        }
        .v-text-field {
          .v-input__slot {
            min-height: inherit;
            height: 38px;
            border: solid 1px var(--v-lightGrey-base);
            border-radius: 0;
          }
          .v-text-field__details {
            display: none;
          }
        }
      }
    }
    .condition-summary {
      background: var(--v-white-base);
    }
  }
  .add-section-wrap {
    .add-section {
      background: var(--v-background-base);
      border: 1px solid var(--v-zircon-base);
      box-sizing: border-box;
      border-radius: 5px;
      span {
        color: #005587;
      }
    }
  }
  .condition-summary {
    margin-left: 15px;
    border: solid 1px var(--v-lightGrey-base);
    border-radius: 10px;
    background: var(--v-background-base);
    min-height: 60px;
    max-height: 60px;
    padding: 10px 15px;
    display: flex;
    flex-direction: column;
    .title {
      font-family: Open Sans !important;
      font-style: normal;
      font-weight: normal;
      font-size: 12px !important;
      line-height: 16px;
    }
    .value {
      font-family: Open Sans SemiBold;
      font-style: normal;
      font-weight: 600;
      font-size: 14px;
      line-height: 19px;
    }
  }
  .seperator {
    position: relative;
    hr {
      width: 100%;
      border-style: solid;
      border-color: var(--v-zircon-base);
    }
    .v-chip {
      position: absolute;
      top: 0;
      transform: translateX(-50px);
      left: 50%;
      background: var(--v-zircon-base) !important;
    }
  }
}
</style>
