<template>
  <div>
    <PageHeader class="background-border" :headerHeightChanges="'py-3'">
      <template #left>
        <Breadcrumb :items="items" />
      </template>
      <template #right>
        <v-icon
          size="22"
          color="lightGrey"
          class="icon-border icon-cursor pa-2 ma-1"
        >
          mdi-download
        </v-icon>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />

    <div v-if="!loading && singleCustomer" class="pl-15 py-6 pr-9">
      <v-row>
        <v-col cols="3">
          <v-card
            class="
              text-center
              rounded-lg
              card-info-wrapper
              box-shadow-5
              card-height
            "
          >
            <v-card-title
              class="justify-center font-weight-regular title-font-size"
            >
              {{ fullName }}
            </v-card-title>
            <v-card-text class="justify-center title-text pt-5 pb-5">
              <div>Hux ID</div>
              <span class="id-size">{{ singleCustomer.hux_id }} </span>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col
          :cols="data.colValue"
          v-for="data in customerDataDisplay"
          :key="data.id"
          class="matix-card-space"
        >
          <v-card
            class="rounded-lg card-info-wrapper card-shadow no-background"
          >
            <v-card-text class="pl-3 pr-3 pb-3 pt-3 matrix-card">
              <div class="title-text pb-1">
                {{ data.title }}
                <Tooltip v-if="data.hoverTooltip" positionTop>
                  <template #label-content>
                    <Icon type="info" :size="12" v-if="data.hoverTooltip" />
                  </template>
                  <template #hover-content>
                    {{ data.hoverTooltip }}
                  </template>
                </Tooltip>
              </div>
              <span v-if="!data.slider" class="sample-card-text">{{
                data.value
              }}</span>
              <hux-slider
                v-if="data.slider"
                :isRangeSlider="false"
                :value="data.value"
              ></hux-slider>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row class="details-card">
        <v-col cols="3"> </v-col>
        <v-col
          v-for="data in customerDetailsMore"
          :cols="data.colValue"
          :key="data.id"
          class="matix-card-space"
        >
          <v-card
            class="rounded-lg card-info-wrapper card-shadow no-background"
          >
            <v-card-text class="pl-3 pr-3 pb-3 pt-3 matrix-card">
              <div class="title-text pb-1">
                {{ data.title }}
                <Tooltip v-if="data.hoverTooltip" positionTop>
                  <template #label-content>
                    <Icon type="info" :size="12" v-if="data.hoverTooltip" />
                  </template>
                  <template #hover-content>
                    {{ data.hoverTooltip }}
                  </template>
                </Tooltip>
              </div>
              <div class="sample-card-text">{{ data.value }}</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="5">
          <v-card class="rounded-lg card-info-wrapper box-shadow-5">
            <v-card-title class="py-5 card-heading">
              {{ cardTitles[0].title }}
              <v-icon size="17" color="neroBlack" class="ml-2">
                mdi-lock-outline
              </v-icon>
            </v-card-title>
            <v-card-text class="justify-center title-text">
              <v-simple-table>
                <template v-slot:default>
                  <tbody>
                    <tr>
                      <td class="title-text">Email</td>
                      <td class="table-text">
                        <span v-if="singleCustomer.email" class="blur-text"
                          >{{ singleCustomer.email }}
                        </span>
                        <span v-else>-</span>
                      </td>
                      <td class="title-text">Address</td>
                      <td class="table-text">
                        <span v-if="singleCustomer.address" class="blur-text">
                          {{ singleCustomer.address }}
                        </span>
                        <span v-else>-</span>
                      </td>
                    </tr>
                    <tr>
                      <td class="title-text">Phone</td>
                      <td class="table-text">
                        <span v-if="singleCustomer.phone" class="blur-text">
                          {{ singleCustomer.phone }}
                        </span>
                        <span v-else>-</span>
                      </td>
                      <td class="title-text">City</td>
                      <td class="table-text">
                        <span v-if="singleCustomer.city" class="blur-text">
                          {{ singleCustomer.city }}
                        </span>
                        <span v-else>-</span>
                      </td>
                    </tr>
                    <tr>
                      <td class="title-text">Age</td>
                      <td class="table-text">
                        <span v-if="singleCustomer.age" class="blur-text">
                          {{ singleCustomer.age }}
                        </span>
                        <span v-else>-</span>
                      </td>
                      <td class="title-text">State</td>
                      <td class="table-text">
                        <span v-if="singleCustomer.state" class="blur-text">
                          {{ singleCustomer.state }}
                        </span>
                        <span v-else>-</span>
                      </td>
                    </tr>
                    <tr>
                      <td class="title-text">Gender</td>
                      <td class="table-text">
                        <span v-if="singleCustomer.gender" class="blur-text">
                          {{ singleCustomer.gender }}
                        </span>
                        <span v-else>-</span>
                      </td>
                      <td class="title-text">Zip</td>
                      <td class="table-text">
                        <span v-if="singleCustomer.zip" class="blur-text">
                          {{ singleCustomer.zip }}
                        </span>
                        <span v-else>-</span>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="3">
          <v-card class="rounded-lg card-info-wrapper box-shadow-5">
            <v-card-title class="card-heading py-5">
              {{ cardTitles[1].title }}
            </v-card-title>
            <v-card-text class="title-text">
              <v-simple-table>
                <template v-slot:default>
                  <tbody>
                    <tr v-for="data in contactPreferences" :key="data.id">
                      <td class="title-text">{{ data.title }}</td>
                      <td class="table-text cl">{{ data.value }}</td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="4">
          <identity-chart></identity-chart>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Tooltip from "@/components/common/Tooltip.vue"
