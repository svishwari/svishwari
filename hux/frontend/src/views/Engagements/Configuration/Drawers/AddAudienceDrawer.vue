<template>
  <Drawer v-model="localToggle" :disable-transition="isOpening" expandable>
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
      <v-btn tile color="white" @click="closeDrawer()">
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

  computed: {
    isOpening() {
      return this.localToggle
    },
  },

  methods: {
    closeDrawer() {
      this.localToggle = false
    },

    add() {
      // TODO: Call the API to create the audience
      // If successful, close the drawer
      this.closeDrawer()
    },
  },

  async mounted() {
    this.loading = true
    // do something ...
  },
}
</script>
