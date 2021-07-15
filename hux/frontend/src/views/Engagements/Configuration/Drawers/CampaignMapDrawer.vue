<template>
  <drawer v-model="localToggle" content-padding="pa-0 mapping-drawer">
    <template #header-left>
      <div class="d-flex align-center">
        <h3 class="text-h3">Map Facebook Campaign</h3>
      </div>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />
      <div class="py-5 px-6">
        <span class="text-caption">
          To see KPI’s for Facebook, map to a Facebook campaign and select a
          delivery time.
        </span>
        <data-cards
          bordered
          :items="Object.values(campaigns)"
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
          class="pt-13 campaigns-wrapper"
          v-if="!loading"
        >
          <template #field:campaign="row">
            <hux-dropdown
              :selected="row.value"
              :items="avaialableCampaignsOptions()"
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
                    x-small
                    fab
                    class="primary mr-0"
                    height="21"
                    width="21"
                    @click="addNewMappingItem()"
                    v-if="avaialableCampaignsOptions().length > 0"
                  >
                    <v-icon size="14">mdi-plus</v-icon>
                  </v-btn>
                </template>
                <template #hover-content>Add another mapping</template>
              </tooltip>

              <v-btn
                icon
                color="primary"
                v-if="canDeleteMapping(row.index)"
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
      <v-btn tile color="primary" @click="mapSelections" :disabled="!canMapNow">
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
      campaigns: {
        0: {
          campaign: null,
          delivery_job: null,
        },
      },
      identityAttrs: {},
    }
  },
  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },
  },
  computed: {
    ...mapGetters({
      campaignMappings: "engagements/destinationCampaignMappings",
    }),
    campaignOptions() {
      if (this.campaignMappings && this.campaignMappings.campaigns) {
        return this.campaignMappings.campaigns
      }
      return []
    },
    canMapNow() {
      return Object.keys(this.campaigns).every(
        (key) =>
          this.campaigns[key].campaign && this.campaigns[key].delivery_job
      )
    },
    deliveryOptions() {
      return this.campaignMappings.delivery_jobs
    },
  },
  methods: {
    ...mapActions({
      getCampaignMappingsOptions: "engagements/fetchCampaignMappings",
      getCampaigns: "engagements/getCampaigns",
    }),

    closeDrawer() {
      this.localToggle = false
      this.campaigns = {
        0: {
          campaign: null,
          delivery_job: null,
        },
      }
    },
    addNewMappingItem() {
      const key = new Date().getTime().toString()
      this.$set(this.campaigns, key, {
        campaign: null,
        delivery_job: null,
      })
    },
    removeMapping(index) {
      this.$delete(this.campaigns, Object.keys(this.campaigns)[index])
    },
    canAddNewMapping(index) {
      return Object.values(this.campaigns).length - 1 === index
    },
    canDeleteMapping() {
      return Object.values(this.campaigns).length > 1
    },
    onSelectedItem(item, value, type) {
      item.item[type] = value
    },
    mapSelections() {
      this.localToggle = false
      this.$emit("onCampaignMappings", {
        mappings: this.campaigns,
        attrs: this.identityAttrs,
      })
    },
    avaialableCampaignsOptions() {
      const selectedCampaigns = Object.keys(this.campaigns).map(
        (key) =>
          (this.campaigns[key].campaign && this.campaigns[key].campaign.name) ||
          ""
      )
      return this.campaignOptions.filter(
        (option) => !selectedCampaigns.includes(option.name)
      )
    },
    onCancelAndBack() {
      this.$emit("onCancelAndBack")
      this.reset()
    },
    async loadCampaignMappings(attrs) {
      this.identityAttrs = attrs
      this.loading = true
      await this.getCampaigns(attrs)
      await this.getCampaignMappingsOptions(attrs)
      this.loading = false
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
