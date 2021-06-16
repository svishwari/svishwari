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
        <v-row align="center" no-gutters :class="{ 'pl-2': bordered }">
          <v-col v-for="field in fields" :key="field.label" :cols="field.col">
            <div class="px-4 py-2">
              <span class="text-caption">
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
                      'secondary--text': isSortedBy(field.key),
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

        <!-- row -->
        <v-card
          v-for="(item, index) in Object.values(props.items)"
          :key="index"
          :class="{ 'bordered-card': bordered }"
          class="data-card mb-2"
        >
          <v-row align="center" no-gutters>
            <v-col v-for="field in fields" :key="field.key" :cols="field.col">
              <div class="pa-4">
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
      </template>

      <!-- empty slot -->
      <template #no-data>
        <v-alert color="background" class="empty-card">
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

export default {
  name: "DataCards",

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
  },

  data() {
    return {
      sortBy: null,
      sortDesc: true,
      itemsPerPage: ALL,
    }
  },

  methods: {
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
}
</script>

<style lang="scss" scoped>
.data-card {
  @extend .box-shadow-5;
}

.empty-card {
  border: 1px solid var(--v-zircon-base) !important;
}

.bordered-card {
  border-left: 8px solid var(--v-aliceBlue-base);
}
</style>
