<template>
  <v-card
    class="descriptive-card align-center text-center rounded-lg mr-10 mb-10"
    :style="{ 'min-height': minHeight }"
    :class="{ 'in-active': disabled }"
  >
    <div v-if="$slots.top" class="pa-3 pb-0">
      <slot name="top" />
    </div>

    <div v-if="icon" class="d-flex justify-center pb-4">
      <div class="dot">
        <icon :type="icon" :size="44" color="primary" class="d-block" />
      </div>
    </div>

    <tooltip nudge-right="100px" min-width="auto !important">
      <template #label-content>
        <div
          class="text-h4 px-3 pb-2 text-ellipsis d-block title"
          :class="disabled ? 'black--text text--darken-4' : 'primary--text'"
          data-e2e="card-title"
        >
          {{ title }}
        </div>
      </template>
      <template #hover-content>
        <span class="black--text text--darken-4">{{ title }}</span>
      </template>
    </tooltip>

    <tooltip nudge-right="100px" min-width="auto !important">
      <template #label-content>
        <div
          class="text-caption px-3 d-block description"
          data-e2e="card-description"
        >
          {{ description }}
        </div>
      </template>
      <template #hover-content>
        <span class="black--text text--darken-4">{{ description }}</span>
      </template>
    </tooltip>

    <div v-if="$slots.default" class="px-3 pt-2">
      <slot />
    </div>
  </v-card>
</template>

<script>
import Icon from "@/components/common/Icon"
import Tooltip from "@/components/common/Tooltip"

export default {
  name: "DescriptiveCard",

  components: {
    Icon,
    Tooltip,
  },

  props: {
    icon: {
      type: String,
      required: false,
    },

    title: {
      type: String,
      required: false,
      default: "Model Name",
    },

    description: {
      type: String,
      required: false,
      default: "Descriptive text for the model item chosen above",
    },
    type: {
      type: String,
      required: true,
      default: "Models", 
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  computed: {
    minHeight() {
      if(this.type == 'Models'){
        return '255px';
      }else if(this.type == 'Modules'){
        return '225px';
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.descriptive-card {
  @extend .box-shadow-5;
  color: var(--v-black-darken4);
  font-weight: normal;
  // min-height: 255px;
  transition: box-shadow 0.2s;
  width: 255px;

  &:hover {
    @extend .box-shadow-3;
  }
  &.in-active {
    cursor: default;
    &:hover {
      @extend .box-shadow-5;
    }
  }
  .dot {
    height: 60px;
    width: 60px;
    padding: 7px;
    border-radius: 50%;
    display: inline-block;
    background-color: var(--v-white-base);
    text-align: -webkit-center;
    @extend .box-shadow-1;
  }
  .description {
    min-height: 55px;
  }
}
</style>
