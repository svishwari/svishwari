<template>
  <v-card
    :outlined="disabled"
    class="descriptive-card align-center text-center rounded-lg card-space mb-6"
    :class="[
      disabled ? 'in-active' : '',
      interactable ? 'interactable' : 'non-interactable',
    ]"
    :height="height"
    :width="width"
    :to="to"
  >
    <div v-if="$slots.top" class="card-status pa-3 pb-0">
      <slot name="top" />
      <v-menu close-on-click>
        <template #activator="{ on, attrs }">
          <v-icon
            v-if="actionMenu"
            id="menu-icon-card"
            class="d-flex float-right"
            v-bind="attrs"
            color="primary"
            v-on="on"
          >
            mdi-dots-vertical
          </v-icon>
        </template>
        <div
          id="menu-options-card"
          class="black--text text-darken-4 cursor-pointer white"
        >
          <slot name="action-menu-options"></slot>
        </div>
      </v-menu>
      <div v-if="comingSoon" class="coming-soon d-flex float-right mt-n4">
        Coming soon!
      </div>
    </div>

    <div v-if="icon" class="d-flex justify-center" :class="topRightAdjustment">
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

    <tooltip nudge-right="100px" min-width="auto !important">
      <template #label-content>
        <div
          class="text-h4 px-6 pb-1 pt-2 text-ellipsis d-block title text-h4"
          :class="disabled || !interactable ? 'black--text' : 'primary--text'"
          :style="{ 'padding-top': !icon ? '56px' : null }"
          data-e2e="card-title"
        >
          {{ title }}
        </div>
      </template>
      <template #hover-content>
        <span class="black--text text-body-2">{{ title }}</span>
      </template>
    </tooltip>

    <!-- <template v-else>
      <div
        class="text-h4 px-6 pb-1 pt-2 text-ellipsis d-block title"
        :class="disabled || !interactable ? 'black--text' : 'primary--text'"
        :style="{ 'padding-top': !icon ? '56px' : null }"
        data-e2e="card-title"
      >
        {{ title }}
      </div>
    </template> -->

    <tooltip nudge-right="100px" min-width="auto !important">
      <template #label-content>
        <div
          class="px-3 pb-2 d-block text-body-2 black--text text--lighten-4"
          :style="{
            'padding-top': !icon ? '22px' : null,
            height: 21,
          }"
          data-e2e="card-subtitle"
        >
          {{ subTitle }}
        </div>
      </template>
      <template #hover-content>
        <span class="black--text text-body-2 text--lighten-4">{{
          subTitle
        }}</span>
      </template>
    </tooltip>

    <tooltip
      v-if="!noDescription"
      nudge-right="100px"
      min-width="auto !important"
    >
      <template #label-content>
        <div
          class="px-3 d-block description text-body-2 black--text"
          :style="{
            'padding-top': !icon ? '22px' : null,
            height: descriptionHeight,
          }"
          data-e2e="card-description"
        >
          {{ description }}
        </div>
      </template>
      <template #hover-content>
        <span class="black--text text-body-2">{{ description }}</span>
      </template>
    </tooltip>

    <div v-if="$slots.default" class="px-3">
      <slot />
    </div>
  </v-card>
</template>

<script>
import Icon from "@/components/common/Icon"
import Tooltip from "@/components/common/Tooltip"
import Logo from "@/components/common/Logo"

export default {
  name: "DescriptiveCard",

  components: {
    Icon,
    Tooltip,
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
    subTitle: {
      type: String,
      required: false,
      default: "",
    },
    noDescription: {
      type: Boolean,
      required: false,
      default: false,
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
    interactable: {
      type: Boolean,
      required: false,
      default: false,
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
  },

  // mounted() {
  //   if (
  //     document.getElementById("menu-options-card") &&
  //     document.getElementById("menu-options-card").children.length == 0
  //   ) {
  //     document.getElementById("menu-icon-card").style.cssText =
  //       "display:none !important"
  //   } else {
  //     document.getElementById("menu-icon-card").style.cssText =
  //       "display:flex !important"
  //   }
  // },
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
      @extend .box-shadow-5;
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
    -webkit-line-clamp: 2;
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
