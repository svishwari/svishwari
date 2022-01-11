<template>
  <div class="eng-step-3">
    <div class="black--text text-body-1">
      Set up a default delivery schedule
    </div>
    <v-row class="my-2 ml-1">
      <div class="d-flex">
        <div
          class="cursor-pointer text-center rounded-lg manual py-5 px-5 mr-2"
          :class="[isActive ? 'active' : 'box-shadow-1']"
          @click="toggleClass($event)"
        >
          <icon
            type="manual"
            :color="isActive ? 'primary' : 'black'"
            :variant="isActive ? 'lighten6' : ''"
            :size="40"
          />
          <div
            class="mt-2 text-button"
            :class="isActive ? 'primary--text text--lighten-6' : ''"
          >
            Manual
          </div>
          <div class="pt-2 black--text text--lighten-4 text-body-2">
            Deliver this engagement when you are ready.
          </div>
        </div>
        <div
          class="cursor-pointer text-center rounded-lg recurring py-5 px-5 ml-2"
          :class="[!isActive ? 'active' : 'box-shadow-1']"
          @click="toggleClass($event)"
        >
          <icon
            type="recurring"
            :color="!isActive ? 'primary' : 'black'"
            :variant="!isActive ? 'lighten6' : ''"
            :size="40"
          />
          <div
            class="mt-2 text-button"
            :class="!isActive ? 'primary--text text--lighten-6' : ''"
          >
            Recurring
          </div>
          <div class="pt-2 black--text text--lighten-4 text-body-2">
            Deliver this engagement during a chosen timeframe.
          </div>
        </div>
        <audience-lists :value="value" />
      </div>
    </v-row>
  </div>
</template>

<script>
//Components
import Icon from "@/components/common/Icon"
import AudienceLists from "../AudienceLists"

export default {
  name: "Step3",

  components: {
    Icon,
    AudienceLists,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      isActive: true,
      errorMessages: [],
    }
  },

  methods: {
    toggleClass: function (event) {
      if (!event.currentTarget.classList.contains("active")) {
        this.isActive = !this.isActive
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.eng-step-3 {
  margin-right: 16px;
  .row {
    .d-flex {
      .manual,
      .recurring {
        height: 175px;
        width: 199px;
        border-radius: 12px;
      }
      .manual.active,
      .recurring.active {
        border: 1px solid var(--v-primary-lighten4);
      }
    }
  }
}
</style>
