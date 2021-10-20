<template>
  <div v-if="Statuses.Active.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-icon color="success" class="mr-2" :size="iconSize">
        mdi-checkbox-blank-circle
      </v-icon>
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-icon color="success" class="mr-2" :size="iconSize" v-on="on">
          mdi-checkbox-blank-circle
        </v-icon>
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column text-h5">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-icon
            v-if="showIconTooltip"
            color="success"
            class="mr-2"
            :size="iconSize"
          >
            mdi-checkbox-blank-circle
          </v-icon>
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses['Not Delivered'].includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-icon color="primary lighten-4" class="mr-2" :size="iconSize">
        mdi-checkbox-blank-circle
      </v-icon>
      <span v-if="showLabel">{{ status }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-icon
          color="primary lighten-4"
          class="mr-2"
          :size="iconSize"
          v-on="on"
        >
          mdi-checkbox-blank-circle
        </v-icon>
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column text-h5">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-icon
            v-if="showIconTooltip"
            color="primary lighten-4"
            class="mr-2"
            :size="iconSize"
          >
            mdi-checkbox-blank-circle
          </v-icon>
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Inactive.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-icon color="black-lighten3" class="mr-2" :size="iconSize">
        mdi-checkbox-blank-circle
      </v-icon>
      <span v-if="showLabel">{{ status }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-icon color="black-lighten3" class="mr-2" :size="iconSize" v-on="on">
          mdi-checkbox-blank-circle
        </v-icon>
      </template>
      <div
        v-if="showLabel"
        class="px-4 py-2 white d-flex flex-column text-button"
      >
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-icon
            v-if="showIconTooltip"
            color="black lighten-3"
            class="mr-2"
            :size="iconSize"
          >
            mdi-checkbox-blank-circle
          </v-icon>
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Activating.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <span class="half-left-circle success" />
      <span class="half-right-circle mr-2 primary lighten-8" />
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <span class="d-flex align-center" v-on="on">
          <span class="half-left-circle success" />
          <span class="half-right-circle mr-2 primary lighten-8" />
        </span>
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column text-h5">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <span v-if="showIconTooltip" class="d-flex align-center">
            <span class="half-left-circle success" />
            <span class="half-right-circle mr-2 primary lighten-8" />
            <span v-if="showLabel">{{ status | TitleCase }} </span>
          </span>
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Pending.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-btn
        width="15"
        height="15"
        icon
        outlined
        color="success"
        class="dotted mr-2"
      />
      <span v-if="showLabel">
        {{ status | TitleCase }}
      </span>
    </span>
    <v-menu v-else bottom offset-y offset-x open-on-hover>
      <template #activator="{ on }">
        <v-btn
          width="15"
          height="15"
          icon
          outlined
          color="success"
          class="dotted"
          style="margin-left: 1.5px"
          v-on="on"
        />
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column text-h5">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-btn
            v-if="showIconTooltip"
            width="15"
            height="15"
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

  <div v-else-if="Statuses.Requested.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-btn
        width="15"
        height="15"
        icon
        outlined
        color="primary lighten-6"
        class="dotted mr-2"
      />
      <span v-if="showLabel">
        {{ status | TitleCase }}
      </span>
    </span>
    <v-menu v-else bottom offset-y offset-x open-on-hover>
      <template #activator="{ on }">
        <v-btn
          width="15"
          height="15"
          icon
          outlined
          color="primary lighten-6"
          class="dotted"
          style="margin-left: 1.5px"
          v-on="on"
        />
      </template>

      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column text-h5">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-btn
            v-if="showIconTooltip"
            width="15"
            height="15"
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
      <v-icon color="red" class="mr-2" :size="iconSize">
        mdi-information
      </v-icon>
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-icon color="red" class="mr-2" :size="iconSize" v-on="on">
          mdi-information
        </v-icon>
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column text-h5">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-icon
            v-if="showIconTooltip"
            color="red"
            class="mr-2"
            :size="iconSize"
          >
            mdi-information
          </v-icon>
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Feedback.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-icon color="blue" class="mr-2" :size="iconSize">
        mdi-message-alert
      </v-icon>
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-icon color="blue" class="mr-2" :size="iconSize" v-on="on">
          mdi-message-alert
        </v-icon>
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column text-h5">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-icon
            v-if="showIconTooltip"
            color="blue"
            class="mr-2"
            :size="iconSize"
          >
            mdi-message-alert
          </v-icon>
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Draft.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-icon color="blue" class="mr-2" :size="iconSize">
        mdi-checkbox-blank-circle-outline
      </v-icon>
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-icon color="blue" class="mr-2" :size="iconSize" v-on="on">
          mdi-checkbox-blank-circle-outline
        </v-icon>
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column text-h5">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-icon
            v-if="showIconTooltip"
            color="blue"
            class="mr-2"
            :size="iconSize"
          >
            mdi-checkbox-blank-circle-outline
          </v-icon>
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Success.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-icon color="green" class="mr-2" :size="iconSize">
        mdi-checkbox-marked-circle
      </v-icon>
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-icon color="green" class="mr-2" :size="iconSize" v-on="on">
          mdi-checkbox-marked-circle
        </v-icon>
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column text-h5">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-icon
            v-if="showIconTooltip"
            color="green"
            class="mr-2"
            :size="iconSize"
          >
            mdi-checkbox-marked-circle
          </v-icon>
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Informational.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-icon color="blue" class="mr-2" :size="iconSize">
        mdi-message-alert
      </v-icon>
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-icon color="blue" class="mr-2" :size="iconSize" v-on="on">
          mdi-message-alert
        </v-icon>
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column text-h5">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-icon
            v-if="showIconTooltip"
            color="blue"
            class="mr-2"
            :size="iconSize"
          >
            mdi-message-alert
          </v-icon>
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Stopped.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-icon color="black lighten-3" class="mr-2" :size="iconSize">
        mdi-checkbox-blank-circle
      </v-icon>
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-icon color="black lighten-3" class="mr-2" :size="iconSize" v-on="on">
          mdi-checkbox-blank-circle
        </v-icon>
      </template>
      <div v-if="showLabel" class="px-4 py-2 white d-flex flex-column text-h5">
        <span v-if="tooltipTitle" class="mb-2">{{ tooltipTitle }} </span>
        <span class="d-flex align-center">
          <v-icon
            v-if="showIconTooltip"
            color="black lighten-3"
            class="mr-2"
            :size="iconSize"
          >
            mdi-checkbox-blank-circle
          </v-icon>
          {{ status | TitleCase }}
        </span>
      </div>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: "Status",

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
    showTooltip: {
      type: Boolean,
      required: false,
      default: true,
    },
    iconSize: {
      type: Number,
      required: false,
      default: 24,
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
        Active: ["Active", "Delivered", "Succeeded"],
        Inactive: ["Caution", "Inactive"],
        Activating: ["Activating", "In progress"],
        Draft: ["Draft"],
        Error: ["Error", "Failed", "Critical"],
        Pending: ["Pending", "Delivering"],
        Feedback: ["Feedback"],
        Success: ["Success"],
        Informational: ["Informational"],
        Stopped: ["Stopped"],
        Requested: ["Requested"],
        "Not Delivered": ["Not Delivered"],
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
</style>
