<template>
  <v-card
    :disabled="disabled"
    class="descriptive-card align-center text-center rounded-lg card-space mb-4"
    :width="getWidth"
  >
    <div class="pa-4 pb-6">
      <div v-if="status">
        <status
          :icon-size="16"
          :status="status"
          collapsed
          class="d-flex float-left"
        />
      </div>
      <div v-if="actionMenu">
        <v-menu close-on-click>
          <template #activator="{ on, attrs }">
            <v-icon
              class="d-flex float-right"
              v-bind="attrs"
              color="primary"
              v-on="on"
            >
              mdi-dots-vertical
            </v-icon>
          </template>
          <div class="black--text text-darken-4 cursor-pointer white">
            <slot name="action-menu-options"></slot>
          </div>
        </v-menu>
      </div>
    </div>
    <div v-if="icon" class="d-flex justify-center">
      <div class="dot" :style="{ padding: logoBoxPadding }">
        <logo
          v-if="logoOption"
          :type="icon"
          :size="logoSize"
          :color="iconColor"
          class="d-block"
          :class="logoSize === 60 ? 'icon-margin' : ''"
        />
        <icon
          v-else
          :type="icon"
          :size="32"
          :color="iconColor"
          class="d-block"
        />
      </div>
    </div>
    <v-card class="pt-4">
      <div :class="description || $slots.body ? '' : 'pa-4'" class="text-h3">
        {{ title }}
      </div>
      <v-chip v-if="pill" disabled>{{ pill }}</v-chip>
      <div v-if="description" class="pt-2" :class="$slots.body ? '' : 'pa-4'">
        {{ description }}
      </div>
      <div v-if="$slots.body" class="pa-4 pt-2">
        <slot name="body"></slot>
      </div>
    </v-card>
  </v-card>
</template>

<script>
import Icon from "@/components/common/Icon"
import Logo from "@/components/common/Logo"
import Status from "@/components/common/Status"

export default {
  name: "DescriptiveCard",

  components: {
    Icon,
    Logo,
    Status,
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
    actionMenu: {
      type: Boolean,
      required: false,
      default: false,
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
    descriptionHeight: {
      type: String,
      required: false,
      default: "auto",
    },
    logoSize: {
      type: Number,
      required: false,
      default: 32,
    },
    logoBoxPadding: {
      type: String,
      required: false,
      default: "14px",
    },
    topRightAdjustment: {
      type: String,
      required: false,
      default: "mt-3 mr-8",
    },
    size: {
      type: String,
      required: false,
      default: "small",
    },
    status: {
      type: String,
      required: false,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    pill: {
      type: String,
      required: false,
    },
  },

  computed: {
    getWidth() {
      return this.size == "small" ? 270 : 368
    },
  },
}
</script>

<style lang="scss" scoped>
.descriptive-card {
  @extend .box-shadow-5;
  color: var(--v-black-darken4);
  font-weight: normal;
  transition: box-shadow 0.2s;

  &.interactable {
    cursor: pointer;
  }

  &.non-interactable {
    cursor: default;
    &:hover {
      @extend .box-shadow-none;
    }
  }

  &:hover {
    @extend .box-shadow-3;
  }
  &.in-active {
    @extend .box-shadow-none;
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
    border-radius: 50%;
    @extend .box-shadow-1;
    background: var(--v-white-base);
    text-align: -webkit-center;
  }
  .description {
    -webkit-box-orient: vertical !important;
    -webkit-line-clamp: 2 !important;
    overflow: hidden !important;
    display: -webkit-box !important;
  }
}
.card-space {
  margin-right: 24px !important;
}
.icon-margin {
  margin-left: -10px !important;
  margin-top: -10px !important;
}
.v-menu__content {
  &.theme--light {
    &.menuable__content__active {
      margin-top: 28px !important;
    }
  }
}
</style>
