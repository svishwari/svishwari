<template>
  <drawer v-model="localToggle" content-padding="pa-0 mapping-drawer">
    <template #header-left>
      <div class="d-flex align-center">
        <h3 class="text-h3 black--text text--darken-4">Map Facebook Campaign</h3>
      </div>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />
      <div class="py-5 px-6">
        <span class="text-caption black--text text--darken-4">
          To see KPI’s for Facebook, map to a Facebook campaign and select a
          delivery time.
        </span>
        <data-cards
          v-if="!loading"
          bordered
          empty="No campaigns available to map to a delivery moment."
          :items="mappings"
          :fields="[
            {
              key: 'campaign',
              label: 'Facebook campaign',
              col: 5,
            },
            {
              key: 'delivery_job',
              label: 'Delivery moment',
              col: 5,
            },
            {
              key: 'manage',
              col: 2,
            },
          ]"
          class="pt-11 campaigns-wrapper"
        >
          <template #field:campaign="row">
            <hux-dropdown
              :selected="row.value"
              :items="availableCampaignsOptions()"
              @on-select="onSelectedItem(row, $event, 'campaign')"
            >
            </hux-dropdown>
          </template>
          <template #field:delivery_job="row">
            <hux-dropdown
              :selected="row.value"
              :items="deliveryOptions"
              @on-select="onSelectedItem(row, $event, 'delivery_job')"
            >
            </hux-dropdown>
          </template>
          <template #field:manage="row">
            <div class="d-flex align-center justify-end">
              <tooltip v-if="canAddNewMapping(row.index)">
                <template #label-content>
                  <v-btn
                    v-if="availableCampaignsOptions().length > 0"
                    x-small
                    fab
                    class="primary mr-0"
                    height="21"
                    width="21"
                    @click="addNewMappingItem()"
                  >
                    <v-icon size="14">mdi-plus</v-icon>
                  </v-btn>
                </template>
                <template #hover-content>Add another mapping</template>
              </tooltip>

              <v-btn
                v-if="canDeleteMapping(row.index)"
                icon
                color="primary"
                height="21"
                @click="removeMapping(row.index)"
              >
                <v-icon>mdi-delete-outline</v-icon>
              </v-btn>
            </div>
          </template>
        </data-cards>
      </div>
    </template>
    <template #footer-left>
      <v-btn tile color="white" @click="closeDrawer">
        <span class="primary--text">Cancel</span>
      </v-btn>
      <v-btn tile color="primary" :disabled="!canMapNow" @click="mapSelections">
        Map selection
      </v-btn>
    </template>
  </drawer>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Drawer from "@/components/common/Drawer.vue"
import DataCards from "../../../../components/common/DataCards.vue"
import HuxDropdown from "../../../../components/common/HuxDropdown.vue"
import Tooltip from "../../../../components/common/Tooltip.vue"

export default {
  name: "CampaignMapDrawer",
  components: { Drawer, DataCards, HuxDropdown, Tooltip },
  props: {
    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      localToggle: false,
      loading: false,
      campaigns: [],
      emptyCampaign: {
        campaign: null,
        delivery_job: null,
      },
      identityAttrs: {},
    }
  },
  computed: {
    ...mapGetters({
      campaignMappingOptions: "engagements/campaignMappingOptions",
      campaignMapping: "engagements/campaignMapping",
    }),
    campaignOptions() {
      if (
        this.campaignMappingOptions &&
        this.campaignMappingOptions.campaigns
      ) {
        return this.campaignMappingOptions.campaigns
      }
      return []
    },
    mappings() {
      return JSON.stringify(this.campaignMappingOptions) === "{}"
        ? []
        : this.campaigns.map((camp) => {
            return camp["id"]
              ? {
                  campaign: this.campaignMappingOptions.campaigns.filter(
                    (camOpt) => camOpt.id === camp.id
                  )[0],
                  delivery_job:
                    this.campaignMappingOptions.delivery_jobs.filter(
                      (camOpt) => camOpt.id === camp.delivery_job_id
                    )[0],
                }
              : camp
          })
    },
    canMapNow() {
      return this.mappings.length > 0
        ? this.mappings.every((camp) => camp.campaign && camp.delivery_job)
        : false
    },
    deliveryOptions() {
      return this.campaignMappingOptions.delivery_jobs
    },
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },
  },
  methods: {
    ...mapActions({
      getCampaignMappingsOptions: "engagements/fetchCampaignMappings",
      getCampaigns: "engagements/getCampaigns",
    }),
    reset() {
      this.campaigns = [
        {
          campaign: null,
          delivery_job: null,
        },
      ]
    },
    closeDrawer() {
      this.localToggle = false
      this.reset()
    },
    addNewMappingItem() {
      this.campaigns.push(JSON.parse(JSON.stringify(this.emptyCampaign)))
    },
    removeMapping(index) {
      this.campaigns.splice(index, 1)
    },
    canAddNewMapping(index) {
      return this.campaigns.length - 1 === index
    },
    canDeleteMapping() {
      return this.campaigns.length > 1
    },
    onSelectedItem(item, value, type) {
      item.item[type] = value
    },
    mapSelections() {
      this.localToggle = false
      this.$emit("onCampaignMappings", {
        mappings: this.mappings,
        attrs: this.identityAttrs,
      })
    },
    availableCampaignsOptions() {
      const selectedCampaigns = this.mappings.map(
        (camp) => camp.campaign && camp.campaign.name
      )
      return this.campaignOptions.filter(
        (option) => !selectedCampaigns.includes(option.name)
      )
    },
    async loadCampaignMappings(attrs) {
      this.reset()
      this.identityAttrs = attrs
      try {
        this.loading = true
        await this.getCampaignMappingsOptions(attrs)
        await this.getCampaigns(attrs)
        const campaigns = await this.campaignMapping(attrs.destinationId)
        this.campaigns =
          campaigns.length > 0
            ? campaigns
            : [JSON.parse(JSON.stringify(this.emptyCampaign))]
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.mapping-drawer {
  .campaigns-wrapper {
    ::v-deep .v-data-iterator {
      .data-card-headers {
        .col {
          &:not(:first-child) {
            .px-4 {
              padding-left: 0px !important;
            }
          }
        }
      }
      .data-card {
        margin-top: 0px !important;
        .col {
          .hux-dropdown {
            width: 100% !important;
            button {
              margin: 0 !important;
            }
          }
          &:nth-child(1) {
            .pa-4 {
              padding: 14px 0px 14px 16px !important;
            }
          }

          &:nth-child(2) {
            .pa-4 {
              padding: 14px 0px 14px 0px !important;
            }
          }
        }
      }
    }
  }
}
</style>
