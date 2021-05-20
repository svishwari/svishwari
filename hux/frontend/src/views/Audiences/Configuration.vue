<template>
  <div class="create-audience-wrap">
    <div class="mt-10 ml-15">
      <div class="heading font-weight-light neroBlack--text">
        Add an audience
      </div>
      <div class="sub-heading font-weight-regular">
        Build a target Audience from the data you own. Feel free to save and
        complete later as a draft or simply create and fill in the information
        when you are ready.
      </div>

      <div class="overview font-weight-regular neroBlack--text mt-15">
        Audience overview
      </div>
      <div class="row overview-list mb-0 ml-0 mt-1">
        <MetricCard
          class="list-item mr-3"
          width="11.368852459016393%"
          :min-width="126.5"
          :height="80"
          v-for="(item, i) in overviewListItems"
          :key="i"
          :title="item.title"
          :subtitle="item.subtitle"
          :icon="item.icon"
          :interactable="true"
        ></MetricCard>
      </div>
      <v-divider class="divider mt-5"></v-divider>
    </div>

    <div class="timeline-wrapper mt-9 ml-9 pr-1">
      <v-form ref="form" class="mx-2 mr-0" v-model="isFormValid" lazy-validation>
        <v-timeline align-top dense class="">
          <v-timeline-item color="blue" class="timeline-section mb-7">
            <template v-slot:icon class="timeline-icon-section">
              <span>1</span>
            </template>
            <v-row class="pt-1">
              <v-col cols="4">
                <strong class="text-h5 neroBlack--text"
                  >General information</strong
                >
                <TextField
                  placeholderText="What is the name for this audience ?"
                  height="40"
                  labelText="Audience name"
                  backgroundColor="white"
                  v-bind:required="true"
                  v-model="audience.audienceName"
                  class="mt-1 aud-name-field text-caption neroBlack--text pt-2"
                  :rules="audienceNamesRules"
                ></TextField>
              </v-col>
              <v-col cols="8">
                <div class="mt-8 ml-15 text-caption neroBlack--text">
                  Add to an engagement -
                  <i style="tilt">you must have at least one</i>
                  <div>
                    <v-icon
                      size="30"
                      class="add-icon mt-1"
                      color="primary"
                      @click="
                        engagementDrawer.insideFlow = !engagementDrawer.insideFlow
                      "
                    >
                      mdi-plus-circle
                    </v-icon>
                    <v-chip
                      class="ma-2"
                      close
                      @click:close="detachEngagement(item.id)"
                      text-color="primary"
                      v-for="(item, index) in selectedEngagements"
                      :key="`engagement-${index}`"
                    >
                      {{ item.name }}
                    </v-chip>
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-timeline-item>
          <v-timeline-item color="blue" class="timeline-section mb-7">
            <template v-slot:icon class="timeline-icon-section">
              <span>2</span>
            </template>
            <v-row class="pt-1 pr-0">
              <attribute-rules :rules="attributeRules"></attribute-rules>
            </v-row>
          </v-timeline-item>
          <v-timeline-item
            color="blue"
            class="timeline-section disable-down-timeline mb-15"
          >
            <template v-slot:icon class="timeline-icon-section">
              <span>3</span>
            </template>
            <v-row class="pt-1">
              <v-col cols="12">
                <strong class="text-h5 neroBlack--text">
                  Select destination(s) -
                  <i style="font-size: 12px">Optional</i>
                </strong>
                <div>
                  <v-icon size="30" class="add-icon mt-1" color="primary">
                    mdi-plus-circle
                  </v-icon>
                </div>
              </v-col>
            </v-row>
          </v-timeline-item>
          <v-timeline-item class="timeline-section disabled">
            <template v-slot:icon class="timeline-icon-section">
              <span>4</span>
            </template>
            <v-row class="pt-1">
              <v-col cols="12">
                <strong class="text-h5"> Create lookalike audience </strong>
              </v-col>
            </v-row>
          </v-timeline-item>
        </v-timeline>
      </v-form>

      <HuxFooter>
        <template v-slot:left>
          <huxButton
            ButtonText="Cancel"
            variant="tertiary"
            v-bind:isTile="true"
            width="94"
            height="40"
            class="ma-2"
            @click.native="$router.go(-1)"
          ></huxButton>

          <!-- 
            Not required in P1 
          -->

          <!-- <huxButton
            ButtonText="Save &amp; complete later"
            variant="tertiary"
            v-bind:isTile="true"
            width="201"
            height="40"
            class="ma-2"
          ></huxButton> -->
        </template>
        <template v-slot:right>
          <huxButton
            ButtonText="Create"
            variant="primary"
            v-bind:isTile="true"
            width="94"
            height="44"
            class="ma-2"
            @click="createAudience()"
            :isDisabled="!isAudienceFormValid"
          ></huxButton>
        </template>
      </HuxFooter>
      <drawer v-model="engagementDrawer.insideFlow">
        <template v-slot:header-left>
          <div class="p-4 d-flex align-items-center">
            <v-icon>mdi-bullhorn-outline</v-icon>
            <h5 class="text-h5 font-weight-regular ml-2">
              Add to an engagement
            </h5>
          </div>
        </template>
        <template v-slot:default>
          <v-stepper v-model="engagementDrawer.viewStep">
            <v-stepper-items>
              <v-stepper-content step="1">
                <div>
                  <huxButton
                    ButtonText="New engagement"
                    icon="mdi-plus"
                    iconPosition="left"
                    variant="primary"
                    v-bind:isTile="true"
                    height="40"
                    @click="
                      resetNewEngagement()
                      engagementDrawer.viewStep = 2
                    "
                  >
                  </huxButton>
                </div>
                <div class="engagement-list-wrap">
                  <CardHorizontal
                    v-for="(engagement, index) in engagements"
                    :key="`engage-${index}`"
                    :title="engagement.name"
                    :isAdded="engagement.is_added || isSelected(engagement.id)"
                    :isAvailable="engagement.is_enabled"
                    :isAlreadyAdded="engagement.is_added"
                    @click="selectEngagement(engagement)"
                    class="my-3"
                  />
                </div>
              </v-stepper-content>
              <v-stepper-content step="2">
                <div class="new-engament-wrap">
                  <h2 class="mb-8">
                    Build a new engagement to see performance information on
                    this audience.
                  </h2>
                  <v-form ref="newEngagement" v-model="newEngagementValid">
                    <TextField
                      labelText="Engagement name"
                      placeholder="Give this engagement a name"
                      v-model="engagement.name"
                    />
                    <TextField
                      labelText="Description - <i>optional</i>"
                      placeholder="What is the purpose of this engagement?"
                      v-model="engagement.description"
                    />
                    <div class="delivery-options">
                      <span class="my-1">Delivery schedule</span>
                      <v-btn-toggle v-model="engagement.deliveryType">
                        <v-btn>
                          <v-radio
                            :off-icon="
                              engagement.deliveryType == 0
                                ? '$radioOn'
                                : '$radioOff'
                            "
                          />
                          <v-icon class="ico">mdi-gesture-tap</v-icon>
                          Manual
                        </v-btn>
                        <v-btn>
                          <v-radio
                            :off-icon="
                              engagement.deliveryType == 1
                                ? '$radioOn'
                                : '$radioOff'
                            "
                          />
                          <v-icon class="ico">mdi-clock-check-outline</v-icon>
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
          <div
            class="d-flex align-baseline"
            v-if="engagementDrawer.viewStep == 2"
          >
            <huxButton
              ButtonText="Create &amp; add"
              variant="primary"
              v-bind:isTile="true"
              height="40"
              class="ma-2"
              @click="engagementDrawer.viewStep = 1"
            ></huxButton>
          </div>
        </template>

        <template v-slot:footer-left>
          <div
            class="d-flex align-baseline"
            v-if="engagementDrawer.viewStep == 1"
          >
            {{ engagements.length }} results
          </div>
          <div
            class="d-flex align-baseline"
            v-if="engagementDrawer.viewStep == 2"
          >
            <huxButton
              ButtonText="Cancel &amp; back"
              variant="white"
              v-bind:isTile="true"
              height="40"
              class="ma-2"
              @click.native="engagementDrawer.viewStep = 1"
            ></huxButton>
          </div>
        </template>
      </drawer>
    </div>
  </div>
