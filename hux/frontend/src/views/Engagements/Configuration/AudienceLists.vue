<template>
  <div>
    <v-card class="rounded-lg card-style audiences-lists ml-7" flat width="451">
      <v-card-title class="d-flex justify-space-between">
        <div class="d-flex align-center">
          <icon
            type="audiences"
            :size="21"
            class="mr-1"
            color="black"
            variant="base"
          />
          <span class="text-h3">Audiences</span>
        </div>
      </v-card-title>
      <hux-data-table
        :columns="columnDefs"
        :data-items="audienceLists"
        disable-sort
      >
        <template #row-item="{ item }">
          <td v-for="header in columnDefs" :key="header.value">
            <div class="black--text text-body-1" v-if="header.value == 'name'">
              <tooltip>
                <template slot="label-content">
                  <span class="ellipsis">
                    {{ item[1].name }}
                  </span>
                </template>
                <template slot="hover-content">
                  {{ item[1].name }}
                </template>
              </tooltip>
            </div>
            <div class="black--text text-body-1" v-if="header.value == 'size'">
              <size :value="item[1].size" />
            </div>
            <div
              v-if="header.value == 'destinations'"
              class="d-flex align-center"
            >
              <div class="d-flex align-center destination-ico">
                <tooltip
                  v-for="destination in getOverallDestinations(
                    item[1].destinations
                  )"
                  :key="destination.id"
                >
                  <template #label-content>
                    <logo class="mr-1" :type="destination.type" :size="18" />
                  </template>
                  <template #hover-content>
                    <span>{{ destination.type }}</span>
                  </template>
                </tooltip>
              </div>
              <span v-if="item[1].destinations.length > 3" class="ml-1">
                <tooltip>
                  <template #label-content>
                    + {{ item[1].destinations.length - 3 }}
                  </template>
                  <template #hover-content>
                    <div class="d-flex flex-column">
                      <div
                        v-for="extraDestination in getExtraDestinations(
                          item[1].destinations
                        )"
                        :key="extraDestination.id"
                        class="d-flex align-center py-2"
                      >
                        <logo
                          :key="extraDestination.id"
                          class="mr-4"
                          :type="extraDestination.type"
                          :size="18"
                        />
                        <span>{{ extraDestination.type }}</span>
                      </div>
                    </div>
                  </template>
                </tooltip>
              </span>
              <span v-else-if="item[1].destinations.length == 0">—</span>
            </div>
          </td>
        </template>
      </hux-data-table>
    </v-card>
    <div class="info-widget d-flex mt-2 ml-7 pa-3">
      <div class="bulb">
        <icon type="FAB-bulb" :size="18" class="mt-1"/>
      </div>
      <div class="description ml-4">
        The lookalike audience will not be created in it's associated
        destination until the original audience is delivered. That delivery will
        trigger the lookalike creation.
      </div>
    </div>
  </div>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Size from "@/components/common/huxTable/Size.vue"
import Icon from "@/components/common/Icon.vue"
import Logo from "@/components/common/Logo.vue"
import HuxIcon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip"

export default {
  name: "StandaloneDelivery",
  components: {
    HuxDataTable,
    Size,
    Icon,
    Logo,
    HuxIcon,
    Tooltip,
  },
  props: {
    value: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      selection: null,
      columnDefs: [
        {
          text: "Audience name",
          value: "name",
          width: "200px",
        },
        {
          text: "Size",
          value: "size",
          width: "133px",
        },
        {
          text: "Destination(s)",
          value: "destinations",
          width: "117px",
        },
      ],
      deliveries: [],
    }
  },
  computed: {
    audienceLists() {
      return [...Object.entries(this.value.audiences)]
    },
  },
  methods: {
    getOverallDestinations(engagementDestinations) {
      let destinations = [...engagementDestinations]
      if (destinations.length > 3) {
        return destinations.slice(0, 3)
      }
      return destinations
    },
    getExtraDestinations(engagementDestinations) {
      let destinations = [...engagementDestinations]
      if (destinations.length > 3) {
        return destinations.slice(3)
      }
      return destinations
    },
  },
}
</script>

<style lang="scss" scoped>
.audiences-lists {
  .v-card__title {
    background: var(--v-primary-lighten1);
    color: var(--v-black-base);
    border-radius: 12px 12px 0px 0px !important;
    font-size: 14px;
    line-height: 22px;
    height: 47px;
    flex-wrap: inherit;
  }
  .ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 15ch;
    display: inline-block;
    width: 28ch;
    white-space: nowrap;
  }
}
.info-widget {
  width: 451px;
  height: 114px;
  background: var(--v-yellow-lighten1);
  border: 1px solid var(--v-primary-lighten1);
  text-align: justify;
}
</style>
