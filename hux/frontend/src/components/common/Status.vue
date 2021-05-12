<template>
  <div v-if="status == Statuses.Active">
    <span v-if="!collapsed">
      <v-icon color="success" class="mr-2"> mdi-checkbox-blank-circle </v-icon>
      <span>Active</span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template v-slot:activator="{ on }">
        <v-icon v-on="on" color="success" class="mr-2">
          mdi-checkbox-blank-circle
        </v-icon>
      </template>
      <div class="px-4 py-2 white">Active</div>
    </v-menu>
  </div>

  <div v-else-if="status == Statuses.Activating">
    <span v-if="!collapsed" class="d-flex align-center">
      <span class="half-left-circle success" />
      <span class="half-right-circle mr-2 secondary" />
      <span>Activating</span>
    </span>

    <v-menu v-else bottom offset-y open-on-hover>
      <template v-slot:activator="{ on }">
        <span v-on="on" class="d-flex align-center">
          <span class="half-left-circle success" />
          <span class="half-right-circle mr-2 secondary" />
        </span>
      </template>
      <div class="px-4 py-2 white">Activating</div>
    </v-menu>
  </div>

  <div v-else-if="status == Statuses.Pending">
    <span v-if="!collapsed">
      <v-btn
        style="border-style: dashed"
        width="18"
        height="18"
        icon
        outlined
        color="success"
        class="mr-2"
      />
      <span>Pending</span>
    </span>
    <v-menu v-else bottom offset-y open-on-hover>
      <template v-slot:activator="{ on }">
        <v-btn
          style="border-style: dashed"
          width="18"
          height="18"
          icon
          outlined
          color="success"
          class="mr-2"
          v-on="on"
        />
      </template>
      <div class="px-4 py-2 white">Pending</div>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: "status",

  data() {
    return {
      Statuses: {
        Active: "success",
        Inactive: "caution",
        Activating: "activating",
        Draft: "draft",
        Disabled: "disabled",
        Error: "error",
        Pending: "pending",
        Delivering: "delivering",
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
</style>
