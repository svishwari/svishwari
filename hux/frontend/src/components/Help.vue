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
      :title="reportBug ? 'Report A Bug' : 'Contact Us'"
      data-e2e="contact-us-modal"
      :show-back="reportBug ? true : false"
      :show-confirm="reportBug ? true : false"
      @onCancel="cancel()"
      @onBack="back()"
      @onSubmit="submit()"
    >
      <template v-if="!reportBug" #body>
        <div
          class="
            black--text
            text--darken-4 text-subtitle-1
            font-weight-regular
            px-13
            mt-5
            pb-13
          "
        >
          We’re always trying our best to improve your experience and your
          feedback can help us do that. Please select an option below if you
          feedback, an idea how we can improve, have stumbled upon a bug, or
          simply want to contact us.
        </div>
        <div class="ml-5">
          <plain-card
            v-for="button in buttonCards"
            :key="button.id"
            :icon="button.icon"
            :icon-color="'white'"
            :title="button.name"
            :description="button.desc"
            :style="{ float: 'left' }"
            title-color="black--text"
            height="200"
            width="255"
            class="model-desc-card mr-0"
            data-e2e="contact-us-list"
            @onClick="executeCardFunction(button.name)"
          ></plain-card>
        </div>
      </template>
      <template v-else #body>
        <div
          class="
            black--text
            text--darken-4 text-subtitle-1
            font-weight-regular
            px-13
            mt-5
            pb-13
          "
        >
          Give us some details about the problem you are having.
        </div>
      </template>
    </modal>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon"
import Modal from "@/components/common/Modal"
import PlainCard from "@/components/common/Cards/PlainCard"

export default {
  name: "Help",
  components: {
    Icon,
    Modal,
    PlainCard,
  },

  data() {
    return {
      dailog: false,
      reportBug: false,
      buttonCards: [
        {
          id: "1",
          icon: "system-info",
          name: "General feedback",
          desc: "Have ideas around how to make your Hux experience better? Share them with us.",
        },
        {
          id: "2",
          icon: "error-on-screen",
          name: "Report a bug",
          desc: "Oh no! Did something go wrong? Let’s fix that for you ASAP.",
        },
        {
          id: "3",
          icon: "email-contact-us",
          name: "Email us",
          desc: "Feel free to reach out to us about any of your Hux needs, wants, or problems.",
        },
      ],
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