</template>

<script>
import MetricCard from "@/components/common/MetricCard"
import HuxFooter from "@/components/common/HuxFooter"
import huxButton from "@/components/common/huxButton"
import TextField from "@/components/common/TextField"
import AttributeRules from "./AttributeRules.vue"
import Drawer from "@/components/common/Drawer.vue"
import HuxButton from "../../components/common/huxButton.vue"
import CardHorizontal from "../../components/common/CardHorizontal.vue"
import { mapGetters, mapActions } from "vuex"

export default {
  name: "Configuration",
  components: {
    MetricCard,
    HuxFooter,
    huxButton,
    TextField,
    AttributeRules,
    Drawer,
    HuxButton,
    CardHorizontal,
  },
  data() {
    return {
      overviewListItems: [
        { title: "Target size", subtitle: "34,203,204" },
        { title: "Countries", subtitle: "2", icon: "mdi-earth" },
        { title: "US States", subtitle: "52", icon: "mdi-map" },
        { title: "Cities", subtitle: "19,495", icon: "mdi-map-marker-radius" },
        { title: "Age", subtitle: "-", icon: "mdi-cake-variant" },
        { title: "Women", subtitle: "52%", icon: "mdi-gender-female" },
        { title: "Men", subtitle: "46%", icon: "mdi-gender-male" },
        { title: "Other", subtitle: "2%", icon: "mdi-gender-male-female" },
      ],

      engagementDrawer: {
        insideFlow: false,
        viewStep: 1,
      },
      audience: {
        name: null,
        engagements: [],
        attributeRules: [],
        destinations: [],
      },
      selectedEngagements: [],
      newEngagementValid: true,
      engagement: {
        name: "",
        description: "",
        deliveryType: 0,
      },
      audienceNamesRules: [(v) => !!v || "Audience name is required"],
      isFormValid: false,
    }
  },
  computed: {
    ...mapGetters({
      engagements: "engagements/list",
    }),
    attributeRules() {
      return this.audience ? this.audience.attributeRules : []
    },
    isEngagementSelected() {
      return this.selectedEngagements.length > 0
    },
    isAudienceFormValid() {
      return !!this.audience.audienceName && this.selectedEngagements.length > 0
    },
  },
  methods: {
    ...mapActions({
      fetchEngagements: "engagements/getAll",
    }),

    selectEngagement(engagement) {
      const filtered = [...this.selectedEngagements]
      const existingIndex = filtered.findIndex(
        (eng) => eng.id === engagement.id
      )
      if (existingIndex > -1) filtered.splice(existingIndex, 1)
      else filtered.push(engagement)
      this.selectedEngagements = filtered
    },
    resetNewEngagement() {
      this.$refs.newEngagement.reset()
      this.engagement.deliveryType = 0
    },
    isSelected(id) {
      return this.selectedEngagements.filter((eng) => eng.id === id).length > 0
    },
    detachEngagement(id) {
      const existingIndex = this.selectedEngagements.findIndex(
        (eng) => eng.id === id
      )
      if (existingIndex > -1) this.selectedEngagements.splice(existingIndex, 1)
    },
    createAudience() {},
  },
  async mounted() {
    await this.fetchEngagements()
  },
}
</script>

