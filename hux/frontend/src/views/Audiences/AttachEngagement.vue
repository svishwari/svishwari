<template>
  <Drawer v-model="localDrawer" @onClose="goToStep1()">
    <template v-slot:header-left>
      <div class="d-flex align-center">
        <Icon
          v-if="viewStep == '1'"
          type="engagements"
          :size="18"
          color="neroBlack"
        />
        <h3 v-if="viewStep == '1'" class="text-h3 ml-2 neroBlack--text">
          Add to an engagement
        </h3>
        <h3 v-else class="text-h3 ml-2 neroBlack--text">
          Add a new engagement
        </h3>
      </div>
    </template>
    <template v-slot:default>
      <v-progress-linear
        color="primary"
        :active="loading"
        :indeterminate="loading"
      />
      <v-stepper v-if="!loading" v-model="viewStep">
        <v-stepper-items>
          <v-stepper-content step="1">
            <div v-if="!areEngagementAlreadyCreated">
              <EmptyPage>
                <template v-slot:icon>mdi-alert-circle-outline</template>
                <template v-slot:title>Oops! There’s nothing here yet</template>
                <template v-slot:subtitle>
                  No engagements has been launched yet. Let’s create one <br />
                  by clicking the new engagement button below.
                </template>
                <template v-slot:button>
                  <huxButton
                    ButtonText="New engagement"
                    icon="mdi-plus"
                    iconPosition="left"
                    variant="primary"
                    size="small"
                    :isTile="true"
                    @click="goToStep2()"
                    class="ma-2"
                  ></huxButton>
                </template>
              </EmptyPage>
            </div>
            <div class="ma-1" v-else>
              <h6 class="mb-6 text-h6 neroBlack--text">
                Select an existing engagement or create a new one. You are
                required to have at least one selected.
              </h6>
              <huxButton
                ButtonText="New engagement"
                icon="mdi-plus"
                iconPosition="left"
                variant="primary"
                :isTile="true"
                height="40"
                @click="goToAddNewEngagement()"
              ></huxButton>
              <div class="engagement-list-wrap mt-6">
                <div>
                  <span class="text-caption">Engagement name</span>
                  <v-icon
                    :class="{ 'rotate-icon-180': toggleSortIcon }"
                    class="ml-1"
                    color="secondary"
                    size="12"
                    @click="onSortIconClick()"
                  >
                    mdi-arrow-down
                  </v-icon>
                </div>
                <CardHorizontal
                  v-for="engagement in engagements"
                  :key="engagement.id"
                  :isAdded="isEngagementSelected(engagement)"
                  :enableBlueBackground="isEngagementSelected(engagement)"
                  @click="onEngagementClick(engagement)"
                  class="my-3"
                >
                  <v-menu open-on-hover offset-x offset-y :max-width="177">
                    <template v-slot:activator="{ on }">
                      <div v-on="on" class="pl-2 font-weight-regular">
                        {{ engagement.name }}
                      </div>
                    </template>
                    <template v-slot:default>
                      <div class="px-4 py-2 white">
                        <div class="neroBlack--text text-caption">Name</div>
                        <div class="lightGreyText--text text-caption mt-1">
                          {{ engagement.name }}
                        </div>
                        <div class="neroBlack--text text-caption mt-3">
                          Description
                        </div>
                        <div class="lightGreyText--text text-caption mt-1">
                          {{ engagement.description }}
                        </div>
                      </div>
                    </template>
                  </v-menu>
                </CardHorizontal>
              </div>
            </div>
          </v-stepper-content>
          <v-stepper-content step="2">
            <div class="new-engament-wrap">
              <h6 class="mb-8 text-h6 neroBlack--text">
                Build a new engagement to see performance information on this
                audience.
              </h6>
              <v-form ref="newEngagementRef" v-model="newEngagementValid">
                <TextField
                  labelText="Engagement name"
                  placeholder="Give this engagement a name"
                  v-model="newEngagement.name"
                  :required="true"
                  :rules="newEngagementRules"
                />
                <TextField
                  labelText="Description - <i>optional</i>"
                  placeholder="What is the purpose of this engagement?"
                  v-model="newEngagement.description"
                />
                <div class="mb-2">
                  Delivery schedule
                  <v-menu max-width="184" open-on-hover offset-y>
                    <template v-slot:activator="{ on }">
                      <v-icon
                        v-on="on"
                        color="secondary"
                        :size="12"
                        class="ml-1"
                      >
                        mdi-information-outline
                      </v-icon>
                    </template>
                    <template v-slot:default>
                      <div class="px-4 py-2 white">
                        <div class="neroBlack--text text-caption">
                          Manual delivery
                        </div>
                        <div class="gray--text text-caption mt-1">
                          Choose this option if you want the engagement
                          delivered immediately or at a future date and time.
                        </div>
                        <div class="neroBlack--text text-caption mt-3">
                          Recurring delivery
                        </div>
                        <div class="gray--text text-caption mt-1">
                          Choose this option if you want the engagement
                          delivered on a specific recurring basis you selected.
                        </div>
                      </div>
                    </template>
                  </v-menu>
                </div>
                <div class="d-flex flex-column delivery-options">
                  <v-btn-toggle
                    v-model="newEngagement.delivery_schedule"
                    mandatory
                  >
                    <v-btn>
                      <v-radio
                        :off-icon="
                          newEngagement.delivery_schedule == 0
                            ? '$radioOn'
                            : '$radioOff'
                        "
                      />
                      <v-icon class="ico">mdi-gesture-tap</v-icon>Manual
                    </v-btn>
                    <v-btn disabled style="background: white !important">
                      <v-radio
                        :off-icon="
                          newEngagement.delivery_schedule == 1
                            ? '$radioOn'
                            : '$radioOff'
                        "
                      />
                      <v-icon class="ico"> mdi-clock-check-outline </v-icon>
                      Recurring
                    </v-btn>
                  </v-btn-toggle>
                </div>
              </v-form>
            </div>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </template>
    <template v-slot:footer-right>
      <div class="d-flex align-baseline" v-if="viewStep == 2">
        <huxButton
          ButtonText="Create &amp; add"
          variant="primary"
          :isTile="true"
          height="40"
          :isDisabled="!newEngagementValid"
          @click.native="addEngagement()"
        />
      </div>
    </template>

    <template v-slot:footer-left>
      <div
        class="d-flex align-baseline"
        v-if="viewStep == 1 && areEngagementAlreadyCreated"
      >
        {{ engagements.length }} results
      </div>
      <div class="d-flex align-baseline" v-if="viewStep == 2">
        <huxButton
          ButtonText="Cancel &amp; back"
          variant="white"
          :isTile="true"
          height="40"
          @click.native="goToStep1()"
        ></huxButton>
      </div>
    </template>
  </Drawer>
