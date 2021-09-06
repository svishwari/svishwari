<template>
  <v-card
    v-if="showTooltip"
    tile
    :style="{
      transform: `translate(${position.x}px, ${position.y}px)`,
      'border-radius': '0px !important',
    }"
    class="mx-auto card-style"
  >
    <div v-if="isArcHover" class="arc-hover">
      <icon v-if="sourceInput.icon" :type="sourceInput.icon" :size="12" />
      <span class="prop-name">{{ sourceInput.name }}</span>
      <div
        v-for="item in sourceInput.assetsData"
        :key="item.name"
        class="sub-props pt-4"
      >
        <logo v-if="item.icon" :type="item.icon" :size="14" />
        <span class="subprop-name">{{ item.description }}</span>
        <span class="value ml-1">{{ item.value }}</span>
      </div>
    </div>
    <div v-if="!isArcHover" class="ribbon-hover">
      <icon
        v-if="sourceInput.sourceIcon"
        :type="sourceInput.sourceIcon"
        :size="12"
        color="primary"
      />
      <span class="prop-name">{{ sourceInput.sourceName }}</span>
      <span class="pipe"></span>
      <icon
        v-if="sourceInput.targetIcon"
        :type="sourceInput.targetIcon"
        :size="12"
        color="primary"
      />
      <span class="prop-name">{{ sourceInput.targetName }}</span>
      <span class="text-line">
        {{ sourceInput.currentOccurence }} Co-occurrences
      </span>
      <span class="text-line-italic">
        out of {{ sourceInput.totalOccurence }} total co-occurrences
      </span>
    </div>
  </v-card>
</template>

<script>
import Icon from "@/components/common/Icon"
import Logo from "@/components/common/Logo"
export default {
  name: "ChartTooltip",
  components: { Icon, Logo },
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
  @extend .font-weight-semi-bold;
  font-style: normal;
  font-size: $font-size-root;
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
  @extend .box-shadow-3;
  border-radius: 0px;
  max-width: 213px;
  height: auto;
  top: -220px;
  left: -55px;
  z-index: 1;

  .ribbon-hover {
    @extend .card-padding;
    .pipe {
      border-left: 1px solid var(--v-black-lighten3) !important;
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
    }
  }

  .arc-hover {
    @extend .card-padding;
    .prop-name {
      @extend .global-heading;
    }
    .sub-props {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      height: 30px;
      .subprop-name {
        @extend .global-text-line;
        flex: 1 0 50%;
        padding-left: 5px;
      }
      .value {
        @extend .global-text-line;
      }
    }
  }
}
</style>
