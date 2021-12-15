<template>
  <div class="tabs-wrapper">
    <v-tabs v-model="tabOption" class="mt-8">
      <v-tabs-slider color="primary" class="sliderCss"></v-tabs-slider>
      <div class="d-flex">
        <v-tab
          key="modules"
          class="pa-2 mr-3 text-h3 black--text text--lighten-4"
          color
        >
          Modules &amp; Solutions
        </v-tab>
        <v-tab key="team" class="text-h3 black--text text--lighten-4">
          Team members
        </v-tab>
      </div>
    </v-tabs>
    <v-tabs-items v-model="tabOption" class="mt-2">
      <v-tab-item key="modules">
        <module-solutions />
      </v-tab-item>
      <v-tab-item key="team">
        <team-members />
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import { mapGetters } from "vuex"

import ModuleSolutions from "../Configuration/ModuleSolutions/ModuleSolutions.vue"
import TeamMembers from "../Configuration/TeamMembers/TeamMembers.vue"

export default {
  name: "ConfigTabs",
  components: { ModuleSolutions, TeamMembers },
  data() {
    return {
      tabOption: 0,
    }
  },
  computed: {
    ...mapGetters({}),
  },
}
</script>

<style lang="scss" scoped>
.sliderCss {
  position: absolute;
  top: 2px;
}
::v-deep .v-tabs .v-tabs-bar .v-tabs-bar__content .v-tab {
  color: var(--v-black-lighten4) !important;
}
</style>
