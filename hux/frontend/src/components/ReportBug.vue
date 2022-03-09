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
        placeholder="Enter subject"
        class="px-13"
        height="40"
        required
        @change="setBugSubject($event)"
      />
      <v-textarea
        solo
        label-text="Bug summary"
        placeholder="Enter a short description"
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
  ::v-deep .v-input__control {
    .v-input__slot {
      border: 1px solid var(--v-black-lighten3) !important;
      @extend .no-shadow;
      .v-text-field__slot {
        textarea {
          resize: none;
        }
      }
    }
  }
}
</style>
