<template>
  <div>
    <v-card v-if="insights" class="rounded-lg card-info-wrapper box-shadow-5">
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
    <v-card v-else class="pt-4 rounded-lg box-shadow-5" height="200px">
      <empty-page
        class="title-no-notification"
        type="error-on-screens"
        :size="50"
      >
        <template #title>
          <div class="title-no-notification">
            Contact preferences are currently unavailable
          </div>
        </template>
        <template #subtitle>
          <div class="des-no-notification">
            Our team is working hard to fix it. Please be patient and try again
            soon!
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
</style>