</template>

<script>
import { mapActions } from "vuex"

import huxButton from "@/components/common/huxButton"
import TextField from "@/components/common/TextField"
import EmptyPage from "@/components/common/EmptyPage"
import Drawer from "@/components/common/Drawer"
import CardHorizontal from "@/components/common/CardHorizontal"
import Icon from "@/components/common/Icon"

import sortBy from "lodash/sortBy"

export default {
  name: "attach-engagement",

  components: {
    Drawer,
    huxButton,
    TextField,
    CardHorizontal,
    EmptyPage,
    Icon,
  },

  computed: {
    areEngagementAlreadyCreated() {
      return this.engagements.length > 0
    },
  },

  data() {
    return {
      localDrawer: this.value,
      toggleSortIcon: false,
      engagements: [],
      loading: false,
      viewStep: 1,
      selectedEngagements: [],
      newEngagement: {
        name: "",
        description: "",
        delivery_schedule: 0,
      },
      newEngagementValid: false,
      newEngagementRules: [(v) => !!v || "Engagement name is required"],
      sortBy: sortBy,
    }
  },

  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
    finalEngagements: {
      type: Array,
      required: true,
      default: () => [],
    },
  },

  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
      if (!this.localDrawer) {
        this.$emit("onClose")
      }
    },
    finalEngagements: function (newVal) {
      this.selectedEngagements = newVal
    },
  },

  methods: {
    ...mapActions({
      fetchEngagements: "engagements/getAll",
      addEngagementToDB: "engagements/add",
    }),
    isEngagementSelected: function (engagement) {
      return this.selectedEngagements.includes(engagement)
    },
    goToAddNewEngagement: function () {
      this.resetNewEngagement()
      this.goToStep2()
    },
    resetNewEngagement: function () {
      this.$refs.newEngagementRef.reset()
      this.newEngagement.delivery_schedule = 0
    },
    goToStep1: function () {
      this.viewStep = 1
    },
    goToStep2: function () {
      this.viewStep = 2
    },
    addEngagement: async function () {
      this.loading = true
      if (this.newEngagement.delivery_schedule == 0) {
        this.newEngagement.delivery_schedule = null
      } else {
        this.newEngagement.delivery_schedule = {
          end_date: "",
          start_date: "",
        }
      }
      let newEngagement = await this.addEngagementToDB(this.newEngagement)
      this.engagements.push(newEngagement)
      this.sortEngagements()
      this.onEngagementClick(newEngagement)
      this.goToStep1()
      this.loading = false
    },
    onEngagementClick: function (engagement) {
      if (this.selectedEngagements.includes(engagement)) {
        if (this.selectedEngagements.length !== 1) {
          const deselectedId = this.selectedEngagements.indexOf(engagement)

          this.selectedEngagements.splice(deselectedId, 1)
          this.$emit("onEngagementChange", this.selectedEngagements)
        }
      } else {
        this.selectedEngagements.push(engagement)
        this.$emit("onEngagementChange", this.selectedEngagements)
      }
    },
    sortEngagements: function () {
      if (this.toggleSortIcon) {
        this.engagements = this.sortBy(this.engagements, ["name"])
      } else {
        this.engagements = this.sortBy(this.engagements, ["name"]).reverse()
      }
    },
    toggleSort: function () {
      this.toggleSortIcon = !this.toggleSortIcon
    },
    onSortIconClick: function () {
      this.toggleSort()
      this.sortEngagements()
    },
  },
  async mounted() {
    this.loading = true
    await this.fetchEngagements()
    this.engagements = JSON.parse(
      JSON.stringify(this.$store.getters["engagements/list"])
    )
    this.sortEngagements()
    this.loading = false
  },
}
</script>

<style lang="scss" scoped>
.v-stepper {
  box-shadow: none;
}
.new-engament-wrap {
  .delivery-options {
    ::v-deep button {
      background: var(--v-white-base);
      border: 1px solid var(--v-lightGrey-base);
      box-sizing: border-box;
      border-radius: 4px;
      border-left-width: 1px !important;
      width: 175px;
      height: 40px;
      padding: 10px;
      margin-right: 10px;
      color: var(--v-lightGrey-base);
      .v-icon {
        &.ico {
          width: 13.44px;
          height: 12.5px;
          margin-right: 9px;
        }
      }
      .v-btn__content {
        justify-content: start;
      }
      .theme--light {
        color: var(--v-lightGrey-base) !important;
      }
      &.v-btn--active {
        border: 1px solid var(--v-primary-base) !important;
        color: var(--v-primary-base) !important;
        .v-icon {
          &.ico {
            width: 13.44px;
            height: 12.5px;
            color: var(--v-secondary-base) !important;
            margin-right: 9px;
          }
        }
        .theme--light {
          color: var(--v-primary-base) !important;
        }
      }
    }
  }
}
</style>
