<template>
  <v-form>
    <FormSteps>
      <FormStep :step="1" label="General information">
        <v-row>
          <v-col>
            <TextField
              v-model="value.name"
              labelText="Engagement name"
              placeholder="Give this engagement a name"
              :rules="[(value) => !!value || 'Engagement name is required']"
              required
            />
          </v-col>
          <v-col>
            <TextField
              v-model="value.description"
              labelText="Description"
              placeholder="What is the purpose of this engagement?"
            />
          </v-col>
        </v-row>
      </FormStep>

      <FormStep :step="2">
        <template slot="label">
          <h5 class="text-h5 d-flex align-start">
            Setup a delivery schedule

            <Tooltip>
              <template #label-content>
                <v-icon color="primary" :size="12" class="ml-1">
                  mdi-information-outline
                </v-icon>
              </template>
              <template #hover-content>
                <v-sheet max-width="240px">
                  <h6 class="text-caption mb-2">Manual delivery</h6>
                  <p class="gray--text">
                    Choose this option if you want the engagement delivered
                    immediately or at a future date and time.
                  </p>
                  <h6 class="text-caption mb-2">Recurring delivery</h6>
                  <p class="gray--text">
                    Choose this option if you want the engagement delivered on a
                    specific recurring basis you selected.
                  </p>
                </v-sheet>
              </template>
            </Tooltip>
          </h5>
        </template>

        <v-row>
          <v-radio-group
            v-model="value.delivery_schedule"
            row
            class="ma-0 radio-div"
          >
            <v-radio :value="0" selected class="btn-radio">
              <template #label>
                <v-icon small color="primary" class="mr-1">
                  mdi-gesture-tap
                </v-icon>
                <span class="primary--text">Manual</span>
              </template>
            </v-radio>

            <v-radio :value="1" class="btn-radio" disabled>
              <template #label>
                <v-icon small class="mr-1">mdi-clock-check-outline</v-icon>
                <span>Recurring</span>
              </template>
            </v-radio>
          </v-radio-group>
          
          <div>
            <span class="date-picker-label">Start date</span>
            <hux-start-date class="mt-n4"
              labelText="Engagement name"
              :label="selectedStartDate"
              :selected="selectedStartDate"
              @on-date-select="onStartDateSelect"
            />
          </div>

          <div>
            <span class="date-picker-label">End date</span>
            <hux-end-date class="mt-n4"
              :label="selectedEndDate"
              :selected="selectedEndDate"
              :isSubMenu="true"
              @on-date-select="onEndDateSelect"
            />
          </div>

        </v-row>
      </FormStep>

      <FormStep :step="3" label="Select audience(s) and destination(s)">
        <DataCards
          bordered
          :items="Object.values(value.audiences)"
          :fields="[
            {
              key: 'name',
              label: 'Audience name',
            },
            {
              key: 'size',
              label: 'Target size',
            },
            {
              key: 'destinations',
              label: 'Destinations',
            },
            {
              key: 'manage',
            },
          ]"
        >
          <template #field:size="row">
            <Tooltip>
              <template #label-content>
                {{ row.value | Numeric(true, true) | Empty }}
              </template>
              <template #hover-content>
                {{
                  row.value | Numeric | Empty("Size unavailable at this time")
                }}
              </template>
            </Tooltip>
          </template>

          <template #field:destinations="row">
            <div class="destinations-wrap">
              <v-row class="align-center">
                <div>
                  <Tooltip
                    v-for="destination in row.value"
                    :key="destination.id"
                  >
                    <template #label-content>
                      <div class="destination-logo-wrapper">
                        <div class="logo-wrapper">
                          <Logo
                            class="added-logo ml-2 svg-icon"
                            :type="destinationType(destination.id)"
                            :size="24"
                          />
                          <Logo
                            class="delete-icon"
                            type="delete"
                            @click.native="
                              removeDestination(row, destination.id)
                            "
                          />
                        </div>
                      </div>
                    </template>
                    <template #hover-content>
                      <div class="d-flex align-center">Remove</div>
                    </template>
                  </Tooltip>
                </div>
                <div>
                  <Tooltip>
                    <template #label-content>
                      <v-btn
                        x-small
                        fab
                        class="primary ml-2"
                        @click="openSelectDestinationsDrawer(row.item.id)"
                      >
                        <v-icon size="16">mdi-plus</v-icon>
                      </v-btn>
                    </template>
                    <template #hover-content>Add destination(s)</template>
                  </Tooltip>
                </div>
              </v-row>
            </div>
          </template>

          <template #field:manage="row">
            <div class="d-flex align-center justify-end">
              <Tooltip v-if="isLastItem(row.index)">
                <template #label-content>
                  <v-btn
                    x-small
                    fab
                    class="primary mr-2"
                    @click="openSelectAudiencesDrawer()"
                  >
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </template>
                <template #hover-content>Add another audience</template>
              </Tooltip>

              <v-btn icon color="primary" @click="removeAudience(row.item)">
                <v-icon>mdi-delete-outline</v-icon>
              </v-btn>
            </div>
          </template>

          <template slot="empty">
            <v-col class="grow">You have not added any audiences, yet.</v-col>
            <v-col class="shrink">
              <v-btn
                x-small
                fab
                color="primary"
                elevation="0"
                @click="openSelectAudiencesDrawer()"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </template>
        </DataCards>
      </FormStep>
    </FormSteps>

    <HuxFooter>
      <template #left>
        <v-btn tile color="white" height="40" @click.native="$router.go(-1)">
          <span class="primary--text">Cancel</span>
        </v-btn>
      </template>

      <template #right>
        <v-btn
          v-if="hasDestinations && isManualDelivery"
          tile
          color="primary"
          height="44"
          :disabled="!isValid"
          @click="deliverNewEngagement()"
        >
          Create &amp; deliver
        </v-btn>

        <v-btn
          v-else
          tile
          color="primary"
          height="44"
          :disabled="!isValid"
          @click="addNewEngagement()"
        >
          Create
        </v-btn>
      </template>
    </HuxFooter>

    <SelectAudiencesDrawer
      v-model="value.audiences"
      :toggle="showSelectAudiencesDrawer"
      @onToggle="(val) => (showSelectAudiencesDrawer = val)"
      @onAdd="openAddAudiencesDrawer()"
    />

    <AddAudienceDrawer
      v-model="value.audiences"
      :toggle="showAddAudiencesDrawer"
      @onToggle="(val) => (showAddAudiencesDrawer = val)"
      @onCancelAndBack="openSelectAudiencesDrawer()"
    />

    <SelectDestinationsDrawer
      v-model="value.audiences"
      :selected-audience-id="selectedAudienceId"
      :toggle="showSelectDestinationsDrawer"
      @onToggle="(val) => (showSelectDestinationsDrawer = val)"
      @onSalesforce="openDataExtensionDrawer"
    />

    <DestinationDataExtensionDrawer
      v-model="value.audiences"
      :selected-destination="selectedDestination"
      :selected-audience-id="selectedAudienceId"
      :toggle="showDataExtensionDrawer"
      @onToggle="(val) => (showDataExtensionDrawer = val)"
      @onBack="openSelectDestinationsDrawer"
    />
  </v-form>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import DataCards from "@/components/common/DataCards.vue"
