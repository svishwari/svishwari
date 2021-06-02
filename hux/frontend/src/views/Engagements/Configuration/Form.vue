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
              :required="true"
              :rules="[(value) => !!value || 'Engagement name is required']"
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

            <v-menu max-width="16rem" offset-x offset-y top>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on" color="primary" :size="12">
                  mdi-information-outline
                </v-icon>
              </template>
              <div class="pa-4 white text-caption">
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
              </div>
            </v-menu>
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
        <div v-if="Object.values(value.audiences).length">
          <v-card
            v-for="item in Object.values(value.audiences)"
            :key="item.id"
            elevation="3"
            class="bordered-card pa-5 mb-4"
          >
            <v-row align="center">
              <v-col class="grow">
                {{ item.name }}
              </v-col>
              <v-col class="grow">
                {{ item.size | Numeric(true, true) }}
              </v-col>
              <v-col class="shrink pa-0">
                <div class="d-flex align-center">
                  <v-btn
                    x-small
                    fab
                    class="primary mr-2"
                    @click="toggleAudiencesDrawer()"
                  >
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                  <v-btn icon color="primary" @click="removeAudience(item)">
                    <v-icon>mdi-delete-outline</v-icon>
                  </v-btn>
                </div>
              </v-col>
            </v-row>
          </v-card>
        </div>
        <v-alert v-else color="background" class="border">
          <v-row align="center">
            <v-col class="grow">You have not added any audiences, yet.</v-col>
            <v-col class="shrink">
              <v-btn
                x-small
                fab
                color="primary"
                elevation="0"
                @click="toggleAudiencesDrawer()"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-alert>
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

    <AudiencesDrawer v-model="value.audiences" :toggle="showAudiencesDrawer" />
  </v-form>
</template>

<script>
import { mapActions } from "vuex"
import HuxFooter from "@/components/common/HuxFooter.vue"
import FormSteps from "@/components/common/FormSteps.vue"
import FormStep from "@/components/common/FormStep.vue"
import TextField from "@/components/common/TextField.vue"
import AudiencesDrawer from "@/views/Audiences/Drawer.vue"

export default {
  name: "EngagementsForm",

  components: {
    HuxFooter,
    TextField,
    FormSteps,
    FormStep,
    AudiencesDrawer,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      showAudiencesDrawer: false,
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
  },

  methods: {
    ...mapActions({
      addEngagement: "engagements/add",
      deliverEngagement: "engagements/deliver",
    }),

    toggleAudiencesDrawer() {
      this.showAudiencesDrawer = !this.showAudiencesDrawer
    },

    removeAudience(audience) {
      this.$delete(this.value.audiences, audience.id)
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

.border {
  border: 1px solid var(--v-zircon-base) !important;
}

.bordered-card {
  border-left: 10px solid var(--v-aliceBlue-base);
}
</style>
