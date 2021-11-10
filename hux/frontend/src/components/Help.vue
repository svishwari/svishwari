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
        <v-list-item class="v-list-item--link" data-e2e="about_hux">
          <a href="#" class="text-body-1 black--text text-decoration-none">
            About Hux
          </a>
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
            Contact Us
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
        <report-bug></report-bug>
      </template>
    </modal>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon"
import Modal from "@/components/common/Modal"
import ContactUsOptions from "./ContactUsOptions.vue"
import ReportBug from "./ReportBug.vue"

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
    }
  },

  methods: {
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
    submit() {
      this.dailog = false
      this.reportBug = false
    },
    executeCardFunction(buttonType) {
      if (buttonType == "Email us") {
        this.sendEmail()
        this.dailog = false
      } else if (buttonType == "Report a bug") {
        this.reportBug = true
      }
    },
    sendEmail() {
      let link = "mailto:ushuxproductidea@deloitte.com"
      window.open(link)
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
