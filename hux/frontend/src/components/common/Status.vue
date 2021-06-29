<template>
  <div v-if="Statuses.Active.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-icon color="success" class="mr-2"> mdi-checkbox-blank-circle </v-icon>
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-icon v-on="on" color="success" class="mr-2">
          mdi-checkbox-blank-circle
        </v-icon>
      </template>
      <div class="px-4 py-2 white" v-if="showLabel">
        {{ status | TitleCase }}
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Inactive.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <v-icon color="columbiaBlue" class="mr-2">
        mdi-checkbox-blank-circle
      </v-icon>
      <span v-if="showLabel">{{ status }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <v-icon v-on="on" color="columbiaBlue" class="mr-2">
          mdi-checkbox-blank-circle
        </v-icon>
      </template>
      <div class="px-4 py-2 white" v-if="showLabel">
        {{ status }}
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Activating.includes(status)">
    <span v-if="!collapsed" class="d-flex align-center">
      <span class="half-left-circle success" />
      <span class="half-right-circle mr-2 secondary" />
      <span v-if="showLabel">{{ status | TitleCase }} </span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template #activator="{ on }">
        <span v-on="on" class="d-flex align-center">
          <span class="half-left-circle success" />
          <span class="half-right-circle mr-2 secondary" />
        </span>
      </template>
      <div class="px-4 py-2 white" v-if="showLabel">
        {{ status | TitleCase }}
      </div>
    </v-menu>
  </div>

  <div v-else-if="Statuses.Pending.includes(status)">
    <span v-if="!collapsed">
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
      <div class="px-4 py-2 white" v-if="showLabel">
        {{ status | TitleCase }}
      </div>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: "status",

  data() {
    return {
      Statuses: {
        Active: ["Active", "Success", "Delivered", "Succeeded"],
        Inactive: ["Caution", "Not Delivered"],
        Activating: ["Activating"],
        Draft: ["Draft"],
        Disabled: ["Disabled"],
        Error: ["Error"],
        Pending: ["Pending", "Delivering"],
      },
    }
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
    showTooltip: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
}
</script>
<style lang="scss" scoped>
.half-right-circle {
  height: 18px;
  width: 9px;
  border-radius: 0 18px 18px 0;
}
.half-left-circle {
  height: 18px;
  width: 9px;
  border-radius: 18px 0 0 18px;
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
