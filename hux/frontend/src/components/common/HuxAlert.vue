<template>
  <div class="hux-alert">
    <v-card
      v-for="item in alerts"
      :key="item.id"
      min-height="56"
      class="alert-card"
      rounded="0"
    >
      <div class="hux-alert-container">
        <v-btn
          v-if="item.type === 'pending'"
          width="15"
          height="15"
          icon
          outlined
          color="success"
          class="dotted mr-2"
        />
        <icon
          v-else
          :type="iconType(item.type)"
          :size="15"
          class="alert-icon mr-5"
          :color="iconColor(item.type)"
          :variant="iconVariant(item.type)"
        />
        <div
          v-if="item.type !== 'pending'"
          class="alert-title text-subtitle-1"
          :class="colorClass(item.type)"
        >
          {{ title(item.type) }}
        </div>
        <div class="pr-6 text-body-2" :class="colorClass(item.type)">
          {{ item.message }}
        </div>
      </div>
      <icon
        type="cross"
        :size="14"
        color="primary"
        class="alert-icon cursor-pointer"
        @click.native="() => removeAlertByID(item.id)"
      />
    </v-card>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon"
import { mapGetters, mapActions } from "vuex"
export default {
  name: "HuxAlert",
  components: {
    Icon,
  },

  computed: {
    ...mapGetters({
      alerts: "alerts/list",
    }),
  },

  methods: {
    ...mapActions({
      removeAlert: "alerts/removeAlert",
    }),

    iconType(type) {
      const defaultIcons = {
        success: "alert-success",
        error: "alert-error",
        feedback: "alert-feedback",
      }
      return defaultIcons[type] || "info_outlined"
    },

    iconColor(type) {
      const defaultIconColor = {
        success: "success",
        error: "error",
      }
      return defaultIconColor[type] || "primary"
    },

    iconVariant(type) {
      const defaultVariants = {
        feedback: "lighten8",
      }
      return defaultVariants[type] || "base"
    },

    title(type) {
      const defaultTitles = {
        success: "YAY!",
        error: "OH NO!",
        feedback: "FEEDBACK",
      }
      return defaultTitles[type] || ""
    },

    colorClass(type) {
      const defaultClasses = {
        success: "success--text",
        error: "error--text",
        feedback: "primary--text text--lighten-8",
        pending: "success--text",
      }
      return defaultClasses[type] || "black--text text--darken-4"
    },

    removeAlertByID(id) {
      this.removeAlert(id)
    },
  },
}
</script>

<style lang="scss" scoped>
.hux-alert {
  position: fixed;
  left: 50%;
  transform: translate(-50%, 0);
  z-index: 99;
  top: 20px;

  .hux-alert-container {
    display: flex;
    align-items: center;
    flex-basis: 100%;
    .alert-title {
      padding-right: 16px;
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
  }

  .alert-icon {
    min-width: 15px;
  }

  .alert-card {
    @extend .box-shadow-25;
    display: flex;
    align-items: center;
    padding: 16px 20px;
    margin-bottom: 16px;
    justify-content: space-between;
    max-width: max-content;
    margin-left: auto;
    margin-right: auto;
  }
}
</style>
