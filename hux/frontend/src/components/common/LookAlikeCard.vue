<template>
  <v-card class="rounded-lg card-info-wrapper lookalike-card box-shadow-5">
    <v-card-title
      class="card-heading d-flex justify-space-between py-3 pl-4 pr-0"
    >
      <span>Lookalikes</span>
      <v-btn
        :disabled="status == 'disabled'"
        text
        color="primary"
        @click="onCreateLookalike"
      >
        <icon type="lookalike-card" :size="16" class="mr-1" />
        Create lookalike
      </v-btn>
    </v-card-title>
    <v-card-text v-if="lookalikesData && status == 'active'" class="pl-0 pr-0">
      <v-simple-table fixed-header height="200px">
        <template v-slot:default>
          <tbody>
            <tr v-for="data in lookalikesData" :key="data.id">
              <td class="title-text name-col">
                <Tooltip>
                  <template #label-content>
                    <router-link
                      :to="{
                        name: 'AudienceInsight',
                        params: { id: data.id },
                      }"
                      class="cell text-decoration-none"
                      append
                    >
                      {{ data.name }}
                    </router-link>
                  </template>
                  <template #hover-content> {{ data.name }} </template>
                </Tooltip>
              </td>
              <td class="table-text cl">
                <template>
                  <Tooltip>
                    <template #label-content>
                      {{ data.size | Numeric(true, false, true) | Empty("-") }}
                    </template>
                    <template #hover-content>
                      {{ data.size | Numeric(true) | Empty("-") }}
                    </template>
                  </Tooltip></template
                >
              </td>
              <td class="table-text cl">
                <template>
                  <Tooltip>
                    <template #label-content>
                      {{ data.update_time | Date("relative") | Empty("-") }}
                    </template>
                    <template #hover-content>
                      {{ data.update_time | Date | Empty("-") }}
                    </template>
                  </Tooltip>
                </template>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card-text>
    <v-card-text
      v-if="!lookalikesData && status == 'active'"
      class="pl-4 pr-4 pt-4"
    >
      <v-list-item-subtitle>
        This audience has no lookalikes yet.
      </v-list-item-subtitle>
      <span>Create one by clicking the "Create lookalike" above.</span>
    </v-card-text>
    <v-card-text v-if="status == 'disabled'" class="pl-4 pr-4 pt-4">
      <span>
        This audience is currently getting prepared in Facebook. This could take
        a couple hours so check back later.
      </span>
    </v-card-text>
  </v-card>
</template>

<script>
import Icon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip.vue"
export default {
  name: "look-alike-card",
  components: {
    Icon,
    Tooltip,
  },
  data() {
    return {
      lookalikesData: this.value,
    }
  },
  props: {
    value: {
      type: Array,
      required: true,
    },
    status: {
      type: String,
      required: true,
    },
  },
  methods: {
    onCreateLookalike: function () {
      this.$emit("createLookalike")
    },
  },
}
</script>

<style lang="scss" scoped>
.lookalike-card {
  min-height: 261px;
  max-height: 261px;
  overflow: hidden;

  ::v-deep .v-card-text {
    padding: 0px !important;
  }

  .name-col {
    min-width: 118px;
    max-width: 118px;
  }
  .cell {
    padding-left: 18px !important;
    font-weight: normal;
    font-size: 14px !important;
    line-height: 22px;
    display: inline-block;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-box-orient: vertical !important;
    -webkit-line-clamp: 3 !important;
    overflow: hidden !important;
  }

  .title-text {
    padding-left: 18px !important;
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
    background-color: rgba(236, 244, 249, 1);
    font-weight: 400;
    height: 54px !important;
  }

  .title-text {
    font-family: Open Sans;
    font-style: normal;
    font-weight: normal;
    color: var(--v-gray-base) !important;
    font-size: 12px !important;
    padding: 0px !important;

    ::v-deep .v-list-item {
      min-height: 44px;
    }
  }
}
</style>
