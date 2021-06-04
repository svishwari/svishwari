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
import { mapActions } from "vuex"
import Drawer from "@/components/common/Drawer.vue"

export default {
  name: "AddAudienceDrawer",

  components: {
    Drawer,
  },

  props: {
    /**
     * The list of audiences to add the new audience to, keyed by id
     *
     * Example:
     * {
     *     "1": {
     *         "id": "1",
     *         "name": "Audience name",
     *         "size": 91240,
     *     },
     * }
     */
    value: {
      type: Object,
      required: true,
    },

    /**
     * A toggle indicating whether the drawer is open or not.
     */
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
    ...mapActions({
      addAudience: "audiences/add",
    }),

    closeDrawer() {
      this.localToggle = false
    },

    async add() {
      try {
        this.loading = true

        // TODO: replace data with details of the audience in the form
        const data = {
          name: `Gold Star Dallas ${Math.floor(Math.random() * 100)}`,
          filters: [],
        }

        const newAudience = await this.addAudience(data)

        this.$set(this.value, newAudience.id, {
          id: newAudience.id,
          name: newAudience.name,
          size: newAudience.size,
        })

        this.closeDrawer()
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
