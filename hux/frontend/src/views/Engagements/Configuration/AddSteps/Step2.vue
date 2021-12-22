<template>
  <div class="eng-step-2">
    <div class="text-body-1 mb-2">Select audience(s) and destination(s)</div>
    <data-cards
      v-show="Object.values(value.audiences).length > 0"
      bordered
      class="mr-4"
      :items="Object.values(value.audiences)"
      :fields="[
        {
          key: 'name',
          label: 'Audience name',
        },
        {
          key: 'size',
          label: 'Size',
        },
        {
          key: 'destinations',
          label: 'Destination(s)',
        },
        {
          key: 'manage',
        },
      ]"
    >
      <template #field:name="row">
        <router-link
          :to="{
            name: 'AudienceInsight',
            params: { id: row.item.id },
          }"
          class="text-decoration-none menu-link"
          append
        >
          {{ row.value }}
        </router-link>
      </template>
      <template #field:size="row">
        <tooltip>
          <template #label-content>
            {{ row.value | Numeric(true, true) | Empty }}
          </template>
          <template #hover-content>
            {{ row.value | Numeric | Empty("Size unavailable at this time") }}
          </template>
        </tooltip>
      </template>

      <template #field:destinations="row">
        <div class="destinations-wrap">
          <v-row class="align-center">
            <div>
              <tooltip v-for="destination in row.value" :key="destination.id">
                <template #label-content>
                  <div class="destination-logo-wrapper">
                    <div class="logo-wrapper">
                      <logo
                        class="added-logo ml-2 svg-icon"
                        :type="destinationType(destination.id)"
                        :size="24"
                      />
                      <logo
                        class="delete-icon"
                        type="delete"
                        @click.native="removeDestination(row, destination.id)"
                      />
                    </div>
                  </div>
                </template>
                <template #hover-content>
                  <div class="d-flex align-center">Remove</div>
                </template>
              </tooltip>
            </div>
            <div>
              <tooltip>
                <template #label-content>
                  <div
                    class="d-flex align-center ml-4 cursor-pointer"
                    data-e2e="add-destination"
                    @click="openSelectDestinationsDrawer(row.item.id)"
                  >
                    <icon type="plus" color="primary" size="12" class="mr-1" />
                    <icon type="destination" color="primary" size="24" />
                  </div>
                </template>
                <template #hover-content>Add destination(s)</template>
              </tooltip>
            </div>
          </v-row>
        </div>
      </template>

      <template #field:manage="row">
        <div class="d-flex align-center justify-end mr-2">
          <icon
            type="trash"
            class="cursor-pointer"
            :size="18"
            color="black"
            @click.native="removeAudience(row.item)"
          />
        </div>
      </template>
    </data-cards>
    <div class="add-aud-to-eng" @click="openSelectAudiencesDrawer()">
      <icon
        type="plus"
        color="primary"
        size="12"
        class="mr-2"
        data-e2e="add-audience"
      />
      <span class="primary--text">Audience</span>
    </div>

    <!-- Drawers -->
    <select-audiences-drawer
      ref="selectAudiences"
      v-model="value.audiences"
      :toggle="showSelectAudiencesDrawer"
      @onToggle="(val) => (showSelectAudiencesDrawer = val)"
      @onAdd="openAddAudiencesDrawer()"
    />

    <add-audience-drawer
      ref="addNewAudience"
      v-model="value.audiences"
      :toggle="showAddAudiencesDrawer"
      @onToggle="(val) => (showAddAudiencesDrawer = val)"
      @onCancelAndBack="openSelectAudiencesDrawer()"
    />

    <select-destinations-drawer
      ref="selectDestinations"
      v-model="value.audiences"
      :selected-audience-id="selectedAudienceId"
      :toggle="showSelectDestinationsDrawer"
      @onToggle="(val) => (showSelectDestinationsDrawer = val)"
      @onSalesforce="openDataExtensionDrawer"
    />

    <destination-data-extension-drawer
      v-model="value.audiences"
      :selected-destination="selectedDestination"
      :selected-audience-id="selectedAudienceId"
      :toggle="showDataExtensionDrawer"
      @onToggle="(val) => (showDataExtensionDrawer = val)"
      @onBack="openSelectDestinationsDrawer"
    />
  </div>
</template>

<script>
//Vuex
import { mapActions, mapGetters } from "vuex"

//Components
import DataCards from "@/components/common/DataCards.vue"
import Icon from "@/components/common/Icon.vue"
import Logo from "@/components/common/Logo.vue"
import Tooltip from "@/components/common/Tooltip.vue"

//Drawers
import AddAudienceDrawer from "@/views/Engagements/Configuration/Drawers/AddAudienceDrawer.vue"
import SelectAudiencesDrawer from "@/views/Engagements/Configuration/Drawers/SelectAudiencesDrawer.vue"
import SelectDestinationsDrawer from "@/views/Engagements/Configuration/Drawers/SelectDestinationsDrawer.vue"
import DestinationDataExtensionDrawer from "@/views/Engagements/Configuration/Drawers/DestinationDataExtensionDrawer.vue"

export default {
  name: "Step2",

  components: {
    //Components
    DataCards,
    Icon,
    Logo,
    Tooltip,
    //Drawers
    AddAudienceDrawer,
    SelectAudiencesDrawer,
    SelectDestinationsDrawer,
    DestinationDataExtensionDrawer,
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
      dontShowModal: false,
    }
  },

  computed: {
    ...mapGetters({
      destination: "destinations/single",
    }),
  },

  methods: {
    ...mapActions({
      addEngagement: "engagements/add",
    }),
    closeAllDrawers() {
      this.showSelectAudiencesDrawer = false
      this.showAddAudiencesDrawer = false
      this.showSelectDestinationsDrawer = false
      this.showDataExtensionDrawer = false
    },
    destinationType(id) {
      return this.destination(id) && this.destination(id).type
    },
    openSelectAudiencesDrawer() {
      this.closeAllDrawers()
      this.$refs.selectAudiences.fetchAudiences()
      this.showSelectAudiencesDrawer = true
    },
    openAddAudiencesDrawer() {
      this.closeAllDrawers()
      this.$refs.addNewAudience.fetchDependencies()
      this.showAddAudiencesDrawer = true
    },
    openDataExtensionDrawer(destination) {
      this.closeAllDrawers()
      this.selectedDestination = destination
      this.showDataExtensionDrawer = true
    },
    openSelectDestinationsDrawer(audienceId) {
      // set the selected audience on which we want to manage its destinations
      this.selectedAudienceId = audienceId
      this.$refs.selectDestinations.fetchDependencies()
      this.closeAllDrawers()
      this.showSelectDestinationsDrawer = true
    },
    removeAudience(audience) {
      this.$delete(this.value.audiences, audience.id)
    },
    removeDestination(deleteAudience, id) {
      const index = this.value.audiences[
        deleteAudience.item.id
      ].destinations.findIndex((destination) => destination.id === id)
      this.value.audiences[deleteAudience.item.id].destinations.splice(index, 1)
    },
  },
}
</script>

<style lang="scss" scoped>
.eng-step-2 {
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
  .add-aud-to-eng {
    display: flex;
    align-items: center;
    padding: 15px 28px;
    margin-right: 16px;
    border: 1px solid var(--v-black-lighten2) !important;
    background-color: var(--v-primary-lighten1) !important;
    border-radius: 5px;
    @extend .cursor-pointer;
  }
}
</style>
