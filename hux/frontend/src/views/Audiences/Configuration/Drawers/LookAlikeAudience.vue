<template>
  <Drawer
    v-model="localToggle"
    :loading="loading"
    class="look-alike-drawer"
    @onClose="onBack"
  >
    <template #header-left>
      <div class="d-flex align-center">
        <Icon type="look-alike" :size="32" color="secondary" class="mr-2" />
        <h3 class="text-h3">Create a lookalike audience in Facebook</h3>
      </div>
    </template>

    <template #default>
      <v-form v-model="isFormValid" ref="lookAlikeForm">
        <div class="look-alike-form px-4 py-3">
          <div class="text-h6 darkGrey--text pb-8">
            Creating a lookalike audience will create a one-off new audience in
            Facebook.
          </div>
          <TextField
            v-model="lookAlikeAudience.name"
            class="pb-3"
            labelText="Lookalike audience name"
            placeholder="What is the name for this new lookalike audience?"
            :rules="lookAlikeNameRules"
            required
          />

          <div class="text-caption darkGrey--text">
            Audience to create a lookalike from
          </div>
          <v-select
            v-model="selectAudience"
            :items="fbDeliveredAudiences"
            dense
            outlined
            class="delivered-audience-selection pb-10"
            background-color="white"
            append-icon="mdi-chevron-down"
            required
          />

          <div class="text-caption darkGrey--text">
            Attach this audience to an engagement - you must have at least one
          </div>

          <HuxDropDownSearch
            v-model="lookAlikeAudience.engagements"
            :toggleDropDown="toggleDropDown"
            @onToggle="(val) => (toggleDropDown = val)"
            :items="engagements"
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
          </HuxDropDownSearch>

          <v-chip
            v-for="(item, index) in lookAlikeAudience.engagements"
            :close="selectedEngagementsLength > 1"
            small
            class="mr-2 my-2 font-weight-semi-bold"
            text-color="primary"
            color="pillBlue"
            close-icon="mdi-close"
            @click:close="detachEngagement(index)"
            :key="item.id"
          >
            {{ item.name }}
          </v-chip>

          <div class="text-caption darkGrey--text pt-9 pb-1">
            The reach for this lookalike audience
          </div>
          <div class="text-caption gray--text pb-1">
            Audience reach ranges from 1% to 10% of the combined population of
            your selected locations. A 1% lookalike consists of the people most
            similar to your lookalike source. Increasing the percentage creates
            a bigger, broader audience.
          </div>

          <LookAlikeSlider v-model="lookAlikeAudience.value" />
        </div>
      </v-form>
    </template>

    <template #footer-right>
      <div class="d-flex align-baseline">
        <HuxButton
          variant="primary"
          isTile
          height="40"
          class="ma-2"
          :isDisabled="!(isFormValid && selectedEngagementsLength !== 0)"
          @click="creatLookAlike()"
        >
          Create &amp; deliver
        </HuxButton>
      </div>
    </template>

    <template #footer-left>
      <div class="d-flex align-baseline">
        <HuxButton
          variant="white"
          isTile
          width="80"
          height="40"
          class="ma-2 drawer-back"
          @click="onBack()"
        >
          Back
        </HuxButton>
      </div>
    </template>
  </Drawer>
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

  computed: {
    ...mapGetters({
      engagements: "engagements/list",
      audiences: "audiences/list",
    }),

    selectAudience: {
      get() {
        return this.selectedAudience
      },
      set(value) {
        this.lookAlikeAudience.audience = value
      },
    },
    fbDeliveredAudiences() {
      let filteredAudience = this.audiences.filter((audience) => {
        let isOneOfDestinationFacebook = false
        if (audience.destinations) {
          isOneOfDestinationFacebook =
            audience.destinations.findIndex(
              (each) => each.type === "Facebook"
            ) !== -1
              ? true
              : false
        }
        return isOneOfDestinationFacebook
      })

      return filteredAudience.map((each) => {
        return {
          text: each.name,
          value: each,
        }
      })
    },

    selectedEngagementsLength() {
      return this.lookAlikeAudience.engagements.length
    },
  },

  data() {
    return {
      loading: false,
      localToggle: false,
      toggleDropDown: false,
      lookAlikeAudience: {
        name: null,
        value: 5,
        audience: null,
        engagements: [],
      },
      isFormValid: false,
      lookAlikeNameRules: [(v) => !!v || "Lookalike audience name is required"],
    }
  },

  methods: {
    ...mapActions({
      getAllEngagements: "engagements/getAll",
      getAllAudiences: "audiences/getAll",
    }),

    creatLookAlike() {
      //TODO: make a API call here HUS-649
      this.onBack()
    },

    reset() {
      this.lookAlikeAudience.value = 5
      this.selectAudience = null
      this.lookAlikeAudience.engagements = []
      this.$refs.lookAlikeForm.$children[0].$children[0].reset()
    },

    detachEngagement(index) {
      this.lookAlikeAudience.engagements.splice(index, 1)
    },

    onBack() {
      this.reset()
      this.localToggle = false
      this.$emit("onBack")
    },
  },

  async mounted() {
    this.loading = true
    await this.getAllEngagements()
    await this.getAllAudiences()
    this.loading = false
  },

  props: {
    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },

    selectedAudience: {
      required: true,
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
      this.lookAlikeAudience.audience = value
    },
  },
}
</script>

<style lang="scss" scoped>
.look-alike-drawer {
  .look-alike-form {
    ::v-deep .v-input {
      .v-input__control {
        .v-input__slot {
          min-height: 40px;
          fieldset {
            color: var(--v-lightGrey-base) !important;
            border-width: 1px !important;
          }
          input::placeholder {
            color: var(--v-lightGrey-base) !important;
          }
        }
      }
    }
    .dropdown-select-activator,
    .delivered-audience-selection {
      ::v-deep .v-input__control {
        .v-input__slot {
          input::placeholder {
            color: var(--v-gray-base) !important;
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
