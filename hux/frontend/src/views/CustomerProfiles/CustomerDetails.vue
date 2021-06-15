<template>
  <Drawer v-model="localDrawer">
    <template #header-left>
      <div class="d-flex align-center">
        <h3 class="text-h3 ml-2 neroBlack--text">Customers</h3>
      </div>
    </template>
    <template #default>
      <PageHeader class="top-bar" :headerHeight="40">
        <template slot="left">
          <v-icon size="18" color="black">mdi-magnify</v-icon>
        </template>
      </PageHeader>
      <hux-data-table :headers="columnDefs" :dataItems="customers">
        <template #row-item="{ item }">
          <td
            v-for="header in columnDefs"
            :key="header.value"
            :style="{ width: header.width }"
          >
            <div v-if="header.value == 'id'">
              <a @click="loadCustomerProfile(item[header.value])">{{
                item[header.value]
              }}</a>
            </div>
            <div
              v-if="header.value == 'first_name' || header.value == 'last_name'"
            >
              <span v-if="item.last_name">{{ item.last_name }}, </span>
              <span v-if="item.first_name"> {{ item.first_name }}</span>
            </div>
            <div v-if="header.value == 'match_confidence'">
              <hux-slider
                :isRangeSlider="false"
                :value="item[header.value]"
              ></hux-slider>
            </div>
          </td>
        </template>
      </hux-data-table>
    </template>
    <template #footer-left>
      <div class="d-flex align-baseline footer-font">
        {{ total_customers }} results
      </div>
    </template>
  </Drawer>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Drawer from "@/components/common/Drawer"
import HuxDataTable from "../../components/common/dataTable/HuxDataTable.vue"
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
      loading: false,
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
          width: "250px",
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
      if (!this.localDrawer) {
        this.$emit("onClose")
      }
    },
    finalEngagements: function (newVal) {
      this.selectedEngagements = newVal
    },
  },

  computed: {
    ...mapGetters({
      customer: "customers/single",
      customersList: "customers/list",
    }),

    customers() {
      let allCustomerList = JSON.parse(JSON.stringify(this.customersList))
      allCustomerList.forEach((data) => {
        data.match_confidence = parseInt(
          this.$options.filters
            .percentageConvert(data.match_confidence, true, true)
            .slice(0, -1)
        )
      })
      return allCustomerList
    },

    total_customers() {
      return this.customersList.length
    },

    id() {
      return this.$route.params.id
    },
  },

  methods: {
    ...mapActions({
      getCustomer: "customers/get",
    }),

    loadCustomerProfile(huxId) {
      this.getCustomer(huxId)
    },
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
</style>
