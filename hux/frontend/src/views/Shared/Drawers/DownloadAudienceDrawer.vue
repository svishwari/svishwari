<template>
  <drawer v-model="localToggle" :width="640" :loading="loading">
    <template #header-left>
      <h3 class="text-h2">Download data</h3>
    </template>
    <template #default>
      <div class="mx-6 my-5">
        <template v-if="piiAccess">
          <span class="text-h3">Generic .csv</span>
          <div class="body-1 mt-2 mb-5">
            <span>Download a generic .csv file of this audience.</span>
            <span class="orange-color"><i>This will include PII data</i></span>
          </div>
          <v-checkbox
            v-model="selectedGeneral"
            color="primary lighten-6"
            class="text--base-1 decrease-margin"
          >
            <template v-slot:label>
              <span class="body-1 color-darken">{{
                checkboxData[0].title
              }}</span>
            </template>
          </v-checkbox>
        </template>
        <template v-else>
          <div class="background-set px-5 py-3 d-flex">
            <icon type="light_bulb" size="84" class="md-2 fix-bulb" />
            <div class="body-1">
              You currently do not have access to view PII, thus cannot download
              this audience data as a generic .csv. Please reach out to your Hux
              Admin to request access.
            </div>
          </div>
        </template>
      </div>
      <v-divider class="mx-5" />
      <div class="mx-6 my-5">
        <span class="text-h3">Hashed .csv</span>
        <div class="body-1 mt-2 mb-5">
          <span v-if="piiAccess"
            >Download hashed customer data files that are preformatted and ready
            to be manually uploaded directly to Amazon and Google,
            respectively.</span
          >
          <span v-else
            >Download hashed customer data files that are preformatted and ready
            for manual uploads specific to Amazon and Google. This file will
            include encrypted PII data.</span
          >
        </div>
        <v-checkbox
          v-for="data in checkboxData[1]"
          :key="data.id"
          v-model="selectedHashed[data.id]"
          multiple
          color="primary lighten-6"
          class="text--base-1 decrease-margin"
        >
          <template v-slot:label>
            <span class="body-1 color-darken"
              >.csv for
              <logo :type="data.type" size="18" class="down-allign" />
              {{ data.title }}</span
            >
          </template>
        </v-checkbox>
      </div>
    </template>

    <template #footer-left>
      <hux-button
        variant="white"
        size="large"
        :is-tile="true"
        class="mr-2 btn-border box-shadow-none"
        @click="closeDrawer"
      >
        <span class="primary--text">Cancel</span>
      </hux-button>
    </template>
    <template #footer-right>
      <hux-button
        variant="primary"
        size="large"
        :is-tile="true"
        :is-disabled="false"
      >
        Download
      </hux-button>
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Drawer from "@/components/common/Drawer.vue"
import HuxButton from "@/components/common/huxButton.vue"
import Logo from "@/components/common/Logo.vue"
import Icon from "@/components/common/Icon.vue"
export default {
  name: "DownloadAudienceDrawer",

  components: {
    Drawer,
    HuxButton,
    Logo,
    Icon,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },

    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      localToggle: false,
      loading: false,
      checkboxData: [
        {
          title: ".csv",
        },
        [
          {
            id: 0,
            title: "Amazon",
            type: "amazon-advertising",
          },
          {
            id: 1,
            title: "Google",
            type: "google-ads",
          },
        ],
      ],
      selectedHashed: [],
      selectedGeneral: false,
    }
  },

  computed: {
    ...mapGetters({
      getPiiAccess: "users/getPiiAccess",
    }),
    piiAccess() {
      return this.getPiiAccess
    },
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
    ...mapActions({}),
    closeDrawer() {
      this.localToggle = false
      this.localSelectedAudiences = this.value
    },
  },
}
</script>

<style scoped>
.orange-color {
  color: orange;
}
.down-allign {
  margin-bottom: -4px;
}
.decrease-margin {
  margin-top: -10px;
  margin-bottom: -20px;
}
.color-darken {
  color: var(--v-black-base) !important;
}
.background-set {
  background: #fffcf2;
}
.fix-bulb {
  margin-top: -26px;
  margin-left: -8px;
  margin-right: 7px;
}
</style>
