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
              </template>
            </Tooltip>
          </h5>
        </template>

        <v-radio-group v-model="value.delivery_schedule" row class="ma-0">
          <v-radio value="null" selected class="btn-radio">
            <template v-slot:label>
              <v-icon small color="primary" class="mr-1">
                mdi-gesture-tap
              </v-icon>
              <span class="primary--text">Manual</span>
            </template>
          </v-radio>

          <v-radio value="scheduled" class="btn-radio" disabled>
            <template v-slot:label>
              <v-icon small class="mr-1">mdi-clock-check-outline</v-icon>
              <span>Recurring</span>
            </template>
          </v-radio>
        </v-radio-group>
      </FormStep>

      <FormStep :step="3" label="Select audience(s) and destination(s)">
        <DataCards
          bordered
          :items="Object.values(value.audiences)"
          :fields="[
            {
              key: 'name',
              label: 'Audience name',
              sortable: true,
            },
            {
              key: 'size',
              label: 'Target size',
              sortable: true,
            },
            {
              key: 'manage',
              sortable: false,
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
      <template v-slot:left>
        <v-btn tile color="white" height="40" @click.native="$router.go(-1)">
          <span class="primary--text">Cancel</span>
        </v-btn>
      </template>

      <template v-slot:right>
        <v-btn
          v-if="hasDestinations && isManualDelivery"
          tile
          color="primary"
          height="44"
          :disabled="!isValid"
          @click="deliverNewEngagement()"
        >
          Add &amp; deliver
        </v-btn>

        <v-btn
          v-else
          tile
          color="primary"
          height="44"
          :disabled="!isValid"
          @click="addNewEngagement()"
        >
          Add
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
    />
  </v-form>
</template>

<script>
import { mapActions } from "vuex"
import DataCards from "@/components/common/DataCards.vue"
import FormStep from "@/components/common/FormStep.vue"
import FormSteps from "@/components/common/FormSteps.vue"
import HuxFooter from "@/components/common/HuxFooter.vue"
import TextField from "@/components/common/TextField.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import SelectAudiencesDrawer from "./Drawers/SelectAudiencesDrawer.vue"
import AddAudienceDrawer from "./Drawers/AddAudienceDrawer.vue"

export default {
  name: "EngagementsForm",

  components: {
    DataCards,
    FormStep,
    FormSteps,
    HuxFooter,
    TextField,
    Tooltip,
    SelectAudiencesDrawer,
    AddAudienceDrawer,
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
    }
  },

  computed: {
    isValid() {
      return this.value.name.length
    },

    hasDestinations() {
      return Object.values(this.value.audiences).find((audience) => {
        return audience.destinations && audience.destinations.length
      })
    },

    isManualDelivery() {
      const MANUAL = "null"
      return this.value.delivery_schedule === MANUAL
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
    },

    openSelectAudiencesDrawer() {
      this.closeAllDrawers()
      this.showSelectAudiencesDrawer = true
    },

    openAddAudiencesDrawer() {
      this.closeAllDrawers()
      this.showAddAudiencesDrawer = true
    },

    removeAudience(audience) {
      this.$delete(this.value.audiences, audience.id)
    },

    isLastItem(index) {
      return Boolean(index === this.totalSelectedAudiences - 1)
    },

    async addNewEngagement() {
      const engagement = await this.addEngagement(this.value)
      this.$router.push({
        name: "EngagementDashboard",
        params: { id: engagement.id },
      })
    },

    async deliverNewEngagement() {
      try {
        const engagement = await this.addEngagement(this.value)
        await this.deliverEngagement(engagement.id)
        this.$router.push({
          name: "EngagementDashboard",
          params: { id: engagement.id },
        })
      } catch (error) {
        console.error(error)
      }
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
</style>
