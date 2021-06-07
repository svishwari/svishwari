<template>
  <div class="hux-v-slider">
    <v-slider
      v-model="currentValue"
      :color="currentColor"
      :readonly="readOnly"
      :track-color="currentColor"
      :min="minRange"
      :max="maxRange"
      always-dirty
    >
      <template v-slot:append>
        <span
          class="slider-value-display"
          :style="{
            color: currentColor,
          }"
          v-text="currentValue + '%'"
        ></span>
      </template>
    </v-slider>
  </div>
</template>

<script>
export default {
  name: "hux-slider",
  props: {
    inputValue: {
      type: Number,
      required: true,
      default: 30,
    },
    minRange: {
      type: Number,
      required: false,
      default: 0,
    },
    maxRange: {
      type: Number,
      required: false,
      default: 100,
    },
    readOnly: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      currentValue: this.inputValue,
      colorCombination: [
        "#ec5b54",
        "#f76d48",
        "#fe823b",
        "#ff972d",
        "#ffae1d",
        "#f6b810",
        "#ecc103",
        "#e0ca00",
        "#c9c703",
        "#b3c40f",
        "#9cc01a",
        "#86bc25",
      ],
    }
  },

  computed: {
    currentColor() {
      if (this.currentValue < 8) return this.colorCombination[0]
      if (this.currentValue < 16) return this.colorCombination[1]
      if (this.currentValue < 24) return this.colorCombination[2]
      if (this.currentValue < 32) return this.colorCombination[3]
      if (this.currentValue < 40) return this.colorCombination[4]
      if (this.currentValue < 48) return this.colorCombination[5]
      if (this.currentValue < 56) return this.colorCombination[6]
      if (this.currentValue < 64) return this.colorCombination[7]
      if (this.currentValue < 72) return this.colorCombination[8]
      if (this.currentValue < 80) return this.colorCombination[9]
      if (this.currentValue < 88) return this.colorCombination[10]
      if (this.currentValue < 96) return this.colorCombination[11]
      return this.colorCombination[11]
    },
  },

  methods: {},
}
</script>

<style lang="scss" scoped>
.hux-v-slider {
  margin-left: 10px;
  margin-right: 10px;

  .slider-value-display {
    width: 28px;
    height: 16px;
    margin-top: 4px;
  }

  ::v-deep .v-slider__thumb {
    height: 16px;
    width: 16px;
    box-shadow: 0px 1px 5px rgb(0 0 0 / 25%);
    -webkit-appearance: none;
    appearance: none;

    &:before {
      left: -10px;
      top: -10px;
    }
  }

  ::v-deep .v-slider--horizontal {
    margin-left: 0px;

    .v-slider__track-container {
      width: 101%;
      height: 6px;
      left: -6px;
      transform: translateY(-50%);
      background: linear-gradient(0.25turn, #ec5b54, #ffcd00, #86bc25);
      border-radius: 5px;
    }

    .v-slider__track-background {
      border-radius: 5px;
      background: transparent !important;
    }

    .v-slider__track-fill {
      border-radius: 5px;
      background: transparent !important;
    }
  }
}
</style>
