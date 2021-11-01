<template>
  <page class="white">
    <template #header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </template>

    <h2 class="text-h2">{{ formTitle }}</h2>

    <p class="mb-10">
      Tell us a little bit about this engagement. What are its goals? When are
      you planning to run it? Who are you targeting? If you don’t know yet -
      that’s okay! You can always fill out the details later.
    </p>

    <engagement-overview v-model="data" />

    <v-divider class="divider my-4 mb-8"></v-divider>

    <engagement-form ref="editEngagement" v-model="data" />

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
import { mapActions, mapGetters } from "vuex"
import Page from "@/components/Page.vue"
import EngagementOverview from "./Overview.vue"
import EngagementForm from "./Form.vue"
import ConfirmModal from "@/components/common/ConfirmModal.vue"

export default {
  name: "Configuration",

  components: {
    Page,
    EngagementOverview,
    EngagementForm,
    ConfirmModal,
  },

  data() {
    return {
      data: {
        name: "",
        description: "",
        audiences: {},
        delivery_schedule: 0,
      },

      loading: false,
      showConfirmModal: false,
      navigateTo: false,
      flagForModal: false,
    }
  },

  computed: {
    ...mapGetters({
      getEngagementObject: "engagements/engagement",
    }),

    formTitle() {
      return this.$route.params.id
        ? `Edit ${this.data.name} `
        : "Add an engagement"
    },
  },

  beforeRouteLeave(to, from, next) {
    if (this.$refs.editEngagement.dontShowModal) {
      next()
    } else {
      if (this.flagForModal == false) {
        this.showConfirmModal = true
        this.navigateTo = to
      } else {
        if (this.navigateTo) next()
      }
    }
  },

  async mounted() {
    this.loading = true
    await this.getAudiences()
    await this.getDestinations()
    if (this.$route.name === "EngagementUpdate") {
      await this.loadEngagement(this.$route.params.id)
    }
    this.loading = false
  },

  methods: {
    ...mapActions({
      getAudiences: "audiences/getAll",
      getDestinations: "destinations/getAll",
      getEngagementById: "engagements/get",
    }),
    navigateaway() {
      this.showConfirmModal = false
      this.flagForModal = true
      this.$router.push(this.navigateTo)
    },
    async loadEngagement(engagementId) {
      await this.getEngagementById(engagementId)
      this.engagementList = this.getEngagementObject(engagementId)
      let audiences = {}
      this.engagementList.audiences.map((each) => {
        audiences[each.id] = each
      })

      // Set value in form
      const _engagementObject = {
        name: this.engagementList.name, // at step - 1
        description: this.engagementList.description, // at step - 1
        delivery_schedule: !this.engagementList.delivery_schedule ? 0 : 1, // at step - 2
        audiences: audiences, // at step - 3
        schedule: this.engagementList.delivery_schedule
          ? this.engagementList.delivery_schedule.schedule
          : {},
      }
      this.$set(this, "data", _engagementObject)

      // Set date at step - 2
      if (this.engagementList.delivery_schedule) {
        // set start date
        this.$refs.editEngagement.onStartDateSelect(
          this.$options.filters.Date(
            this.engagementList.delivery_schedule.start_date,
            "YYYY-MM-DD"
          )
        )
        // set end date
        this.$refs.editEngagement.onEndDateSelect(
          this.$options.filters.Date(
            this.engagementList.delivery_schedule.end_date,
            "YYYY-MM-DD"
          )
        )
      }
    },
  },
}
</script>
