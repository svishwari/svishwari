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
        @input="onDataExtensionSelection"
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
      selectedDataExtension: null,
    }
  },

  computed: {
    dataExtensionNames() {
      return this.dataExtensions.map((each) => {
        return {
          text: each.name,
          value: each.data_extension_id,
        }
      })
    },
  },

  methods: {
    onDataExtensionSelection(value) {
      this.selectedDataExtension = this.dataExtensions.filter(
        (each) => each.data_extension_id === value
      )[0]
      this.$emit("select", this.selectedDataExtension)
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
