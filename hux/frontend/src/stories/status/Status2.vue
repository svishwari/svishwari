<template>
  <div v-if="Statuses.Normal.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-btn
        :width="iconSize"
        :height="iconSize"
        fab
        depressed
        color="success"
        class="mr-2 cursor-default"
      />
      <span v-if="showLabel" class="new-b4">{{ status | TitleCase }} </span>
    </span>
    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-btn
          :width="iconSize"
          :height="iconSize"
          fab
          depressed
          color="success"
          class="mr-2 cursor-default"
          v-on="on"
        />
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column new-b4">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-btn
            v-if="showIconTooltip"
            :width="iconSize"
            :height="iconSize"
            fab
            depressed
            color="success"
            class="mr-2 cursor-default"
          />
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Inactive.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-btn
        :width="iconSize"
        :height="iconSize"
        fab
        depressed
        color="black lighten-5"
        class="mr-2 cursor-default"
      />
      <span v-if="showLabel">{{ status }} </span>
    </span>
    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-btn
          :width="iconSize"
          :height="iconSize"
          fab
          depressed
          color="black lighten-5"
          class="mr-2 cursor-default"
          v-on="on"
        />
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column new-b4">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-btn
            v-if="showIconTooltip"
            :width="iconSize"
            :height="iconSize"
            fab
            depressed
            color="black lighten-5"
            class="mr-2 cursor-default"
          />
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Pending.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-btn
        :width="iconSize"
        :height="iconSize"
        icon
        outlined
        color="success"
        class="dotted mr-2"
      />
      <span v-if="showLabel">
        {{ status | TitleCase }}
      </span>
    </span>
    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-btn
          :width="iconSize"
          :height="iconSize"
          icon
          outlined
          color="success"
          class="dotted mr-2"
          v-on="on"
        />
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column new-b4">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-btn
            v-if="showIconTooltip"
            :width="iconSize"
            :height="iconSize"
            icon
            outlined
            color="success"
            class="dotted mr-2"
          />
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Error.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <icon :size="iconSize" type="failed-error" class="mr-2" />
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>
    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <icon :size="iconSize" type="failed-error" class="mr-2" v-on="on" />
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column new-b4">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <icon :size="iconSize" type="failed-error" class="mr-2" />
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Neutral.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-btn
        :width="iconSize"
        :height="iconSize"
        fab
        depressed
        color="primary"
        class="mr-2 cursor-default"
      />
      <span v-if="showLabel">
        {{ status | TitleCase }}
      </span>
    </span>
    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-btn
          :width="iconSize"
          :height="iconSize"
          fab
          depressed
          color="primary"
          class="mr-2 cursor-default"
          v-on="on"
        />
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column new-b4">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-btn
            v-if="showIconTooltip"
            :width="iconSize"
            :height="iconSize"
            fab
            depressed
            color="primary"
            class="mr-2 cursor-default"
          />
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Unknown.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-btn
        :width="iconSize"
        :height="iconSize"
        fab
        depressed
        color="primary lighten-4"
        class="mr-2 cursor-default"
      />
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>
    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-btn
          :width="iconSize"
          :height="iconSize"
          fab
          depressed
          color="primary lighten-4"
          class="mr-2 cursor-default"
          v-on="on"
        />
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column new-b4">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-btn
            v-if="showIconTooltip"
            :width="iconSize"
            :height="iconSize"
            fab
            depressed
            color="primary lighten-4"
            class="mr-2 cursor-default"
          />
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Guiding.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-btn
        :width="iconSize"
        :height="iconSize"
        fab
        depressed
        color="yellow"
        class="mr-2 cursor-default"
      />
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>
    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-btn
          :width="iconSize"
          :height="iconSize"
          fab
          depressed
          color="yellow"
          class="mr-2 cursor-default"
          v-on="on"
        />
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column new-b4">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-btn
            v-if="showIconTooltip"
            :width="iconSize"
            :height="iconSize"
            fab
            depressed
            color="yellow"
            class="mr-2 cursor-default"
          />
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon.vue"

export default {
  name: "Status",

  components: {
    Icon,
  },

  props: {
    status: {
      type: String,
      required: true,
    },
    collapsed: {
      type: Boolean,
      required: false,
      default: false,
    },
    showLabel: {
      type: Boolean,
      required: false,
      default: true,
    },
    iconSize: {
      type: Number,
      required: false,
      default: 16,
    },
    tooltipTitle: {
      type: String,
      required: false,
      default: "",
    },
    showIconTooltip: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      Statuses: {
        Normal: ["Active", "Delivered", "Done"],
        Inactive: ["Delivery paused", "Inactive", "Disabled"],
        Error: ["Error", "Failed"],
        Pending: ["Requested", "Delivering", "Incomplete"],
        Neutral: ["In progress"],
        Unknown: ["Not delivered", "In review", "Canceled"],
        Guiding: ["To do"],
      },
    }
  },
}
</script>
<style lang="scss" scoped>
.v-icon,
.v-btn--icon {
  cursor: default !important;
}
.half-right-circle {
  height: 14px;
  width: 7px;
  border-radius: 0 14px 14px 0;
}
.half-left-circle {
  height: 14px;
  width: 7px;
  border-radius: 14px 0 0 14px;
}
.dotted {
  border-style: dotted;
  border-width: 2px;

  &:hover {
    animation: spin 3s infinite linear;

    @keyframes spin {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }
  }
}
.hover-button-margin {
  margin-left: 1.5px !important;
}
</style>