import Icon from "@/components/common/Icon"
import HuxSlider from "@/components/common/HuxSlider"
import IdentityChart from "@/components/common/identityChart/IdentityChart"

export default {
  name: "CustomerProfileDetails",
  components: {
    PageHeader,
    Breadcrumb,
    Tooltip,
    Icon,
    HuxSlider,
    IdentityChart,
  },
  data() {
    return {
      items: [
        {
          text: "Customer Profiles",
          disabled: false,
          href: this.$router.resolve({ name: "CustomerProfiles" }).href,
          icon: "customer-profiles",
        },
        {
          text: this.$route.params.id,
          disabled: true,
          href: "/customers" + this.$route.params.id,
        },
      ],
      cardTitles: [
        {
          id: 1,
          title: "Customer insights",
          icon: "customer-profiles",
        },
        {
          id: 2,
          title: "Contact preferences",
          icon: "customer-profiles",
        },
      ],
      loading: false,
    }
  },
  computed: {
    ...mapGetters({
      customer: "customers/single",
    }),
    singleCustomer() {
      return this.customer(this.$route.params.id)
    },

    id() {
      return this.$route.params.id
    },
    fullName() {
      let full_name =
        this.singleCustomer.first_name + " " + this.singleCustomer.last_name
      return full_name
    },
    customerInsightsData() {
      const insightsData = [
        {
          id: 1,
          title: "Email",
          value: this.$options.filters.Empty(this.singleCustomer.email),
        },
        {
          id: 2,
          title: "Phone",
          value: this.$options.filters.Empty(this.singleCustomer.phone),
        },
        {
          id: 3,
          title: "Age",
          value: this.$options.filters.Empty(this.singleCustomer.age),
        },
        {
          id: 4,
          title: "Gender",
          value: this.$options.filters.Empty(this.singleCustomer.gender),
        },
        {
          id: 5,
          titleNex: "Address",
          valueNex: this.$options.filters.Empty(this.singleCustomer.address),
        },
        {
          id: 6,
          titleNex: "City",
          valueNex: this.$options.filters.Empty(this.singleCustomer.city),
        },
        {
          id: 7,
          titleNex: "State",
          valueNex: this.$options.filters.Empty(this.singleCustomer.state),
        },
        {
          id: 8,
          titleNex: "Zip",
          valueNex: this.$options.filters.Empty(this.singleCustomer.zip),
        },
      ]
      return insightsData.filter(
        (item) => item.title !== null && item.titleNex !== null
      )
    },
    contactPreferences() {
      const contactData = [
        {
          id: 1,
          title: "Email",
          value: this.singleCustomer.preference_email,
          subLabel: null,
        },
        {
          id: 2,
          title: "Push",
          value: this.singleCustomer.preference_push,
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 3,
          title: "SMS",
          value: this.singleCustomer.preference_sms,
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 4,
          title: "In-App",
          value: this.singleCustomer.preference_in_app ,
          subLabel: null,
        },
      ]
      return contactData.filter((item) => item.title !== null)
    },
    customerDataDisplay() {
      const cusomerDeatils = [
        {
          id: 1,
          title: "Customer length",
          value: this.formattedDate(this.singleCustomer.since),
          colValue: 2.5,
        },
        {
          id: 2,
          title: "Match confidence",
          value: this.$options.filters.Empty(this.singleCustomer.match_confidence),
          colValue: 2.5,
          slider: true,
          hoverTooltip:
            "A percentage that indicates the level of certainty that all incoming records were accurately matched to a given customer.",
        },
        {
          id: 3,
          title: "Lifetime value",
          value: this.singleCustomer.ltv_actual
            ? "$" + this.singleCustomer.ltv_actual
            : "-",
          colValue: 2,
          hoverTooltip:
            "Assessment of the lifetime financial value of each customer.",
        },
        {
          id: 4,
          title: "Conversion time",
          value: this.$options.filters.Empty(this.formattedDate(this.singleCustomer.conversion_time)),
          colValue: 2.5,
          hoverTooltip:
            "The average time customer takes to convert to a purchase.",
        },
      ]
      return cusomerDeatils
    },
    customerDetailsMore() {
      const details = [
        {
          id: 5,
          title: "Churn score",
          value: this.$options.filters.Empty(this.singleCustomer.churn_rate)
            ,
          colValue: 2,
          hoverTooltip:
            "The measure of a customer’s likelihood to stop using a product.",
        },
        {
          id: 6,
          title: "Last click",
          colValue: 2.5,
          value: this.formattedDate(this.singleCustomer.last_click)
            ? this.formattedDate(this.singleCustomer.last_click)
            : "n/a",
        },
        {
          id: 7,
          title: "Last purchase date",
          colValue: 2.5,
          value: this.formattedDate(this.singleCustomer.last_purchase),
        },
        {
          id: 8,
          title: "Last open",
          colValue: 2.5,
          value: this.formattedDate(this.singleCustomer.last_email_open),
        },
      ]
      return details
    },
  },
  methods: {
    ...mapActions({
      getCustomer: "customers/get",
    }),
    formattedDate(value) {
      if (value) {
        return this.$options.filters.Date(value, "relative")
      }
      return "-"
    },
  },
  async mounted() {
    this.loading = true
    await this.getCustomer(this.id)
    this.loading = false
  },
}
</script>

