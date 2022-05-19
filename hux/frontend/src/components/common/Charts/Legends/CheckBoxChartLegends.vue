<template>
  <div>
    <span
      v-for="item in legendsData"
      :key="item.text"
      class="chart-legends mr-6"
    >
      <span class="legend-items" :class="!showCheckBox ? 'mt-5' : ''">
        <v-checkbox
          v-if="showCheckBox"
          :key="item.text"
          v-model="item.checked"
          :disabled="item.disabled"
          :color="item.color"
          class="text--base-1"
          @change="handleCheckboxValueChange()"
        ></v-checkbox>
        <span class="dots" :style="{ backgroundColor: item.color }"> </span>
        <span class="text text-body-1">{{ item.text }}</span>
      </span>
    </span>
  </div>
</template>

<script>
export default {
  name: "CheckboxChartLegends",
  props: {
    /**
     * Accepts an array of object consist of Label circle color & text
     * eg:  [{ color: "rgba(208, 208, 206, 1)", text: "no data available" }]
     */
    legendsData: {
      type: Array,
      required: true,
    },
  },
  computed: {
    // hide checkbox in case of single data
    showCheckBox() {
      return this.legendsData.length > 1
    },
  },
  methods: {
    // checkbox change event trigger
    handleCheckboxValueChange() {
      this.$emit("onCheckboxChange", this.legendsData)
      this.handleSingleEnableCheckbox()
    },
    // handle single checkbox disabling
    handleSingleEnableCheckbox() {
      let checkedItem = this.legendsData.filter((data) => data.checked)
      if (checkedItem.length == 1) {
        checkedItem[0].disabled = true
      } else {
        checkedItem.forEach((data) => (data.disabled = false))
      }
    },
  },
}
</script>
<style lang="scss" scoped>
.chart-legends {
  display: inline-block;
  .legend-items {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    .dots {
      margin-right: 4px;
      margin-left: -6px;
      height: 12px;
      width: 12px;
      border-radius: 50%;
      display: inline-block;
    }
    .text {
      color: var(--v-black-darken1);
      display: inline-block;
    }
  }
}
</style>
