<template>
  <div class="d-flex">
    <hux-select
      v-model="month"
      :items="monthOptions"
      label="Select a month"
      class="mx-1"
      width="141"
      @change="onChange('month', month)"
    />

    <hux-select
      v-model="year"
      :items="yearOptions"
      label="Select a year"
      class="mx-1"
      width="126"
      @change="onChange('year', year)"
    />
  </div>
</template>

<script>
import { defineComponent, computed, ref, watch } from "@vue/composition-api"
import { listOfMonths, listOfYears } from "@/utils"
import filters from "@/filters"
import HuxSelect from "@/components/common/Select.vue"

export default defineComponent({
  components: {
    HuxSelect,
  },

  props: {
    value: {
      type: [String],
      required: false,
      default: null,
    },

    min: {
      type: [String],
      required: false,
    },

    max: {
      type: [String],
      required: false,
    },
  },

  emits: ["input", "change"],

  setup(props, { emit }) {
    const localValue = computed({
      get: () => props.value,
      set: (value) => {
        emit("input", value)
        emit("change", value)
      },
    })

    const localMin = computed({
      get: () => props.min,
    })

    const localMax = computed({
      get: () => props.max,
    })

    const month = ref(null)

    const year = ref(null)

    const monthOptions = computed({
      get: () => {
        let config

        if (props.min && props.max) {
          const minYear = filters.Date(props.min, "YYYY")
          const maxYear = filters.Date(props.max, "YYYY")

          if (year.value === minYear) {
            let endMonth

            if (maxYear === minYear) {
              endMonth = filters.Date(props.max, "MMMM")
            }

            config = {
              startMonth: filters.Date(props.min, "MMMM"),
              endMonth: endMonth,
            }
          }

          if (year.value === maxYear) {
            let startMonth

            if (minYear === maxYear) {
              startMonth = filters.Date(props.min, "MMMM")
            }

            config = {
              startMonth: startMonth,
              endMonth: filters.Date(props.max, "MMMM"),
            }
          }
        }

        return listOfMonths(config)
      },
    })

    const yearOptions = computed({
      get: () => {
        let config

        if (props.min && props.max) {
          config = {
            startYear: filters.Date(props.min, "YYYY"),
            endYear: filters.Date(props.max, "YYYY"),
          }
        }

        return listOfYears(config)
      },
    })

    /**
     *
     * Change value to the selected month/year.
     *
     * @param {string} input the input changed ex. month or year
     */
    function onChange(input) {
      // when selecting a year and the selected month is not available,
      // fall back to selecting the first month available
      if (input === "year" && !monthOptions.value.includes(month.value)) {
        month.value = monthOptions.value[0]
      }
      localValue.value = filters.Date(
        `${month.value} ${year.value}`,
        "YYYY-MM-DD"
      )
    }

    /**
     * Watch value to update the selected month/year.
     */
    watch(localValue, (value) => {
      if (value) {
        month.value = filters.Date(value, "MMMM")
        year.value = filters.Date(value, "YYYY")
      }
    })

    return {
      localValue,
      localMin,
      localMax,
      month,
      year,
      monthOptions,
      yearOptions,
      onChange,
    }
  },
})
</script>

<style lang="scss" scoped></style>