<style lang="scss" scoped>
.customer-profile-wrap {
  ::v-deep .mdi-chevron-right::before {
    content: none;
  }
}
::v-deep .v-card__title {
  background: var(--v-aliceBlue-base);
}
::v-deep .v-card__text {
  padding: 0px;
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
.v-data-table {
  .v-data-table__wrapper {
    tr:hover:not(.v-data-table__expanded__content):not(.v-data-table__empty-wrapper) {
      background: white !important;
    }
  }
}
.title-font-size {
  font-family: Open Sans;
  font-style: normal;
  font-weight: 300 !important;
  font-size: 21px;
  color: var(--v-neroBlack-base);
}
.title-text {
  font-family: Open Sans;
  font-style: normal;
  font-weight: normal;
  color: var(--v-gray-base) !important;
  font-size: 12px !important;
}
.table-text {
  color: var(--v-neroBlack-base);
  font-size: 12px !important;
}
.card-heading {
  font-size: 15px !important;
  color: var(--v-neroBlack-base);
  font-weight: 400;
  height: 54px !important;
}
.sample-card-text {
  font-size: 14px;
  font-family: Open Sans;
  font-style: normal;
  font-weight: 600;
  color: var(--v-neroBlack-base) !important;
}
.icon-cursor {
  cursor: default !important;
}
.details-card {
  position: relative;
  margin-top: -93px;
}
.card-height {
  height: 155px !important;
}
.hux-score-slider {
  margin-bottom: -27px !important;
  margin-top: -8px;
}
.blur-text {
  color: transparent;
  text-shadow: 0 0 8px #000;
}
.no-background {
  background: none !important;
}
.matrix-card {
  height: 70px !important;
}
.matix-card-space {
  padding-right: 5px !important;
}
.id-size {
  font-size: 14px;
}
</style>
