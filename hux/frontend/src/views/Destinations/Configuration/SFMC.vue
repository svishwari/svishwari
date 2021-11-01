<template>
  <v-row>
    <v-col cols="6" class="sfmc-data-extension">
      <div class="text-caption black--text text--darken-4 pb-2">
        Performance metric data extension name
      </div>
      <v-select
        :items="dataExtensionNames"
        placeholder="Select"
        dense
        outlined
        background-color="white"
        append-icon="mdi-chevron-down"
        @input="(value) => onDataExtensionSelection('performance', value)"
      />
    </v-col>
    <v-col cols="6" class="sfmc-data-extension">
      <div class="text-caption black--text text--darken-4 pb-2">
        Campaign activity data extension name
      </div>
      <v-select
        :items="dataExtensionNames"
        placeholder="Select"
        dense
        outlined
        background-color="white"
        append-icon="mdi-chevron-down"
        @input="(value) => onDataExtensionSelection('campaign', value)"
      />
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "SFMC",

  props: {
    dataExtensions: {
      type: Array,
      required: true,
    },
  },

  data() {
    return {
      isFullyConfigured: false,
      selectedDataExtension: {},
    }
  },

  computed: {
    dataExtensionNames() {
      return this.dataExtensions.map((each) => {
        return {
          text: each.name,
          value: {
            data_extension_id: each.data_extension_id,
            name: each.name,
          },
        }
      })
    },
  },

  methods: {
    onDataExtensionSelection(type, value) {
      if (type === "performance") {
        this.selectedDataExtension.performance_metrics_data_extension = value
      }
      if (type === "campaign") {
        this.selectedDataExtension.campaign_activity_data_extension = value
      }
      if (
        this.selectedDataExtension.performance_metrics_data_extension &&
        this.selectedDataExtension.campaign_activity_data_extension
      ) {
        this.$emit("select", this.selectedDataExtension)
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.sfmc-data-extension {
  ::v-deep .v-input {
    .v-input__control {
      .v-input__slot {
        min-height: 40px;
        fieldset {
          color: var(--v-black-lighten3) !important;
          border-width: 1px !important;
        }
      }
      .v-text-field__details {
        display: none;
      }
    }
  }
}
</style>
