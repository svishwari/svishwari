<template>
  <div>
    <v-data-iterator :items="items" :items-per-page="100" hide-default-footer>
      <template v-slot:default="props">
        <!-- header -->
        <v-row align="center" no-gutters>
          <v-col v-for="field in fields" :key="field.label">
            <div class="px-4 py-2">
              <span class="text-caption">
                {{ field.label }}
              </span>
            </div>
          </v-col>
        </v-row>

        <!-- row -->
        <v-card
          v-for="item in Object.values(props.items)"
          :key="item.id"
          :class="{ 'bordered-card': bordered }"
          class="data-card mb-4"
        >
          <v-row align="center" no-gutters>
            <v-col v-for="field in fields" :key="field.key">
              <div class="pa-4">
                <!-- cell slot -->
                <slot
                  :name="`field:${field.key}`"
                  :value="item[field.key]"
                  :item="item"
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
      <template v-slot:no-data>
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

    bordered: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.data-card {
  box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, 0.05) !important;
}

.empty-card {
  border: 1px solid var(--v-zircon-base) !important;
}

.bordered-card {
  border-left: 10px solid var(--v-aliceBlue-base);
}
</style>
