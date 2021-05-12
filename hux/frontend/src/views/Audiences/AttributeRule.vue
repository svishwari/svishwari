<template>
  <v-col cols="12" class="attribute-rule pt-0">
    <v-col cols="12">
      <strong class="text-h6"
        >Select attribute(s) - <i style="font-size: 12px">Optional</i></strong
      >
      <v-card
        color="#F9FAFB"
        tile
        elevation="0"
        style="border: 1px solid #e2eaec"
        class="mt-2"
        v-if="rules.length == 0"
      >
        <v-card-actions>
          <v-list-item class="grow">
            <v-list-item-content>
              <v-list-item-title class="text-subtitle-1"
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
    <v-col col="12" v-if="rules.length > 0">
      <div
        v-for="(rule, index) in rules"
        :key="`rule-${index}`"
        class="rule-section"
      >
        <span class="section-title mb-2"
          >Match
          <huxSwitch v-model="rule.operand"></huxSwitch>
          of the following
        </span>
        <div
          class="col-12 row pt-0 pb-2"
          v-for="(condition, ixcondition) in rule.conditions"
          :key="`${index}-ruleCondition-${ixcondition}`"
        >
          <div class="condition-card col-10 d-flex">
            <div class="options">
              <DropdownMenu
                v-model="condition.attribute"
                :labelText="fetchDropdownLabel(condition, 'attribute')"
                :menuItem="attributeOptions"
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
            <div class="actions">
              <v-btn icon color="primary" @click="addNewCondition(rule.id)">
                <v-icon>mdi-plus-circle</v-icon>
              </v-btn>
              <v-btn
                icon
                color="primary"
                @click="removeCondition(rule, ixcondition)"
                :disabled="rule.conditions.length === 1"
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
          <v-col col="12" class="row">
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
  name: "AttributeRule",
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
      parent.conditions.splice(child, 1)
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
  .rule-section {
    .section-title {
      display: flex;
      align-items: center;
      .v-input {
        margin-left: 15px;
      }
    }
    .condition-card {
      background: #ffffff;
      /* Background (Light) */

      border: 1px solid #f9fafb;
      box-sizing: border-box;
      box-shadow: 0px 3px 8px #d0d0ce;
      border-left: solid 10px #ecf4f9;
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
          min-width: 200px;
          button {
            width: 100%;
            justify-content: left;
            .v-btn__content {
              justify-content: space-between;
            }
          }
        }
        .v-text-field {
          .v-input__slot {
            min-height: inherit;
          }
          .v-text-field__details {
            display: none;
          }
        }
      }
    }
    .condition-summary {
      background: white;
    }
  }
  .add-section-wrap {
    .add-section {
      background: #f9fafb;
      border: 1px solid #e2eaec;
      box-sizing: border-box;
      border-radius: 5px;
    }
  }
  .condition-summary {
    margin-left: 15px;
    border: solid 1px #d0d0ce;
    border-radius: 10px;
    background: #f9fafb;
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
      border-color: #e2eaec;
    }
    .v-chip {
      position: absolute;
      top: 0;
      transform: translateX(-50px);
      left: 50%;
      background: #e2eaec !important;
    }
  }
}
</style>
