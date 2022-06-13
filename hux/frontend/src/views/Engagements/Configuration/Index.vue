<template>
  <page class="white edit-engagement-wrap">
    <template #header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </template>
    <div class="d-flex align-items-center justify-space-between">
      <div>
        <h2 class="text-h1">{{ formTitle }}</h2>

        <p class="body-1 mb-10">
          Keep in mind that by editing this engagement you may impact related
          audiences and destinations.
        </p>
      </div>
      <div class="pt-5 re-align-delete">
        <tooltip nudge-right="-90" max-width="115">
          <template #label-content>
            <div @click="openModal()">
              <icon size="23" type="delete-button" color="darkD" />
            </div>
          </template>
          <template #hover-content>
            <span>Delete engagement</span>
          </template>
        </tooltip>
      </div>
    </div>
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
    <confirm-modal
      v-model="confirmModal"
      icon="sad-face"
      type="error"
      title="You are about to delete"
      :sub-title="`${confirmSubtitle}`"
      right-btn-text="Yes, delete engagement"
      left-btn-text="Nevermind!"
      @onCancel="confirmModal = !confirmModal"
      @onConfirm="confirmRemoval()"
    >
      <template #body>
        <div
          class="
            black--text
            text--darken-4 text-subtitle-1
            pt-6
            font-weight-regular
          "
        >
          Are you sure you want to delete this Engagement&#63;
        </div>
        <div
          class="black--text text--darken-4 text-subtitle-1 font-weight-regular"
        >
          By deleting this engagement you will not be able to recover it and it
          may impact any associated destinations.
        </div>
      </template>
    </confirm-modal>
  </page>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Page from "@/components/Page.vue"
import EngagementOverview from "./Overview.vue"
import EngagementForm from "./Form.vue"
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import Icon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "Configuration",

  components: {
    Page,
    EngagementOverview,
    EngagementForm,
    ConfirmModal,
    Icon,
    Tooltip,
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
      confirmModal: false,
      confirmSubtitle: "",
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
    if (this.$refs.editEngagement.dontShowModal || !this.confirmModal) {
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
    try {
      await this.getAudiences()
      await this.getDestinations()
      if (this.$route.name === "EngagementUpdate") {
        await this.loadEngagement(this.$route.params.id)
      }
    } finally {
      this.loading = false
    }
  },

  methods: {
    ...mapActions({
      getAudiences: "audiences/getAll",
      getDestinations: "destinations/getAll",
      getEngagementById: "engagements/get",
      deleteEngagement: "engagements/remove",
    }),
    openModal() {
      this.confirmSubtitle = this.data.name
      this.confirmModal = true
    },
    async confirmRemoval() {
      await this.deleteEngagement({ id: this.$route.params.id })
      this.confirmModal = false
      this.$router.push({
        name: "Engagements",
      })
    },
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

<style lang="scss">
.re-align-delete {
  position: absolute;
  right: 35px;
  &:hover {
    cursor: pointer;
  }
}
.edit-engagement-wrap {
  height: calc(100vh - 150px) !important;
  overflow: auto;
  .container {
    height: auto !important;
    overflow: hidden !important;
  }
}
</style>
