<template>
  <div>
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
      We’re always trying our best to improve your experience and your feedback
      can help us do that. Please select an option below if you have feedback,
      an idea for how we can improve, have stumbled upon a bug, or simply want
      to contact us.
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
      />
    </div>
  </div>
</template>

<script>
import PlainCard from "@/components/common/Cards/PlainCard"

export default {
  name: "ContactUsOptions",

  components: {
    PlainCard,
  },

  data() {
    return {
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
    executeCardFunction(name) {
      this.$emit("executeCardFunction", name)
    },
  },
}
</script>
