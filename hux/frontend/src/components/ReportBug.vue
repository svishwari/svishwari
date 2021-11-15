<template>
  <div>
    <div
      class="
        black--text
        text--darken-4 text-subtitle-1
        font-weight-regular
        px-13
        mt-5
        pb-5
      "
    >
      Give us some details about the problem you are having.
    </div>
    <div>
      <text-field
        label-text="Subject"
        placeholder="Enter Subject"
        class="px-13"
        height="40"
        required
        @change="setBugSubject($event)"
      />
      <text-field
        label-text="Bug Summary"
        placeholder="Enter short descritption of event"
        class="px-13 bug-summary"
        height="206"
        required
        @change="setBugSummary($event)"
      />
    </div>
  </div>
</template>

<script>
import TextField from "@/components/common/TextField"

export default {
  name: "ReportBug",
  components: {
    TextField,
  },

  data() {
    return {
      inputText: null,
      bugObject: {
        issue_type: "Bug",
        summary: "",
        description: "",
      },
    }
  },

  methods: {
    setBugSubject(inputText) {
      this.bugObject.summary = inputText
      this.$emit("setBugDetails", this.bugObject)
    },
    setBugSummary(inputText) {
      this.bugObject.description = inputText
      this.$emit("setBugDetails", this.bugObject)
    },
  },
}
</script>
<style lang="scss" scoped>
.bug-summary {
  ::v-deep .v-text-field {
    .v-text-field__slot {
      input {
        margin-top: -162px !important;
      }
    }
  }
}
</style>
