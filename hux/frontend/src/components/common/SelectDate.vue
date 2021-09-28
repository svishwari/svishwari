<template>
  <div class="d-flex">
    <hux-select
      v-model="month"
      :items="monthOptions"
      :items-disabled="[]"
      label="Select month"
      class="mx-1"
      width="141"
      @change="onChange"
    />

    <hux-select
      v-model="year"
      :items="yearOptions"
      :items-disabled="[]"
      label="Select year"
      class="mx-1"
      width="126"
      @change="onChange"
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
            config = {
              startMonth: filters.Date(props.min, "MMMM"),
            }
          }

          if (year.value === maxYear) {
            config = {
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
     * Change value to the selected month/year
     */
    function onChange() {
      localValue.value = filters.Date(
        `${month.value} ${year.value}`,
        "YYYY-MM-DD"
      )
    }

    /**
     * Watch value to update the selected month/year
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
