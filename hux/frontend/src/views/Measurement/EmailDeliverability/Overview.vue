<template>
  <div class="d-flex flex-row-reverse">
    <metric-card
      title="Overall inbox rate"
      :height="75"
      max-width="160"
      :interactable="false"
    >
      <template #subtitle-extended>
        <tooltip>
          <template #label-content>
            <span class="text-subtitle-1">
              {{ entity.overAllRate | Percentage | Empty }}
            </span>
          </template>
          <template #hover-content>
            {{ entity.overAllRate | Percentage | Empty }}
          </template>
        </tooltip>
      </template>
    </metric-card>
    <metric-card
      class="mr-3"
      title="Description"
      :height="75"
      :interactable="false"
    >
      <template #subtitle-extended>
        <tooltip>
          <template #label-content>
            <span class="text-body-1">
              {{ entity.description }}
            </span>
          </template>
          <template #hover-content>
            {{ entity.description }}
          </template>
        </tooltip>
      </template>
    </metric-card>
  </div>
</template>

<script>
import MetricCard from "@/components/common/MetricCard.vue"
import Tooltip from "@/components/common/Tooltip.vue"
export default {
  name: "Overview",
  components: { MetricCard, Tooltip },
  props: {
    entity: {
      type: Object,
      required: true,
      default: () => {},
    },
  },
}
</script>

<style></style>
