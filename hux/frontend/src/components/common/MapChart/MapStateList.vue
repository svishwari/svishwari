<template>
  <div class="list-container">
    <div class="content-style pl-6 pr-4 pb-4">
      <div
        v-for="item in mapChartData"
        :key="item[defaultMetric]"
        class="sub-props pt-4"
      >
        <span class="subprop-name">{{ item[defaultMetric] }}</span>
        <span class="value ml-2 font-weight-semi-bold">
          {{ applyFilter(item[primaryMetric.key], primaryMetric.format) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MapStateList",
  props: {
    mapData: {
      type: Array,
      required: true,
    },
    configurationData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      mapChartData: [],
    }
  },
  computed: {
    primaryMetric() {
      return this.configurationData.primary_metric
    },
    defaultMetric() {
      return this.configurationData.default_metric.key
    },
  },
  mounted() {
    this.sortStateData()
  },
  methods: {
    sortStateData() {
      this.mapChartData = JSON.parse(JSON.stringify(this.mapData))
      if (this.mapChartData) {
        this.mapChartData.sort(
          (a, b) => b[this.primaryMetric.key] - a[this.primaryMetric.key]
        )
      }
    },
    applyFilter(value, filter) {
      switch (filter) {
        case "numeric":
          return this.$options.filters.Numeric(value, true, false, false)
        case "percentage":
          return this.$options.filters.Numeric(value, true, false, false, true)
        case "currency":
          return this.$options.filters.Currency(value)
        default:
          return this.$options.filters.Empty
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.global-text-line {
  display: inline-block;
  font-style: normal;
  font-size: $font-size-root;
  line-height: 19px;
}
.list-container {
  max-height: 550px;
  min-height: 20px;
  .content-style {
    padding-top: 0px !important;
    min-height: 100px;
    max-height: 318px;
    overflow-y: scroll;
    .sub-props {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      .subprop-name {
        @extend .global-text-line;
        flex: 1 0 30%;
        text-align: right;
        margin-right: 30px;
      }
      .value {
        @extend .global-text-line;
        color: var(--v-black-darken4);
        flex: 1;
        text-align: left;
      }
    }
  }
  ::-webkit-scrollbar {
    width: 5px;
  }
  ::-webkit-scrollbar-track {
    box-shadow: inset 0 0 5px var(--v-white-base);
    border-radius: 10px;
  }
  ::-webkit-scrollbar-thumb {
    background: var(--v-black-lighten3);
    border-radius: 5px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: var(--v-black-lighten3);
  }
}
</style>
