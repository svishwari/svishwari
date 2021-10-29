<template>
  <v-card class="rounded-lg card-info-wrapper box-shadow-5">
    <v-card-title class="py-5 pl-6" data-e2e="customer-insights">
      <h3 class="text-h3">Customer insights</h3>
      <tooltip position-top>
        <icon type="ds_lock_special" :size="17" color="black" class="ml-2" />
        <template #tooltip>
          You do not have access to see individual information.<br />
          Contact your administrator for access.
        </template>
      </tooltip>
    </v-card-title>
    <v-card-text class="justify-center px-0">
      <v-simple-table>
        <template v-slot:default>
          <tbody>
            <tr>
              <td class="text-body-1 black--text text--lighten-4 pl-6">
                Email
              </td>
              <td class="text-body-1 blur-text">
                {{ insights["email"] | Empty }}
              </td>
              <td class="text-body-1 black--text text--lighten-4">Address</td>
              <td class="text-body-1 blur-text">
                {{ insights["address"] | Empty }}
              </td>
            </tr>
            <tr>
              <td class="text-body-1 black--text text--lighten-4 pl-6">
                Phone
              </td>
              <td class="text-body-1 blur-text">
                {{ insights["phone"] | Empty }}
              </td>
              <td class="text-body-1 black--text text--lighten-4">City</td>
              <td class="text-body-1 blur-text">
                {{ insights["city"] | Empty }}
              </td>
            </tr>
            <tr>
              <td class="text-body-1 black--text text--lighten-4 pl-6">Age</td>
              <td class="text-body-1 blur-text">
                {{ insights["age"] | Empty }}
              </td>
              <td class="text-body-1 black--text text--lighten-4">State</td>
              <td class="text-body-1 blur-text">
                {{ insights["state"] | Empty }}
              </td>
            </tr>
            <tr>
              <td class="text-body-1 black--text text--lighten-4 pl-6">
                Gender
              </td>
              <td class="text-body-1">
                <span class="blur-text">
                  {{ insights["gender"] | Empty }}
                </span>
              </td>
              <td class="text-body-1 black--text text--lighten-4">Zip</td>
              <td class="text-body-1">
                <span class="blur-text">
                  {{ insights["zip"] | Empty }}
                </span>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card-text>
  </v-card>
</template>

<script>
import Icon from "../../components/common/Icon.vue"
import Tooltip from "../../components/common/Tooltip.vue"
export default {
  name: "ProfileIdentifiableInsights",
  components: { Tooltip, Icon },
  props: {
    insights: {
      type: Object,
      required: true,
      default: () => {},
    },
  },
}
</script>

<style lang="scss" scoped>
.blur-text {
  color: transparent;
  text-shadow: 0 0 8px #000;
  user-select: none;
}
</style>