<style lang="scss" scoped>
.create-audience-wrap {
  padding-right: 60px;
  .heading {
    font-size: 24px;
    line-height: 40px;
  }
  .sub-heading {
    font-size: 14px;
    line-height: 22px;
    max-width: 910px;
  }
  .overview {
    font-size: 15px;
    line-height: 20px;
  }
  .divider {
    width: 100%;
  }
  ::v-deep .timeline-wrapper {
    max-width: 1230px;
    padding-right: 30px;
    .theme--light.v-timeline {
      padding-top: 0px;
      .theme--light.v-timeline-item:last-child {
        padding-bottom: 0px;
      }
      .theme--light.v-timeline-item.disabled {
        .v-timeline-item__divider {
          .v-timeline-item__dot {
            background: var(--v-lightGrey-base);
            .v-timeline-item__inner-dot {
              background-color: var(--v-white-base) !important;
              color: var(--v-lightGrey-base);
              height: 34.2px;
              margin: 2.1px;
              width: 34.2px;
            }
          }
        }
      }
    }
    .theme--light.v-timeline:before {
      background: linear-gradient(
          to right,
          var(--v-skyBlueDark-base) 50%,
          rgba(255, 255, 255, 0) 0%
        ),
        linear-gradient(
          var(--v-skyBlueDark-base) 50%,
          rgba(255, 255, 255, 0) 0%
        ),
        linear-gradient(
          to right,
          var(--v-skyBlueDark-base) 49%,
          rgba(255, 255, 255, 0) 0%
        ),
        linear-gradient(
          var(--v-skyBlueDark-base) 50%,
          rgba(255, 255, 255, 0) 0%
        );
      background-position: top, right, bottom, left;
      background-repeat: repeat-x, repeat-y;
      background-size: 12px 0px, 1px 12px;
    }
    .aud-name-field {
      .v-input__control {
        .v-input__slot {
          min-height: 40px;
          .v-text-field__slot {
            .v-label {
              top: 9px;
            }
          }
          fieldset {
            color: #D0D0CE
          }
        }
      }
    }
    .theme--light.v-timeline-item {
      .v-timeline-item__divider {
        .v-timeline-item__dot {
          background: var(--v-info-base);
          .v-timeline-item__inner-dot {
            background-color: var(--v-white-base) !important;
            color: var(--v-info-base);
            height: 34.2px;
            margin: 2.1px;
            width: 34.2px;
          }
        }
      }
    }
    .theme--light.v-timeline-item {
      &.disabled {
        .v-timeline-item__body {
          color: var(--v-lightGrey-base);
        }
        .v-timeline-item__divider {
          .v-timeline-item__dot {
            color: var(--v-lightGrey-base);
            .v-timeline-item__inner-dot {
              background-color: var(--v-white-base) !important;
              color: var(--v-lightGrey-base);
            }
          }
        }
      }
    }
  }
  .v-stepper {
    box-shadow: none;
  }
  .new-engament-wrap {
    h2 {
      font-weight: normal;
      font-size: 14px;
      line-height: 22px;
      color: var(--v-neroBlack-base);
    }
    ::v-deep label {
      font-weight: normal;
      font-size: 12px;
      line-height: 16px;
      color: var(--v-neroBlack-base);
    }
    .delivery-options {
      display: flex;
      flex-direction: column;
      ::v-deep button {
        background: var(--v-tertiary-base);
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
              color: var(--v-skyBlueDark-base) !important;
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
}
</style>
