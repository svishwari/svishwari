<template>
  <v-card
    v-if="showToolTip"
    tile
    :style="{
      transform: `translate(${sourceInput.xPosition}px, ${sourceInput.yPosition}px)`,
    }"
    class="mx-auto tooltip-style"
  >
    <div class="neroBlack--text caption">
      <div class="value-section">
        <div>{{ sourceInput.day }}</div>
        <div>
          {{ sourceInput.month }} {{ sourceInput.date | Date("DD, YYYY") }}
        </div>
      </div>
      <div class="item_count">{{ sourceInput.total_event_count }} Events</div>
      <div
        v-for="event in eventsLabels"
        :key="event.event_name"
        class="value-container"
      >
        <div v-if="sourceInput.eventsCollection.includes(event.event_name)">
          <icon :type="event.event_name" :size="10" />
          <span class="text-label">{{ event.label_name }}</span>
        </div>
      </div>
      <!-- <div class="value-section">
        {{ sourceInput.totalCustomers | Numeric(true, false, false) }}
      </div>
      <div class="value-container">
        <icon type="name" :size="12" :color="colorCodes[sourceInput.index]" />
        <span class="text-label">New customers added</span>
        <div class="value-section">
          {{ sourceInput.addedCustomers | Numeric(true, false, false) }}
        </div>
      </div> -->
    </div>
  </v-card>
</template>

<script>
import Icon from "@/components/common/Icon"

export default {
  name: "LineChartTooltip",
  components: { Icon },
  props: {
    showToolTip: {
      type: Boolean,
      required: false,
      default: false,
    },
    sourceInput: {
      type: Object,
      required: false,
    },
  },
  data() {
    return {
      eventsLabels: [
        {
          label_name: "Abandoned cart",
          event_name: "abandoned_cart",
        },
        {
          label_name: "Customer login",
          event_name: "customer_login",
        },
        {
          label_name: "Trait computed",
          event_name: "trait_computed",
        },
        {
          label_name: "Viewed cart",
          event_name: "viewed_cart",
        },
        {
          label_name: "Viewed checkout",
          event_name: "viewed_checkout",
        },
        {
          label_name: "Viewed sale item",
          event_name: "viewed_sale_item",
        },
        // {
        //   label_name: "Item purchased",
        //   event_name: "item_purchased",
        // },
      ],
    }
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-card {
  border-radius: 0px !important;
}

.global-heading {
  font-style: normal;
  font-size: 12px;
  line-height: 19px;
}

.tooltip-style {
  @extend .box-shadow-3;
  border-radius: 0px;
  padding: 8px 8px 15px 8px;
  max-width: 172px;
  height: auto;
  z-index: 1;
  border-radius: 0px !important;
  position: absolute;
  top: -130px;
  left: 56px;
  .value-container {
    margin-top: 2px;
    @extend .global-heading;
    .text-label {
      margin-left: 8px !important;
    }
  }

  .value-section {
    @extend .global-heading;
    // margin-left: 21px;
  }

  .item_count {
    font-weight: bold;
  }
}
</style>
