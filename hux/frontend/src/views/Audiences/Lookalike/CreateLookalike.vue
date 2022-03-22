<template>
  <page class="white add-eng-wrap" max-width="953px">
    <div class="steps-wrap">
      <v-form ref="lookalikeForm" v-model="isFormValid">
        <div class="lookalike-form px-4 py-3">
          <div class="d-flex align-center">
            <h3 class="text-h1 black--text text--base">
             Create a lookalike audience
            </h3>
          </div>
          <div class="text-body-1 black--text text--base pb-8">
            Creating a lookalike audience will create a one-off new audience of
            the latest successful delivery of {{ audience.source_name }} in the
            selected destination.
          </div>
          <text-field
            v-model="lookalikeAudience.name"
            class="input-audi"
            label-text="Lookalike audience name"
            placeholder="Facebook Lookalike - <Seedaudiencename>"
            :rules="lookalikeNameRules"
            required
          />

          <div class="text-body-2 black--text text--base mb-1 ml-1">
            Destination for this lookalike audience
          </div>
          <hux-dropdown
            :label="lookalikeAudience['selectDestination']"
            :selected="lookalikeAudience['selectDestination']"
            :items="destinationDropDownList"
            min-width="665"
            drop-icon="facebook"
            class="delivered-audience-selection pb-6 ml-n2 mr-n3 mt-n2"
            background-color="white"
            @on-select="onSelectMenuItem"
          />
          <div class="text-body-1 black--text text--base pb-1">
            Set the reach for this lookalike audience
          </div>
          <look-alike-slider v-model="lookalikeAudience.value" class="mr-6" />
          <div class="info-widget d-flex mt-2 pa-3">
            <div class="bulb">
              <icon type="FAB-bulb" :size="21" class="mt-1" />
            </div>
            <div class="description ml-4 text-body-1 black-base text-left">
              The lookalike audience reach ranges from 1% to 10% of the combined
              population of the selected locations. A 1% lookalike audience
              incorporate people most similar to your lookalike source.
              Increasing the percentage creates a larger, broader audience.
            </div>
          </div>
        </div>
      </v-form>
    </div>
    <hux-footer>
      <template #left>
        <hux-button
          size="large"
          is-tile
          variant="white"
          height="40"
          class="btn-border box-shadow-none"
          @click.native="$router.go(-1)"
        >
          <span class="primary--text">Cancel &amp; return</span>
        </hux-button>
      </template>
      <template #right>
        <hux-button
          is-tile
          color="primary"
          height="40"
          :is-disabled="!isFormValid"
          @click="createLookalike()"
        >
          Create
        </hux-button>
      </template>
    </hux-footer>
  </page>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Page from "@/components/Page.vue"
import LookAlikeSlider from "@/components/common/LookAlikeSlider"
import TextField from "@/components/common/TextField"
import Icon from "@/components/common/Icon.vue"
import HuxButton from "@/components/common/huxButton"
import HuxFooter from "@/components/common/HuxFooter.vue"
import HuxDropdown from "@/components/common/HuxDropdown.vue"

export default {
  name: "CreateLookalike",
  components: {
    Page,
    Icon,
    TextField,
    LookAlikeSlider,
    HuxButton,
    HuxFooter,
    HuxDropdown,
  },
  props: {},
  data() {
    return {
      loading: false,
      toggleDropDown: false,
      audienceData: {},
      lookalikeAudience: {
        name: null,
        value: 5,
        selectDestination: "Facebook",
        engagements: [],
      },
      isFormValid: false,
      lookalikeNameRules: [(v) => !!v || "Lookalike audience name is required"],
    }
  },
  computed: {
    ...mapGetters({
      getAudience: "audiences/audience",
    }),
    destinationDropDownList() {
      return [
        {
          name: "Facebook",
          value: "facebook",
          type: "facebook",
        },
      ]
    },
    audience() {
      return this.audienceData
    },
  },

  async mounted() {
    await this.loadAudienceById()
  },
  methods: {
    ...mapActions({
      getAudienceById: "audiences/getAudienceById",
      createLookalikeAudience: "audiences/addLookalike",
    }),

    async loadAudienceById() {
      await this.getAudienceById(this.$route.params.id)
      const _getAudience = this.getAudience(this.$route.params.id)
      if (_getAudience) {
        this.audienceData = JSON.parse(JSON.stringify(_getAudience))
      }
    },

    onSelectMenuItem(item) {
      this.lookalikeAudience["selectDestination"] = item.name
    },

    async createLookalike() {
      let payload = {
        audience_id: this.audienceData.id,
        name: this.lookalikeAudience.name,
        audience_size_percentage: this.lookalikeAudience.value,
      }
      let response = await this.createLookalikeAudience(payload)
      this.$router.push({
        name: "AudienceInsight",
        params: { id: response.id },
      })
    },

    reset() {
      this.lookalikeAudience.name = ""
      this.lookalikeAudience.value = 5
    },
    onBack() {
      this.reset()
    },
  },
}
</script>
<style lang="scss" scoped>
.add-eng-wrap {
  .steps-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
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
    .info-widget {
      background: var(--v-yellow-lighten1);
      border: 1px solid var(--v-primary-lighten1);
      text-align: justify;
    }
  }
}
::v-deep .text-label {
  margin-left: 4px !important;
}
::v-deep .v-text-field > .v-input__control > .v-input__slot > .v-text-field__slot {
  padding: 0px 4px !important;
}
::v-deep .v-slider__thumb:before {
  opacity: 0 !important;
}
.input-audi {
  width: 77% !important;
}
</style>
