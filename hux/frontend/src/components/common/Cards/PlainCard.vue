<template>
  <v-card
    :outlined="disabled"
    class="plain-card align-center text-center rounded-lg card-space mb-10"
    :class="{ 'in-active': disabled }"
    :height="height"
    :width="width"
    :to="to"
    @click="onClick"
  >
    <div v-if="icon" class="d-flex justify-center mt-6">
      <div class="dot">
        <logo
          v-if="logoOption"
          :type="icon"
          :size="44"
          :color="iconColor"
          class="d-block"
        />
        <icon
          v-else
          :type="icon"
          :size="44"
          :color="iconColor"
          class="d-block"
        />
      </div>
    </div>

    <template>
      <div
        class="px-6 pb-1 pt-2 d-block title black-base text-button"
        :style="{ 'padding-top': !icon ? '56px' : null }"
        data-e2e="card-title"
      >
        {{ title }}
      </div>
    </template>

    <template>
      <div
        class="px-3 d-block description text-body-2 desc-color"
        :style="{ 'padding-top': !icon ? '22px' : null }"
        data-e2e="card-description"
      >
        {{ description }}
      </div>
    </template>

    <div v-if="$slots.default" class="px-3 pt-2">
      <slot />
    </div>
  </v-card>
</template>

<script>
import Icon from "@/components/common/Icon"
import Logo from "@/components/common/Logo"

export default {
  name: "PlainCard",

  components: {
    Icon,
    Logo,
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
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    actionMenu: {
      type: Boolean,
      required: false,
      default: false,
    },
    comingSoon: {
      type: Boolean,
      required: false,
      default: false,
    },
    height: {
      type: [Number, String],
      required: true,
    },
    width: {
      type: [Number, String],
      required: true,
    },
    to: {
      type: Object,
      required: false,
      default: () => {},
    },
    dotOption: {
      type: String,
      required: false,
      default: "Activate",
    },
    logoOption: {
      type: Boolean,
      required: false,
      default: false,
    },
    iconColor: {
      type: String,
      required: false,
      default: "Primary",
    },
  },

  methods: {
    onClick() {
      this.$emit("onClick")
    },
  },
}
</script>

<style lang="scss" scoped>
.plain-card {
  @extend .box-shadow-5;
  color: var(--v-black-darken4);
  font-weight: normal;
  transition: box-shadow 0.2s;
  cursor: pointer;

  &:hover {
    @extend .box-shadow-3;
  }
  &.in-active {
    cursor: default;
    background-color: var(--v-primary-lighten1);
    &:hover {
      @extend .box-shadow-5;
    }
    .coming-soon {
      width: 104px;
      height: 28px;
      margin-top: -12px;
      position: absolute;
      right: 0;
      background: #e2eaec;
      border-radius: 0px 12px;
      padding: 4px;
    }
  }
  .dot {
    width: 60px;
    height: 60px;
    padding: 8px;
    border-radius: 50%;
    background: var(--v-white-base);
  }
  .description {
    -webkit-box-orient: vertical !important;
    -webkit-line-clamp: 2 !important;
  }
}
.card-space {
  margin-right: 24px !important;
}
.desc-color {
  color: var(--v-black-lighten4) !important;
}
</style>
