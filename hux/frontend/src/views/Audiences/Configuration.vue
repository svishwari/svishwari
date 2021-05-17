<template>
  <div class="create-audience-wrap">
    <div class="mt-10 ml-15">
      <div class="heading font-weight-light">Add an audience</div>
      <div class="sub-heading font-weight-regular">
        Build a target Audience from the data you own. Feel free to save and
        complete later as a draft or simply create and fill in the information
        when you are ready.
      </div>

      <div class="overview mt-15">Audience overview</div>
      <div class="row overview-list mb-0 ml-0 mt-1">
        <MetricCard
          class="list-item mr-3"
          :width="135"
          :height="80"
          v-for="(item, i) in overviewListItems"
          :key="i"
          :title="item.title"
          :subtitle="item.subtitle"
          :icon="item.icon"
          :active="false"
        ></MetricCard>
      </div>
      <v-divider class="divider mt-5"></v-divider>
    </div>

    <div class="timeline-wrapper mt-9 ml-9">
      <v-timeline align-top dense class="">
        <v-timeline-item color="blue" class="timeline-section">
          <template v-slot:icon class="timeline-icon-section">
            <span>1</span>
          </template>
          <v-row class="pt-1">
            <v-col cols="4">
              <strong class="text-h6">General information</strong>
              <!-- <h3 class="text-subtitle-1">General information</h3> -->
              <TextField
                placeholderText="What is the name for this audience ?"
                labelText="Audience name"
                backgroundColor="white"
                v-bind:required="true"
                class="mt-1 text-body-1"
              ></TextField>
            </v-col>
            <v-col cols="8">
              <div class="mt-8 ml-15 text-subtitle-1">
                Attach an engagement (we can auto-create an engagement for you)
                - you must have at least one
                <div>
                  <v-icon size="30" class="add-icon" color="primary">
                    mdi-plus-circle
                  </v-icon>
                  <v-chip class="ma-2" text-color="primary">
                    audience name
                  </v-chip>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-timeline-item>
        <v-timeline-item color="blue" class="timeline-section">
          <template v-slot:icon class="timeline-icon-section">
            <span>2</span>
          </template>
          <v-row class="pt-1 pr-10 mr-10">
            <v-col cols="12">
              <strong class="text-h6"
                >Attributes selection (you can always do this later !)</strong
              >
              <v-card
                color="#F9FAFB"
                tile
                elevation="0"
                style="border: 1px solid #e2eaec"
                class="mt-2"
              >
                <v-card-actions>
                  <v-list-item class="grow">
                    <v-list-item-content>
                      <v-list-item-title class="text-subtitle-1"
                        >You have not added any attributes,
                        yet!</v-list-item-title
                      >
                    </v-list-item-content>
                    <v-row align="center" justify="end">
                      <v-icon size="30" class="add-icon" color="primary">
                        mdi-plus-circle
                      </v-icon>
                    </v-row>
                  </v-list-item>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-timeline-item>
        <v-timeline-item color="blue" class="timeline-section">
          <template v-slot:icon class="timeline-icon-section">
            <span>3</span>
          </template>
          <v-row class="pt-1">
            <v-col cols="12">
              <strong class="text-h6">
                Select a destination (you can add more than one) -optional
              </strong>
              <div>
                <v-icon
                  size="30"
                  class="add-icon"
                  color="primary"
                  @click="toggleDrawer()"
                >
                  mdi-plus-circle
                </v-icon>
                <!-- <v-btn fab x-small color="primary" @click="toggleDrawer()">
                  <v-icon dark> mdi-plus-circle </v-icon>
                </v-btn> -->
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
              <strong> Create lookalike audience </strong>
            </v-col>
          </v-row>
        </v-timeline-item>
      </v-timeline>

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
          <huxButton
            ButtonText="Save &amp; complete later"
            variant="tertiary"
            v-bind:isTile="true"
            width="201"
            height="40"
            class="ma-2"
          ></huxButton>
        </template>
        <template v-slot:right>
          <huxButton
            ButtonText="Create"
            variant="primary"
            v-bind:isTile="true"
            width="94"
            height="44"
            class="ma-2"
          ></huxButton>
        </template>
      </HuxFooter>

      <drawer v-model="drawer">

        <template v-slot:header-left>
          <div class="d-flex align-baseline" v-if="e1 == 1">
            <h5 class="text-h5 font-weight-regular pr-2">
              Select a destination to add
            </h5>
          </div>
          <div class="d-flex align-baseline" v-if="e1 == 2">
            <h5 class="text-h5 font-weight-regular pr-2 d-flex align-center">
              <Logo :type="selectedDestination.type" />
              <div class="pl-2 font-weight-regular">{{ selectedDestination.name }}</div>
            </h5>
          </div>
        </template>

        <template v-slot:default>
          <v-stepper v-model="e1">
            <v-stepper-items>
              <v-stepper-content step="1">
                <div class="ma-5">
                  <CardHorizontal
                    v-for="(destination, index) in destinations"
                    :key="destination.id"
                    :title="destination.name"
                    :icon="destination.type"
                    :isAdded="
                      destination.is_added || index == selectedDestinationIndex
                    "
                    :isAvailable="destination.is_enabled"
                    :isAlreadyAdded="destination.is_added"
                    @click="
                      onSelectDestination(index, destination)
                      e1 = 2
                    "
                    class="my-3"
                  />
                </div>
              </v-stepper-content>
              <v-stepper-content step="2">
                <AddDestination />
              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>
        </template>

        <template v-slot:footer-right>
          <div class="d-flex align-baseline" v-if="e1 == 2">
            <huxButton
              ButtonText="Add"
              variant="primary"
              v-bind:isTile="true"
              width="80"
              height="40"
              class="ma-2"
            ></huxButton>
          </div>
        </template>

        <template v-slot:footer-left>
          <div class="d-flex align-baseline" v-if="e1 == 1">
           {{ destinations.length }} results
          </div>
          <div class="d-flex align-baseline" v-if="e1 == 2">
            <huxButton
              ButtonText="Back"
              variant="white"
              v-bind:isTile="true"
              width="80"
              height="40"
              class="ma-2"
              @click.native="e1 = 1"
            ></huxButton>
          </div>
        </template>

      </drawer>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import MetricCard from "@/components/common/MetricCard"
