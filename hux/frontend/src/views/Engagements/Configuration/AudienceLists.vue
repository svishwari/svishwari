<template>
  <div>
    <v-card class="rounded-lg card-style-list audiences-lists ml-6" flat>
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
            <div v-if="header.value == 'name'" class="black--text text-body-1">
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
            <div v-if="header.value == 'size'" class="black--text text-body-1">
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
                    <logo class="mr-1" :type="destination.type" :size="24" />
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
        <icon type="FAB-bulb" :size="21" class="mt-1" />
      </div>
      <div class="description ml-4 text-body-1 black-base text-left">
        You may create a lookalike audience for this engagement after delivering
        an audience to a digital advertising platform.
      </div>
    </div>
  </div>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Size from "@/components/common/huxTable/Size.vue"
import Icon from "@/components/common/Icon.vue"
import Logo from "@/components/common/Logo.vue"
import Tooltip from "@/components/common/Tooltip"

export default {
  name: "StandaloneDelivery",
  components: {
    HuxDataTable,
    Size,
    Icon,
    Logo,
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
          width: "180px",
        },
        {
          text: "Size",
          value: "size",
          width: "100px",
        },
        {
          text: "Destination(s)",
          value: "destinations",
          width: "130px",
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
::-webkit-scrollbar {
  width: 5px;
}
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px var(--v-white-base);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: var(--v-black-lighten3);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--v-black-lighten3);
}
.info-widget {
  background: var(--v-yellow-lighten1);
  border: 1px solid var(--v-primary-lighten1);
  text-align: justify;
}
.card-style-list {
  border: 1px solid var(--v-black-lighten2);
  border-radius: 12px !important;
}
::v-deep .hux-data-table[data-v-1db23c48] table tr:last-child > td {
  border-bottom: none !important;
}
::v-deep .theme--light .v-data-table {
  background-color: transparent !important;
}
</style>
