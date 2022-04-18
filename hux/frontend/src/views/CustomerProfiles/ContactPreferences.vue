<template>
  <div>
    <v-card
      v-if="insights && !profileError"
      class="rounded-lg card-info-wrapper box-shadow-5"
    >
      <v-card-title
        class="card-heading py-5 pl-6"
        data-e2e="contact-preferencecs"
      >
        <h3 class="text-h3">Contact preferences</h3>
      </v-card-title>
      <v-card-text class="title-text px-0">
        <v-simple-table>
          <template #default>
            <tbody>
              <tr v-for="pref in prefrerences" :key="pref.id">
                <td class="text-body-1 black--text text--lighten-4 pl-6">
                  {{ pref.title }}
                </td>
                <td class="text-body-1 black--text">
                  {{ pref.value }}
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card-text>
    </v-card>
    <v-card
      v-else
      class="no-data-chart-frame pt-4 rounded-lg box-shadow-5"
      height="280px"
    >
      <empty-page
        class="title-no-notification pa-8"
        :type="profileError ? 'error-on-screens' : 'no-customer-data'"
        :size="50"
      >
        <template #title>
          <div class="title-no-notification">
            {{ profileError ? "Unavailable" : "No customer Data" }}
          </div>
        </template>
        <template #subtitle>
          <div class="des-no-notification">
            {{
              profileError
                ? "Our team is working hard to fix this data table. Please be patient and try again soon!"
                : "Customer data will appear here once customer data is available."
            }}
          </div>
        </template>
      </empty-page>
    </v-card>
  </div>
</template>

<script>
import EmptyPage from "@/components/common/EmptyPage.vue"
export default {
  name: "ContactPreferences",
  components: { EmptyPage },
  props: {
    insights: {
      type: Object,
      required: true,
      default: () => {},
    },
    profileError: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    prefrerences() {
      return [
        {
          id: 1,
          title: "Email",
          value: this.insights["preference_email"],
          subLabel: null,
        },
        {
          id: 2,
          title: "Push",
          value: this.insights["preference_push"],
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 3,
          title: "SMS",
          value: this.insights["preference_sms"],
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 4,
          title: "In-App",
          value: this.insights["preference_in_app"],
          subLabel: null,
        },
      ]
    },
  },
}
</script>
<style lang="scss" scoped>
::v-deep table {
  tr:hover {
    background-color: transparent !important;
  }
  td {
    height: 40px !important;
  }
}
.no-data-chart-frame {
  @include no-data-frame-bg("empty-1-chart.png");
}
</style>
