<template>
  <v-card
    tile
    elevation="19"
    v-if="showTooltip"
    :style="{ transform: `translate(${position.x}px, ${position.y}px)` }"
    class="mx-auto card-style"
  >
    <div class="arc-hover" v-if="isArcHover">
      <Icon :type="sourceInput.icon" :size="12" />
      <span class="prop-name">{{ sourceInput.name }}</span>
      <div
        class="sub-props"
        v-for="item in sourceInput.assetsData"
        :key="item.name"
      >
        <Icon :type="item.icon" :size="12" />
        <span class="subprop-name">{{ item.description }}</span>
        <span class="value">{{ item.value }}</span>
      </div>
    </div>
    <div class="ribbon-hover" v-if="!isArcHover">
      <Icon :type="sourceInput.icon1" :size="12" />
      <span class="prop-name">{{ sourceInput.name1 }}</span>
      <span class="pipe"></span>
      <Icon :type="sourceInput.icon2" :size="12" />
      <span class="prop-name">{{ sourceInput.name2 }}</span>
      <span class="text-line"
        >{{ sourceInput.currentOccurance }} Co-occurances</span
      >
      <span class="text-line-italic"
        >out of {{ sourceInput.totalOccurance }} total co-occurances</span
      >
    </div>
  </v-card>
</template>

<script>
import Icon from "@/components/common/Icon"
export default {
  name: "ChartTooltip",
  components: { Icon },
  props: {
    position: {
      type: Object,
      required: false,
      default() {
        return {
          x: 0,
          y: 0,
        }
      },
    },
    isArcHover: {
      type: Boolean,
      required: false,
    },
    showTooltip: {
      type: Boolean,
      required: false,
      default: false,
    },
    animate: {
      type: Boolean,
      required: false,
      default: true,
    },
    sourceInput: {
      type: Object,
      required: false,
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-card {
  border-radius: 0px !important;
}
.global-heading {
  font-style: normal;
  font-weight: 600;
  font-size: 14px;
  line-height: 19px;
  padding-left: 10px;
}

.global-text-line {
  display: inline-block;
  font-weight: normal;
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
}

.card-padding {
  padding: 10px 20px 20px 20px;
}

.card-style {
  max-width: 213px;
  height: auto;
  top: -239px;
  left: -310px;
  z-index: 1;
  border-radius: 0px !important;

  .ribbon-hover {
    @extend .card-padding;

    .pipe {
      border-left: 1px solid var(--v-lightGrey-base) !important;
      height: 500px;
      transform: rotate(90deg);
      margin-left: 10px;
      margin-right: 10px;
    }

    .prop-name {
      @extend .global-heading;
    }
    .text-line {
      @extend .global-text-line;
      margin-top: 10px;
    }
    .text-line-italic {
      @extend .global-text-line;
      font-style: italic;
      font-weight: normal;
    }
  }

  .arc-hover {
    @extend .card-padding;
    .prop-name {
      @extend .global-heading;
    }
    .sub-props {
      padding-top: 16px;

      .subprop-name {
        @extend .global-text-line;
        padding-left: 5px;
        font-size: 12px;
        line-height: 16px;
      }

      .value {
        @extend .global-text-line;
        font-size: 12px;
        line-height: 16px;
        float: right;
      }
    }
  }
}
</style>