import FormStep from "@/components/common/FormStep.vue"
import FormSteps from "@/components/common/FormSteps.vue"
import HuxFooter from "@/components/common/HuxFooter.vue"
import Logo from "@/components/common/Logo.vue"
import TextField from "@/components/common/TextField.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import AddAudienceDrawer from "./Drawers/AddAudienceDrawer.vue"
import SelectAudiencesDrawer from "./Drawers/SelectAudiencesDrawer.vue"
import SelectDestinationsDrawer from "./Drawers/SelectDestinationsDrawer.vue"
import DestinationDataExtensionDrawer from "./Drawers/DestinationDataExtensionDrawer.vue"
import HuxStartDate from "@/components/common/DatePicker/HuxStartDate"
import HuxEndDate from "@/components/common/DatePicker/HuxEndDate"

export default {
  name: "EngagementsForm",

  components: {
    DataCards,
    FormStep,
    FormSteps,
    Logo,
    HuxFooter,
    TextField,
    Tooltip,
    AddAudienceDrawer,
    SelectAudiencesDrawer,
    SelectDestinationsDrawer,
    DestinationDataExtensionDrawer,
    HuxStartDate,
    HuxEndDate,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      showSelectAudiencesDrawer: false,
      showAddAudiencesDrawer: false,
      showSelectDestinationsDrawer: false,
      showDataExtensionDrawer: false,
      selectedAudienceId: null,
      selectedDestination: null,
      selectedStartDate: "Select date",
      selectedEndDate: "Select date",
    }
  },

  computed: {
    ...mapGetters({
      destination: "destinations/single",
    }),

    payload() {
      return {
        name: this.value.name,
        description: this.value.description,
        delivery_schedule: this.value.delivery_schedule,
        audiences: Object.values(this.value.audiences).map((audience) => {
          return {
            id: audience.id,
            destinations: audience.destinations,
          }
        }),
        create_time: this.selectedStartDate,
        update_time: this.selectedEndDate,
      }
    },

    isValid() {
      return this.value.name.length
    },

    hasDestinations() {
      return Object.values(this.value.audiences).find((audience) => {
        return audience.destinations && audience.destinations.length
      })
    },

    isManualDelivery() {
      return this.value.delivery_schedule === 0
    },

    totalSelectedAudiences() {
      return Object.values(this.value.audiences).length
    },
  },

  methods: {
    ...mapActions({
      addEngagement: "engagements/add",
      deliverEngagement: "engagements/deliver",
    }),

    closeAllDrawers() {
      this.showSelectAudiencesDrawer = false
      this.showAddAudiencesDrawer = false
      this.showSelectDestinationsDrawer = false
      this.showDataExtensionDrawer = false
    },

    openSelectAudiencesDrawer() {
      this.closeAllDrawers()
      this.showSelectAudiencesDrawer = true
    },

    openAddAudiencesDrawer() {
      this.closeAllDrawers()
      this.showAddAudiencesDrawer = true
    },

    openSelectDestinationsDrawer(audienceId) {
      // set the selected audience on which we want to manage its destinations
      this.selectedAudienceId = audienceId
      this.closeAllDrawers()
      this.showSelectDestinationsDrawer = true
    },

    openDataExtensionDrawer(destination) {
      this.closeAllDrawers()
      this.selectedDestination = destination
      this.showDataExtensionDrawer = true
    },

    removeAudience(audience) {
      this.$delete(this.value.audiences, audience.id)
    },

    isLastItem(index) {
      return Boolean(index === this.totalSelectedAudiences - 1)
    },

    destinationType(id) {
      return this.destination(id).type
    },

    async addNewEngagement() {
      const engagement = await this.addEngagement(this.payload)
      this.$router.push({
        name: "EngagementDashboard",
        params: { id: engagement.id },
      })
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
        console.error(error)
      }
    },

    removeDestination(deleteAudience, id) {
      const index = this.value.audiences[
        deleteAudience.item.id
      ].destinations.findIndex((destination) => destination.id === id)
      this.value.audiences[deleteAudience.item.id].destinations.splice(index, 1)
    },

    onStartDateSelect(val) {
      this.selectedStartDate = val
    },
    
    onEndDateSelect(val) {
      this.selectedEndDate = val
    },
  },
}
</script>

<style lang="scss" scoped>
.btn-radio {
  border: 1px solid var(--v-primary-base);
  padding: 8px 16px;
  border-radius: 4px;

  &.v-radio--is-disabled {
    border-color: var(--v-lightGrey-base);
  }
}
.radio-div {
  margin-top: -11px !important;
}
.destinations-wrap {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-direction: row-reverse;

  .destination-logo-wrapper {
    display: inline-flex;
    .logo-wrapper {
      position: relative;
      .added-logo {
        margin-top: 8px;
      }
      .delete-icon {
        z-index: 1;
        position: absolute;
        left: 8px;
        top: 8px;
        background: var(--v-white-base);
        display: none;
      }
      &:hover {
        .delete-icon {
          display: block;
        }
      }
    }
  }
}
.date-picker-label {
  position: absolute;
  margin-top: -30px;
  margin-left: 8px;
}
</style>
