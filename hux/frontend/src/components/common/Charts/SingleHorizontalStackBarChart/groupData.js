// group data for chart and filter out zero values
import * as d3Scale from "d3-scale"

export default function (data, total) {
  // use scale to get percent values
  const percent = d3Scale.scaleLinear().domain([0, total]).range([0, 100])
  // filter out data that has zero values
  // also get mapping for next placement
  // (save having to format data for d3 stack)
  let cumulative = 0
  const _data = data
    .map((d) => {
      cumulative += d.value
      return {
        value: d.value,
        // want the cumulative to prior value (start of rect)
        cumulative: cumulative - d.value,
        label: d.label,
        percent: percent(d.value),
      }
    })
    .filter((d) => d.value > 0)
  return _data
}
