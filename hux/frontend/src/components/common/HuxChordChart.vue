<template>
  <v-card max-width="424" tile class="rounded-lg">
    <v-list-item three-line>
      <v-list-item-content>
        <div class="mb-4">
          <Tooltip positionTop>
            <template #label-content>
              Individual Identity
              <Icon type="info" :size="12" />
            </template>
            <template class="newp" #hover-content>
              {{ tooltipText }}
            </template>
          </Tooltip>
        </div>
        <v-list-item-subtitle
          class="legend-section"
          v-for="item in legendsData"
          :key="item.id"
          ><Icon :type="item.icon" :size="12" /><span>{{
            item.prop
          }}</span></v-list-item-subtitle
        >
      </v-list-item-content>

      <div class="chart-section" ref="huxChart"></div>
    </v-list-item>
  </v-card>
</template>

<script>
import * as d3 from "d3"
import Tooltip from "@/components/common/Tooltip"
import Icon from "@/components/common/Icon"
export default {
  name: "hux-chord-chart",
  components: { Icon, Tooltip },
  props: {
    chartInput: {
      type: Array,
      required: true,
    },
    colorCodes: {
      type: Array,
      required: false,
    },
  },
  data() {
    return {
      width: 250,
      height: 250,
      outerRadius: 0,
      innerRadius: 0,
      tooltipText: "most recent co-occurence between identifiers",
      legendsData: [
        { prop: "Name", icon: "name" },
        { prop: "Address", icon: "address" },
        { prop: "Email", icon: "email" },
        { prop: "Phone", icon: "phone" },
        { prop: "Cookie", icon: "cookie" },
      ],
    }
  },
  methods: {
    initializeValues() {
      this.outerRadius = Math.min(this.width, this.height) * 0.5 - 35
      this.innerRadius = this.outerRadius - 7
    },

    calculateChartValues() {
      let svg = d3
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)
        .attr("outerRadius", this.outerRadius)
        .attr("innerRadius", this.innerRadius)

      let chord = d3.chord().padAngle(0.05).sortSubgroups(d3.descending)

      let arc = d3
        .arc()
        .innerRadius(this.innerRadius)
        .outerRadius(this.outerRadius)

      let ribbon = d3.ribbon().radius(this.innerRadius)

      let color = d3.scaleOrdinal().domain(d3.range(5)).range(this.colorCodes)

      let g = svg
        .append("g")
        .attr(
          "transform",
          "translate(" + this.width / 2 + "," + this.height / 2 + ")"
        )
        .datum(chord(this.chartInput))

      let group = g
        .append("g")
        .attr("class", "groups")
        .selectAll("g")
        .data((chords) => chords.groups)
        .enter()
        .append("g")

      group
        .append("path")
        .style("fill", (d) => color(d.index))
        .attr("d", arc)

      g.append("g")
        .attr("class", "ribbons")
        .selectAll("path")
        .data((chords) => chords)
        .enter()
        .append("path")
        .attr("d", ribbon)
        .attr("fill-opacity", "0.5")
        .style("fill", () => "#d3d3d3")
    },
  },
  mounted() {
    this.initializeValues()
    this.calculateChartValues()
  },
}
</script>

<style lang="scss" scoped>
.legend-section {
  span {
    margin-left: 8px;
    font-size: 12px;
    line-height: 16px;
    color: rgba(79, 79, 79, 1);
  }
}

.ribbons {
  fill-opacity: 0.67;
}

.mb-4 {
  font-size: 15px;
  line-height: 20px;
  font-weight: 400;
}

.chart-section {
  margin-bottom: -20px;
}
</style>
