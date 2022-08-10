<template>
  <v-radio-group v-model="selectedRadio" :disabled="isDisabled">
    <v-radio
      v-for="(label, index) in labels"
      :key="index"
      :label="label"
      :value="label"
    ></v-radio>
  </v-radio-group>
</template>

<script>
export default {
  name: "RadioButton",
  components: {},
  props: {
    isDisabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    labels: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      selectedRadio: this.labels[0],
    }
  },
  computed: {},
  methods: {},
}
</script>
<style lang="scss" scoped></style>
