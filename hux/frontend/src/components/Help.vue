<template>
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
        @click.stop="openModal()"
      >
        <a
          href="javascript:void(0)"
          class="text-body-1 black--text view-all text-decoration-none"
        >
          Contact Us
        </a>
      </v-list-item>
    </v-list>
    <modal
      v-model="dailog"
      title="Contact Us"
      data-e2e="contact-us-modal"
      @onCancel="cancelRemoval()"
    >
      <template #body>
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

        <descriptive-card
          v-for="button in buttonCards"
          :key="button.id"
          :icon="button.icon"
          :icon-color="'white'"
          :title="button.name"
          :description="button.desc"
          height="225"
          width="255"
          class="mr-10 model-desc-card ml-10"
          data-e2e="contact-us-list"
        ></descriptive-card>
      </template>
    </modal>
  </v-menu>
</template>

<script>
import Icon from "@/components/common/Icon"
import Modal from "@/components/common/Modal"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"

export default {
  name: "Help",
  components: {
    Icon,
    Modal,
    DescriptiveCard,
  },

  data() {
    return {
      dailog: false,
      buttonCards: [
        {
          id: "1",
          icon: "",
          name: "General feedback",
          desc: "Have ideas around how to make your Hux experience better? Share them with us.",
        },
      ],
    }
  },

  methods: {
    openModal() {
      this.dailog = true
    },
    cancelRemoval() {
      this.dailog = false
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
