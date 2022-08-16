<template>
  <div>
    <v-data-iterator
      :items="items"
      :items-per-page="itemsPerPage"
      :sort-by.sync="sortBy"
      :sort-desc.sync="sortDesc"
      hide-default-footer
    >
      <template #default="props">
        <!-- header -->
        <v-card class="header-alignment">
          <v-row
            align="center"
            no-gutters
            :class="{ 'pl-2': bordered, 'data-card-headers': true }"
          >
            <v-col
              v-for="field in fields"
              :key="field.label"
              :cols="field.col"
              :class="[headerClass, { center: field.center }]"
            >
              <tooltip v-if="field.tooltip" :max-width="tooltipwidth">
                <template #label-content>
                  <div class="px-4 py-2" :class="{ 'ta-center': field.center }">
                    <span class="text-body-2 black--text text--lighten-4">
                      {{ field.label }}
                      <v-btn
                        v-if="field.sortable"
                        icon
                        x-small
                        @click="setSortBy(field.key)"
                      >
                        <v-icon
                          x-small
                          :class="{
                            'primary--text text--lighten-8': isSortedBy(
                              field.key
                            ),
                            'rotate-icon-180':
                              isSortedBy(field.key) && sortDesc,
                          }"
                        >
                          mdi-arrow-down
                        </v-icon>
                      </v-btn>
                    </span>
                  </div>
                </template>
                <template #hover-content>
                  {{ field.tooltip }}
                </template>
              </tooltip>
              <div
                v-else
                class="px-4 py-2"
                :class="{ 'ta-center': field.center }"
              >
                <span class="text-body-2 black--text text--lighten-4">
                  {{ field.label }}
                  <v-btn
                    v-if="field.sortable"
                    icon
                    x-small
                    @click="setSortBy(field.key)"
                  >
                    <v-icon
                      x-small
                      :class="{
                        'primary--text text--lighten-8': isSortedBy(field.key),
                        'rotate-icon-180': isSortedBy(field.key) && sortDesc,
                      }"
                    >
                      mdi-arrow-down
                    </v-icon>
                  </v-btn>
                </span>
              </div>
            </v-col>
          </v-row>
        </v-card>

        <!-- row -->
        <div v-for="(item, index) in Object.values(props.items)" :key="index">
          <v-card
            :class="{
              'bordered-card': bordered,
              'mt-0': index == 0,
            }"
            class="data-card my-3 text-body-1 alignment card-changes"
            :style="
              bordered
                ? item.colors
                  ? style(item.colors.color, item.colors.variant)
                  : style()
                : ''
            "
          >
            <v-row align="center" no-gutters>
              <v-col v-for="field in fields" :key="field.key" :cols="field.col">
                <div :class="[cardClass, { center: field.center }]">
                  <!-- cell slot -->
                  <slot
                    :name="`field:${field.key}`"
                    :value="item[field.key]"
                    :item="item"
                    :index="index"
                  >
                    <!-- default cell -->
                    <template>{{ item[field.key] }}</template>
                  </slot>
                </div>
              </v-col>
            </v-row>
          </v-card>
          <v-divider
            v-if="item.default && multipleSegments"
            class="mt-6 mb-6"
          />
        </div>
      </template>
      <!-- empty slot -->
      <template #no-data>
        <v-alert color="primary" class="empty-card">
          <v-row align="center">
            <slot v-if="$slots.empty" name="empty"></slot>
            <v-col v-else class="grow">{{ empty }}</v-col>
          </v-row>
        </v-alert>
      </template>
    </v-data-iterator>
  </div>
</template>

<script>
const ALL = -1
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "DataCards",

  components: {
    Tooltip,
  },

  props: {
    items: {
      type: Array,
      required: true,
    },

    fields: {
      type: Array,
      required: true,
    },

    empty: {
      type: String,
      required: false,
      default: "No items available.",
    },

    sort: {
      type: String,
      required: false,
      default: "none",
    },

    bordered: {
      type: Boolean,
      required: false,
      default: false,
    },

    cardClass: {
      type: String,
      required: false,
      default: "pa-4",
    },

    headerClass: {
      type: String,
      required: false,
      default: "",
    },
    multipleSegments: {
      type: Boolean,
      required: false,
      default: false,
    },
    tooltipwidth: {
      type: String,
      required: false,
      default: "auto",
    },
  },

  data() {
    return {
      sortBy: null,
      sortDesc: true,
      itemsPerPage: ALL,
    }
  },

  mounted() {
    if (this.sort !== "none") {
      if (this.sort === "asc") {
        // Sorts the list in ascending order
        this.sortDesc = false
        this.setSortBy(this.fields[0].key)
      } else {
        // Sorts the list in descending order
        this.setSortBy(this.fields[0].key)
      }
    }
  },

  methods: {
    style(color, variant) {
      return `border-left: 10px solid var(--v-${color ? color : "primary"}-${
        variant ? variant : "lighten6"
      })`
    },

    setSortBy(key) {
      if (this.isSortedBy(key)) {
        this.sortDesc = !this.sortDesc
      } else {
        this.sortBy = key
      }
    },

    isSortedBy(key) {
      return Boolean(this.sortBy === key)
    },
  },
}
</script>

<style lang="scss" scoped>
.data-card {
  @extend .box-shadow-5;
}
.empty-card {
  border: 1px solid var(--v-black-lighten2) !important;
  background: var(--v-primary-lighten1) !important;
}

.bordered-card {
  border-left: 8px solid var(--v-primary-lighten6);
  border-radius: 0px;
}

.alignment {
  height: 60px;
  display: flex;
  align-items: center;
}
.header-alignment {
  box-shadow: none !important;
  background-color: transparent !important;
}
</style>
