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
              :disabled="!Boolean(count)"
              @click="$emit('clear')"
            >
              Clear
            </v-btn>
          </slot>
        </div>

        <div class="content">
          <slot name="default">
            <!-- `FilterPanels` live here -->
          </slot>
        </div>

        <div class="footer mt-auto">
          <slot name="footer">
            <v-btn
              tile
              color="primary"
              class="text-button ml-auto"
              width="134"
              @click="$emit('apply')"
            >
              Apply filter
            </v-btn>
          </slot>
        </div>
      </div>
    </v-card>
  </v-expand-x-transition>
</template>

<script>
import { defineComponent } from "@vue/composition-api"

export default defineComponent({
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
  },
})
</script>

<style lang="scss" scoped>
$footerHeight: 80px;
$headerHeight: 40px;
$offset: 180px;
$padding: 20px;
$width: 300px;

.hux-filters-drawer {
  border-left: 1px solid var(--v-black-lighten3) !important;
  width: $width;
  height: 100%;

  .wrapper {
    display: flex;
    flex-direction: column;
    position: fixed;
    width: $width;
    min-height: calc(100vh - #{$offset});
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
  }

  .footer {
    height: $footerHeight;
    border-top: 1px solid var(--v-black-lighten3);
  }
}
</style>
