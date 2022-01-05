<template>
  <page class="white add-eng-wrap">
    <div class="steps-wrap">
      <div
        v-if="currentStep <= 1"
        class="step-circle"
        :class="currentStep === 1 ? 'active' : 'in-active'"
      >
        1
      </div>
      <v-icon v-else color="success" size="38" class="step-done">
        mdi-checkbox-marked-circle
      </v-icon>
      <div class="ruler"></div>
      <div
        v-if="currentStep <= 2"
        class="step-circle"
        :class="currentStep === 2 ? 'active' : 'in-active'"
      >
        2
      </div>
      <v-icon v-else color="success" size="38" class="step-done">
        mdi-checkbox-marked-circle
      </v-icon>
      <div class="ruler"></div>
      <div
        v-if="currentStep <= 3"
        class="step-circle"
        :class="currentStep === 3 ? 'active' : 'in-active'"
      >
        3
      </div>
      <v-icon v-else color="success" size="38" class="step-done">
        mdi-checkbox-marked-circle
      </v-icon>
    </div>

    <div v-if="currentStep === 1">
      <div class="add-eng-step-title text-h1">Add an engagement</div>
      <div class="text-body-1">
        Tell us a little bit about this engagement. What is the name of it? What
        is the purpose?
      </div>
    </div>

    <div v-if="currentStep === 2">
      <div class="add-eng-step-title text-h1">Select audiences</div>
      <div class="text-body-1">
        Select what audiences (or create a new one), that you would like to
        target as part of this engagement. Then select the destinations where
        you wish to send these audiences to.
      </div>
    </div>

    <div v-if="currentStep === 3">
      <div class="add-eng-step-title text-h1">Scheduling delivery</div>
      <div class="text-body-1">
        Final step. When would you like to run this engagement? Right now or
        schedule it for later?
      </div>
    </div>

    <engagement-overview v-model="data" class="mt-12" />

    <v-divider class="my-4 mb-6 mr-4"></v-divider>

    <div v-if="currentStep === 1">
      <step-1 v-model="data" />
    </div>

    <div v-if="currentStep === 2">
      <step-2 v-model="data" />
    </div>

    <div v-if="currentStep === 3">
      <step-3 v-model="data" />
    </div>

    <hux-footer>
      <template #left>
        <hux-button
          size="large"
          is-tile
          variant="white"
          height="40"
          class="btn-border box-shadow-none"
          @click.native="$router.go(-1)"
        >
          <span class="primary--text">Cancel &amp; return</span>
        </hux-button>

        <hux-button
          v-if="currentStep > 1"
          size="large"
          is-tile
          variant="white"
          height="40"
          class="btn-border box-shadow-none ml-2"
          @click.native="currentStep--"
        >
          <span class="primary--text">Back</span>
        </hux-button>
      </template>
      <template #right>
        <hux-button
          v-if="currentStep < 3"
          is-tile
          color="primary"
          height="40"
          :is-disabled="!isValid"
          @click.native="currentStep++"
        >
          Next
        </hux-button>
        <hux-button
          v-if="currentStep == 3"
          is-tile
          color="primary"
          height="40"
          :is-disabled="!isValid"
          @click="addNewEngagement()"
        >
          Create
        </hux-button>
        <hux-button
          v-if="currentStep == 3"
          is-tile
          color="primary"
          height="40"
          class="ml-2"
          :is-disabled="!isValid"
          @click="deliverNewEngagement()"
        >
          Create &amp; deliver
        </hux-button>
      </template>
    </hux-footer>

    <confirm-modal
      v-model="showConfirmModal"
      icon="leave-config"
      title="You are about to leave the configuration process"
      right-btn-text="Yes, leave configuration"
      body=" Are you sure you want to stop the configuration and go to another page? You will not be able to recover it and will need to start the process again."
      @onCancel="showConfirmModal = false"
      @onConfirm="navigateaway()"
    />
  </page>
</template>

<script>
//Vuex
import { mapActions } from "vuex"

//Components
import Page from "@/components/Page.vue"
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import HuxFooter from "@/components/common/HuxFooter.vue"
import HuxButton from "@/components/common/huxButton"

//Views
import Step1 from "@/views/Engagements/Configuration/AddSteps/Step1.vue"
import Step2 from "@/views/Engagements/Configuration/AddSteps/Step2.vue"
import Step3 from "@/views/Engagements/Configuration/AddSteps/Step3.vue"
import EngagementOverview from "./Overview.vue"

export default {
  name: "Configuration",

  components: {
    Page,
    ConfirmModal,
    HuxFooter,
    HuxButton,
    Step1,
    Step2,
    Step3,
    EngagementOverview,
  },

  data() {
    return {
      data: {
        name: "",
        description: "",
        audiences: {},
        delivery_schedule: 0,
      },
      showConfirmModal: false,
      currentStep: 1,
      navigateTo: false,
      flagForModal: false,
    }
  },

  computed: {
    isValid() {
      if (this.currentStep === 1) {
        if (!this.data.name) {
          return false
        } else {
          return true
        }
      }
      return true
    },

    payload() {
      const requestPayload = {
        name: this.data.name,
        description: this.data.description,
        audiences: Object.values(this.data.audiences).map((audience) => {
          return {
            id: audience.id,
            destinations: audience.destinations,
          }
        }),
      }
      requestPayload["delivery_schedule"] = null
      return requestPayload
    },
  },

  beforeRouteLeave(to, from, next) {
    if (this.flagForModal == false) {
      this.showConfirmModal = true
      this.navigateTo = to
    } else {
      if (this.navigateTo) next()
    }
  },

  methods: {
    ...mapActions({
      addEngagement: "engagements/add",
      deliverEngagement: "engagements/deliver",
    }),

    navigateaway() {
      this.showConfirmModal = false
      this.flagForModal = true
      this.$router.push(this.navigateTo)
    },

    nextStep() {
      this.currentStep = this.currentStep + 1
    },

    async addNewEngagement() {
      try {
        const engagement = await this.addEngagement(this.payload)
        this.$router.push({
          name: "EngagementDashboard",
          params: { id: engagement.id },
        })
      } catch (error) {
        this.errorMessages.push(error.response.data.message)
        this.scrollToTop()
      }
    },

    async deliverNewEngagement() {
      try {
        const engagement = await this.addEngagement(this.payload)
        await this.deliverEngagement(engagement.id)
        this.$router.push({
          name: "EngagementDashboard",
          params: { id: engagement.id },
        })
      } catch (error) {
        this.errorMessages.push(error.response.data.message)
        this.scrollToTop()
      }
    },
  },
}
</script>
<style lang="scss" scoped>
.add-eng-wrap {
  .steps-wrap {
    display: flex;
    align-items: center;
    .step-circle {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      text-align: center;
      vertical-align: middle;
      line-height: 32px;
      &.active {
        border: 1px solid var(--v-success-base);
        color: var(--v-success-base);
      }
      &.in-active {
        border: 1px solid var(--v-black-lighten2);
        color: var(--v-black-lighten2);
      }
    }
    .step-done {
      margin-top: -3px;
    }
    .ruler {
      width: 40px;
      border-top: 1px dashed var(--v-success-base);
    }
  }
  .add-eng-step-title {
    margin-top: 28px;
  }
}
</style>
