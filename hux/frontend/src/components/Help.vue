<template>
  <div>
    <v-menu :min-width="192" left offset-y close-on-click>
      <template #activator="{ on }">
        <span
          class="d-flex cursor-pointer mr-4"
          data-e2e="help-dropdown"
          v-on="on"
        >
          <icon class="mx-2 my-2 nav-icon" type="help" :size="24" />
        </span>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title class="font-weight-semi-bold text-h6 black--text">
            Help
          </v-list-item-title>
        </v-list-item>
        <v-list-item
          class="v-list-item--link"
          data-e2e="contactus"
          @click="openModal()"
        >
          <a
            href="javascript:void(0)"
            class="text-body-1 black--text view-all text-decoration-none"
          >
            Contact us
          </a>
        </v-list-item>
      </v-list>
    </v-menu>
    <modal
      v-model="dailog"
      :title="reportBug ? 'Report a bug' : 'Contact us'"
      data-e2e="contact-us-modal"
      :show-back="reportBug ? true : false"
      :show-confirm="reportBug ? true : false"
      @onCancel="cancel()"
      @onBack="back()"
      @onSubmit="submit()"
    >
      <template v-if="!reportBug" #body>
        <contact-us-options
          @executeCardFunction="executeCardFunction"
        ></contact-us-options>
      </template>
      <template v-else #body>
        <report-bug @setBugDetails="setBugDetails"></report-bug>
      </template>
    </modal>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon"
import Modal from "@/components/common/Modal"
import ContactUsOptions from "./ContactUsOptions.vue"
import ReportBug from "./ReportBug.vue"
import { mapActions } from "vuex"

export default {
  name: "Help",
  components: {
    Icon,
    Modal,
    ContactUsOptions,
    ReportBug,
  },

  data() {
    return {
      dailog: false,
      reportBug: false,
      bugDetails: {},
    }
  },

  methods: {
    ...mapActions({
      contactUs: "users/contactUs",
      setAlert: "alerts/setAlert",
    }),
    openModal() {
      this.dailog = true
    },
    cancel() {
      this.dailog = false
      this.reportBug = false
    },
    back() {
      this.reportBug = false
    },
    async submit() {
      await this.contactUs(this.bugDetails)
      this.dailog = false
      this.reportBug = false
    },
    executeCardFunction(buttonType) {
      let emailLink = "mailto:ushuxproductidea@deloitte.com"
      let generalSurvey =
        "https://deloittesurvey.deloitte.com/Community/se/3FC11B267AFCA9B6"

      if (buttonType == "Report a bug") {
        this.reportBug = true
      } else if (buttonType == "Email us") {
        window.open(emailLink)
        this.dailog = false
      } else {
        window.open(generalSurvey)
        this.dailog = false
      }
    },
    setBugDetails(bugObj) {
      this.bugDetails = bugObj
    },
  },
}
</script>

<style lang="scss" scoped>
.v-menu__content {
  top: 64px !important;
  .v-list {
    .v-list-item {
      min-height: 40px !important;
    }
  }
}
.view-all {
  @extend .cursor-pointer;
}
</style>
