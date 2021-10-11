<template>
  <drawer
    v-model="localToggle"
    :loading="loading"
    class="lookalike-drawer"
    @onClose="onBack"
  >
    <template #header-left>
      <div class="d-flex align-center">
        <icon type="lookalike" :size="32" class="mr-2" />
        <h3 class="text-h3">Create a lookalike audience in Facebook</h3>
      </div>
    </template>

    <template #default>
      <v-form ref="lookalikeForm" v-model="isFormValid">
        <div class="lookalike-form px-4 py-3">
          <div class="text-h6 black--text text--darken-3 pb-8">
            Creating a lookalike audience will create a one-off new audience in
            Facebook.
          </div>
          <text-field
            v-model="lookalikeAudience.name"
            class="pb-3"
            label-text="Lookalike audience name"
            placeholder="What is the name for this new lookalike audience?"
            :rules="lookalikeNameRules"
            required
          />

          <div class="text-caption black--text text--darken-3">
            Audience to create a lookalike from
          </div>
          <v-select
            v-model="selectAudience"
            :items="lookalikeAbleAudiences"
            dense
            outlined
            class="delivered-audience-selection pb-10"
            background-color="white"
            append-icon="mdi-chevron-down"
            required
          />

          <div class="text-caption black--text text--darken-3">
            Attach this audience to an engagement - you must have at least one
          </div>

          <hux-drop-down-search
            v-model="lookalikeAudience.engagements"
            :toggle-drop-down="toggleDropDown"
            :min-selection="1"
            :items="engagements"
            @onToggle="(val) => (toggleDropDown = val)"
          >
            <template #activator>
              <div class="dropdown-select-activator">
                <v-select
                  dense
                  readonly
                  placeholder="Select engagement(s)"
                  outlined
                  background-color="white"
                  append-icon="mdi-chevron-down"
                />
              </div>
            </template>
          </hux-drop-down-search>

          <v-chip
            v-for="(item, index) in lookalikeAudience.engagements"
            :key="item.id"
            :close="selectedEngagementsLength > 1"
            small
            class="mr-2 my-2 font-weight-semi-bold"
            text-color="primary"
            color="primary lighten-4"
            close-icon="mdi-close"
            @click:close="detachEngagement(index)"
          >
            {{ item.name }}
          </v-chip>

          <div class="text-caption black--text text--darken-3 pt-9 pb-1">
            The reach for this lookalike audience
          </div>
          <div class="text-caption black--text text--darken-1 pb-1">
            Audience reach ranges from 1% to 10% of the combined population of
            your selected locations. A 1% lookalike consists of the people most
            similar to your lookalike source. Increasing the percentage creates
            a bigger, broader audience.
          </div>

          <look-alike-slider v-model="lookalikeAudience.value" class="mr-6" />
        </div>
      </v-form>
    </template>

    <template #footer-right>
      <div class="d-flex align-baseline">
        <hux-button
          variant="primary"
          is-tile
          height="40"
          class="ma-2"
          :is-disabled="!(isFormValid && selectedEngagementsLength !== 0)"
          @click="createLookalike()"
        >
          Create &amp; deliver
        </hux-button>
      </div>
    </template>

    <template #footer-left>
      <div />
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import Drawer from "@/components/common/Drawer"
import LookAlikeSlider from "@/components/common/LookAlikeSlider"
import TextField from "@/components/common/TextField"
import Icon from "@/components/common/Icon.vue"
import HuxButton from "@/components/common/huxButton"
import HuxDropDownSearch from "@/components/common/HuxDropDownSearch"

export default {
  name: "LookAlikeAudienceDrawer",

  components: {
    Drawer,
    Icon,
    TextField,
    LookAlikeSlider,
    HuxButton,
    HuxDropDownSearch,
  },

  props: {
    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },

    selectedAudience: {
      required: false,
    },
  },

  data() {
    return {
      loading: false,
      localToggle: false,
      toggleDropDown: false,
      lookalikeAudience: {
        name: null,
        value: 5,
        audience: null,
        engagements: [],
      },
      isFormValid: false,
      lookalikeNameRules: [(v) => !!v || "Lookalike audience name is required"],
    }
  },

  computed: {
    ...mapGetters({
      engagements: "engagements/list",
      audiences: "audiences/list",
    }),

    selectAudience: {
      get() {
        const aud = this.audiences.filter(
          (aud) => aud.id === this.selectedAudience.id
        )
        return aud.length > 0 ? aud[0] : {}
      },
      set(value) {
        this.lookalikeAudience.audience = value
      },
    },
    lookalikeAbleAudiences() {
      // This assumes we cannot create a lookalike audience from a lookalike audience
      let filteredAudience = this.audiences.filter(
        (each) => each.lookalikeable === "Active" && !each.is_lookalike
      )

      return filteredAudience.map((each) => {
        return {
          text: each.name,
          value: each,
        }
      })
    },

    selectedEngagementsLength() {
      return this.lookalikeAudience.engagements.length
    },
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },

    selectedAudience(value) {
      this.lookalikeAudience.audience = value
    },
    async prefetchLookalikeDependencies() {
      this.loading = true
      await this.getAllEngagements()
      await this.getAllAudiences()
      this.loading = false
    },
  },
  methods: {
    ...mapActions({
      getAllEngagements: "engagements/getAll",
      getAllAudiences: "audiences/getAll",
      createLookalikeAudience: "audiences/addLookalike",
    }),

    async createLookalike() {
      let engagementIds = this.lookalikeAudience.engagements.map(
        (selectedEngagement) => selectedEngagement.id
      )
      let payload = {
        audience_id: this.lookalikeAudience.audience.id,
        name: this.lookalikeAudience.name,
        audience_size_percentage: this.lookalikeAudience.value,
        engagement_ids: engagementIds,
      }
      await this.createLookalikeAudience(payload)
      this.$emit("onCreate")
      this.onBack()
    },

    reset() {
      this.lookalikeAudience.value = 5
      this.selectAudience = null
      this.lookalikeAudience.engagements = []
      this.$refs.lookalikeForm.$children[0].$children[0].reset()
    },

    detachEngagement(index) {
      this.lookalikeAudience.engagements.splice(index, 1)
    },

    onBack() {
      this.reset()
      this.localToggle = false
      this.$emit("onBack")
    },
    async prefetchLookalikeDependencies() {
      this.loading = true
      await this.getAllEngagements()
      await this.getAllAudiences()
      this.loading = false
    },
  },
}
</script>

<style lang="scss" scoped>
.lookalike-drawer {
  .lookalike-form {
    ::v-deep .v-input {
      .v-input__control {
        .v-input__slot {
          min-height: 40px;
          fieldset {
            color: var(--v-black-lighten3) !important;
            border-width: 1px !important;
          }
          input::placeholder {
            color: var(--v-black-lighten3) !important;
          }
        }
      }
    }
    .dropdown-select-activator,
    .delivered-audience-selection {
      ::v-deep .v-input__control {
        .v-input__slot {
          input::placeholder {
            color: var(--v-black-darken1) !important;
          }
        }
        .v-text-field__details {
          display: none;
        }
      }
    }
  }
}
</style>
