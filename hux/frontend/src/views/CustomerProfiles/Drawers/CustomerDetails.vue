<template>
  <Drawer v-model="localDrawer" :drawerpadding="'pa-0'" :headerpadding="'px-3'">
    <template #header-left>
      <div class="d-flex align-center">
        <h3 class="text-h3 ml-2 neroBlack--text">Customers</h3>
      </div>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />
      <PageHeader class="top-bar" :headerHeight="40" :paddingchanges="'px-4'">
        <template slot="left">
          <v-icon size="18" color="lightGrey">mdi-magnify</v-icon>
        </template>
      </PageHeader>
      <hux-data-table :headers="columnDefs" :dataItems="customers">
        <template #row-item="{ item }">
          <td
            v-for="header in columnDefs"
            :key="header.value"
            :style="{ width: header.width }"
          >
            <div v-if="header.value == 'id'" class="text-body-2">
              <router-link
                :to="{
                  name: 'CustomerProfileDetails',
                  params: { id: item[header.value] },
                }"
                class="text-decoration-none text-body-2"
                append
                >{{ item[header.value] }}
              </router-link>
            </div>
            <div
              v-if="header.value == 'first_name' || header.value == 'last_name'"
              class="text-body-2"
            >
              <span v-if="item.last_name">{{ item.last_name }}, </span>
              <span v-if="item.first_name"> {{ item.first_name }}</span>
            </div>
            <div v-if="header.value == 'match_confidence'">
              <hux-slider
                :isRangeSlider="false"
                :value="item[header.value]"
                class="slider-margin"
              ></hux-slider>
            </div>
          </td>
        </template>
      </hux-data-table>
    </template>
    <template #footer-left>
      <div class="d-flex align-baseline footer-font">
        {{ customersList.length }} results
      </div>
    </template>
  </Drawer>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Drawer from "@/components/common/Drawer"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import HuxSlider from "@/components/common/HuxSlider"
import PageHeader from "@/components/PageHeader"

export default {
  name: "CustomerDetails",
  components: {
    Drawer,
    HuxDataTable,
    HuxSlider,
    PageHeader,
  },
  data() {
    return {
      loading: true,
      localDrawer: this.value,
      columnDefs: [
        {
          text: "Hux ID",
          value: "id",
          width: "auto",
        },
        {
          text: "Full name",
          value: "first_name",
          width: "auto",
        },
        {
          text: "Match confidence",
          value: "match_confidence",
          width: "200px",
          hoverTooltip:
            "A percentage that indicates the level of certainty that all incoming records were accurately matched to a given customer.",
        },
      ],
    }
  },

  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
  },

  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
  },

  async updated() {
    this.loading = true
    await this.getCustomers()
    this.loading = false
  },

  computed: {
    ...mapGetters({
      customersList: "customers/list",
    }),

    customers() {
      let sortedCustomerList = this.customersList
      return sortedCustomerList.sort((a, b) => a.id - b.id)
    },
  },

  methods: {
    ...mapActions({
      getCustomers: "customers/getAll",
    }),
  },
}
</script>

<style lang="scss" scoped>
.hux-data-table {
  margin-top: 1px;
}
::v-deep .v-sheet .theme--light .v-toolbar {
  background: var(--v-aliceBlue-base);
}
::v-deep .theme--light.v-sheet {
  box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.25);
}
.hux-data-table {
  ::v-deep table {
    .v-data-table-header {
      tr {
        height: 40px !important;
      }
      th {
        background: var(--v-aliceBlue-base);
      }
    }
  }
}
.footer-font {
  font-family: Open Sans;
  font-style: normal;
  font-weight: normal;
  font-size: 12px;
  line-height: 16px;
  color: var(gray);
}
.slider-margin {
  margin-bottom: -22px;
}
</style>