import HuxFooter from "@/components/common/HuxFooter"
import huxButton from "@/components/common/huxButton"
import TextField from "@/components/common/TextField"
import Drawer from "@/components/common/Drawer"
import CardHorizontal from "@/components/common/CardHorizontal"
import AddDestination from "@/views/Audiences/AddDestination"
import Logo from "@/components/common/Logo"

export default {
  name: "Configuration",
  components: {
    MetricCard,
    HuxFooter,
    huxButton,
    TextField,
    Drawer,
    CardHorizontal,
    AddDestination,
    Logo,
  },
  data() {
    return {
      e1: 1,
      drawer: false,
      selectedDestinationIndex: -1,
      selectedDestination: null,
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
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/list",
    }),

    destination() {
      return this.destinations[this.selectedDestinationIndex] || null
    },

    isDestinationSelected() {
      return Boolean(this.destination)
    },
  },

  methods: {
    ...mapActions({
      getDestinations: "destinations/getAll",
    }),

    toggleDrawer() {
      this.drawer = !this.drawer
    },

    onSelectDestination(index, selected) {
      this.selectedDestinationIndex = index
      this.selectedDestination = selected
      console.log(this.selectedDestination)
    },
  },
  async mounted() {
    await this.getDestinations()
  },
}
</script>

<style lang="scss" scoped>
.create-audience-wrap {
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
    max-width: 1170px;
  }
  ::v-deep .timeline-wrapper {
    .theme--light.v-timeline:before {
      border: 1px dashed var(--v-info-base);
    }
    .theme--light.v-timeline-item {
      .v-timeline-item__divider {
        .v-timeline-item__dot {
          background: var(--v-info-base);
          .v-timeline-item__inner-dot {
            background-color: var(--v-white-base) !important;
            color: var(--v-info-base);
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
}
</style>
