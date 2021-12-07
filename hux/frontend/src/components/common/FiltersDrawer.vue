<template>
  <v-expand-x-transition>
    <v-card
      v-show="isToggled"
      flat
      tile
      color="white"
      class="hux-filters-drawer"
    >
      <div class="wrapper">
        <div class="header">
          <slot name="header">
            <h2 class="text-h2">
              Filter
              <span v-if="count">({{ count }})</span>
            </h2>

            <v-btn
              text
              min-width="50"
              height="24"
              class="primary--text"
              :disabled="!Boolean(count) || disableClear"
              @click="$emit('clear')"
            >
              Clear
            </v-btn>
          </slot>
        </div>

        <div class="content" :style="top">
          <slot name="default">
            <!-- `FilterPanels` live here -->
          </slot>
        </div>

        <div class="footer mt-auto white">
          <slot name="footer">
            <hux-button
              size="large"
              variant="white"
              is-tile
              class="
                text-button
                ml-auto
                primary--text
                mr-3
                btn-border
                box-shadow-none
              "
              width="91"
              @click="$emit('close')"
            >
              Close
            </hux-button>
            <hux-button
              is-tile
              color="primary"
              class="text-button ml-auto"
              width="157"
              @click="$emit('apply')"
            >
              Apply filter
            </hux-button>
          </slot>
        </div>
      </div>
    </v-card>
  </v-expand-x-transition>
</template>

<script>
import { defineComponent } from "@vue/composition-api"
import huxButton from "@/components/common/huxButton"

export default defineComponent({
  components: {
    huxButton,
  },

  props: {
    isToggled: {
      type: Boolean,
      required: true,
      default: false,
    },

    count: {
      type: Number,
      required: false,
      default: 0,
    },

    disableClear: {
      type: Boolean,
      required: false,
      default: false,
    },
    topcontent: {
      type: String,
      required: false,
      default: "182px",
    },
  },

  computed: {
    top() {
      return "top: " + this.topcontent
    },
  },
})
</script>

<style lang="scss" scoped>
$footerHeight: 80px;
$headerHeight: 40px;
$padding: 20px;
$width: 300px;
.hux-filters-drawer {
  border-left: 1px solid var(--v-black-lighten3) !important;
  width: $width;
  height: 100%;
  z-index: 8;
  position: absolute;
  right: 0;
  .wrapper {
    display: flex;
    flex-direction: column;
    position: fixed;
    width: $width;
  }

  .header,
  .content,
  .footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 $padding;
  }

  .header {
    height: $headerHeight;
    border-bottom: 1px solid var(--v-black-lighten3);
  }

  .content {
    flex-direction: column;
    padding: 0;
    overflow-y: auto;
    max-height: 100%;
    height: 100%;
    position: fixed;
  }

  .footer {
    height: $footerHeight;
    border-top: 1px solid var(--v-black-lighten3) !important;
    position: fixed;
    bottom: 0;
  }
}
</style>
