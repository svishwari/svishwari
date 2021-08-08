<template>
  <div class="list-container">
    <div class="content-style pl-6 pr-4 pb-4">
      <div v-for="item in mapChartData" :key="item.name" class="sub-props pt-4">
        <span class="subprop-name">{{ item.name }}</span>
        <span class="value ml-2 font-weight-semi-bold">
          {{ item.population_percentage | Percentage }}
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
  },
  data() {
    return {
      mapChartData: this.mapData,
    }
  },
  mounted() {
    this.sortStateData()
  },
  methods: {
    sortStateData() {
      if (this.mapChartData) {
        this.mapChartData.sort(
          (a, b) => b.population_percentage - a.population_percentage
        )
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
        flex: 1 0 40%;
        text-align: right;
        margin-right: 30px;
      }
      .value {
        @extend .global-text-line;
        color: var(--v-neroBlack-base);
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
    background: var(--v-lightGrey-base);
    border-radius: 5px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: var(--v-lightGrey-base);
  }
}
</style>
