<template>
  <v-card
    class="rounded-lg card-info-wrapper lookalike-card box-shadow-5"
    height="100%"
  >
    <v-card-title
      class="
        card-heading
        d-flex
        justify-space-between
        py-3
        pl-4
        lookalike-card-title
      "
    >
      <span>Lookalikes</span>
      <v-btn
        :disabled="!isActive"
        text
        color="primary"
        class="body-2 pa-1"
        @click="onCreateLookalike"
      >
        <icon
          type="lookalike-card"
          :size="14"
          class="mr-1"
          :color="!isActive ? 'lightGreyAnotherVariant' : 'primary'"
        />
        Create lookalike
      </v-btn>
    </v-card-title>
    <v-card-text v-if="lookalikesData.length > 0 && isActive" class="pl-0 pr-0">
      <v-simple-table fixed-header height="200px">
        <template v-slot:default>
          <tbody>
            <tr v-for="data in lookalikesData" :key="data.id">
              <td class="title-text name-col">
                <tooltip>
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
                </tooltip>
              </td>
              <td class="table-text">
                <template>
                  <tooltip>
                    <template #label-content>
                      {{ data.size | Numeric(true, false, true) | Empty("-") }}
                    </template>
                    <template #hover-content>
                      {{ data.size | Numeric(true) | Empty("-") }}
                    </template>
                  </tooltip></template
                >
              </td>
              <td class="table-text">
                <template>
                  <tooltip>
                    <template #label-content>
                      {{ data.update_time | Date("relative") | Empty("-") }}
                    </template>
                    <template #hover-content>
                      {{ data.update_time | Date | Empty("-") }}
                    </template>
                  </tooltip>
                </template>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card-text>
    <v-card-text
      v-if="lookalikesData.length == 0 && isActive"
      class="pl-4 pr-4 pt-4"
    >
      <v-list-item-subtitle>
        This audience has no lookalikes yet.
      </v-list-item-subtitle>
      <span>Create one by clicking the "Create lookalike" above.</span>
    </v-card-text>
    <v-card-text v-if="!isActive" class="pl-4 pr-4 pt-4">
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
  name: "LookAlikeCard",
  components: {
    Icon,
    Tooltip,
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
  data() {
    return {
      lookalikesData: this.value,
    }
  },
  computed: {
    isActive() {
      return this.status == "Active" ? true : false
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
  overflow: hidden;

  ::v-deep .v-card-text {
    padding: 0px !important;
  }

  .v-data-table {
    .v-data-table__wrapper {
      tr {
        td {
          border-bottom: thin solid rgba(0, 0, 0, 0.12);
        }
        &:hover {
          background: var(--v-white-base) !important;
        }
      }
    }
  }

  .name-col {
    min-width: 130px;
    max-width: 130px;
  }

  .cell {
    padding-left: 18px !important;
    font-weight: normal;
    font-size: 12px !important;
    line-height: 16px;
    display: inline-block;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-box-orient: vertical !important;
    -webkit-line-clamp: 1 !important;
    overflow: hidden !important;
  }

  .title-text {
    padding-left: 18px !important;
    font-family: Open Sans;
    font-style: normal;
    font-weight: normal;
    color: var(--v-black-darken1) !important;
    font-size: 12px !important;
  }
  .table-text {
    color: var(--v-black-darken4);
    font-size: 12px !important;
  }

  .card-heading {
    font-size: 15px !important;
    background-color: var(--v-primary-lighten2);
    font-weight: 400;
    height: 54px !important;
  }

  .title-text {
    font-family: Open Sans;
    font-style: normal;
    font-weight: normal;
    color: var(--v-black-darken1) !important;
    font-size: 12px !important;
    padding: 0px !important;

    ::v-deep .v-list-item {
      min-height: 44px;
    }
  }
  ::v-deep .v-data-table__wrapper {
    height: inherit !important;
    min-height: 100px !important;
    max-height: 190px;
  }
  ::-webkit-scrollbar {
    width: 5px;
  }
  ::-webkit-scrollbar-track {
    box-shadow: inset 0 0 5px var(--v-white-base);
    border-radius: 10px;
  }
  ::-webkit-scrollbar-thumb {
    background: var(--v-lightGrey-base);
    border-radius: 5px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: var(--v-lightGrey-base);
  }
}
</style>
