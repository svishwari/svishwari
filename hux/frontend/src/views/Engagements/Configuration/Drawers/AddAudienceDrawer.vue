<template>
  <Drawer v-model="localToggle" expandable>
    <template #header-left>
      <h3 class="text-h3">Create a new audience</h3>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />
      <div class="pa-8">
        <p>Build a target audience from the data YOU own.</p>
      </div>
      <!-- TODO: HUS-229, HUS-445 -->
    </template>

    <template #footer-left>
      <v-btn tile color="white" @click="$emit('onCancel')">
        <span class="primary--text">Cancel &amp; back</span>
      </v-btn>
      <v-btn tile color="primary" @click="add()"> Create &amp; add </v-btn>
    </template>
  </Drawer>
</template>

<script>
import Drawer from "@/components/common/Drawer.vue"

export default {
  name: "AddAudienceDrawer",

  components: {
    Drawer,
  },

  props: {
    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      loading: false,
      localToggle: false,
    }
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },
  },

  methods: {
    add() {
      // call the API to create the audience, and on success, emit the event to
      // close this drawer and open the select drawer
      this.$emit("onCreated")
    },
  },

  async mounted() {
    this.loading = true
    // do something ...
  },
}
</script>
