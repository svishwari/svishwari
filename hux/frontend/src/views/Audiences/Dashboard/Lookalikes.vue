<template>
  <div class="lookalike-wrapper">
    <div v-if="false" class="rounded-sm lookalikes box-shadow-none">
      <div class="header d-flex mx-6 px-3 py-3">
        <span class="float-left text-h3 black-base pt-5"> Lookalikes </span>
        <v-spacer> </v-spacer>
        <span class="float-right pt-5">
          <hux-icon type="plus" :size="12" color="primary" class="mr-4 mb-2" />
          <hux-icon type="lookalike" :size="24" class="mr-2" />
        </span>
      </div>
      <div class="lookialike-destination mx-6 my-6">
        <v-card class="rounded-sm status-card mr-2 box-shadow-none">
          <v-card-title class="d-flex pa-2">
            <logo type="facebook" :size="22"></logo>
            <span class="mx-2 float-left"> Facebook </span>
          </v-card-title>
          <v-list dense class="" :height="52">
            <v-list-item>
              <icon type="lookalike" :size="20" class="mr-2" />
              <span>Facebook LAL - Sum...</span>
              <v-spacer> </v-spacer>
              <span>12.6 K </span>
            </v-list-item>
          </v-list>
        </v-card>
      </div>
      <div class="lookialike-destination mx-6 my-6">
        <v-card class="rounded-sm status-card mr-2 box-shadow-none">
          <v-card-title class="d-flex pa-2">
            <logo type="facebook" :size="22"></logo>
            <span class="mx-2"> Facebook </span>
          </v-card-title>
          <v-list dense class="" :height="52">
            <v-list-item>
              <icon type="lookalike" :size="20" class="mr-2" />
              <span>Facebook LAL - Sum...</span>
              <v-spacer> </v-spacer>
              <span>12.6 K </span>
            </v-list-item>
          </v-list>
        </v-card>
      </div>
    </div>
    <div v-if="true" class="no-lookalike">
      <metric-card
        class=""
        title="Lookalikes"
        :height="156"
        :interactable="false"
        title-class="text-h3"
        iconType="Lookalikes"
        titleIcon="lookalike"
      >
        <template #subtitle-extended>
          <div class="black--text text--lighten-4 mt-4 text-body-2">
            No lookalike audiences have been created. Once this audience has
            been delivered to an advertising destination, you can configure a
            lookalike audience in that destination.
          </div>
        </template>
      </metric-card>
    </div>
  </div>
</template>

<script>
import HuxIcon from "@/components/common/Icon.vue"
import Logo from "@/components/common/Logo.vue"
import Icon from "@/components/common/Icon.vue"
import MetricCard from "@/components/common/MetricCard"

export default {
  name: "Lookalikes",
  components: { HuxIcon, Logo, Icon, MetricCard },
  props: {},
  data() {
    return {}
  },
  computed: {},
}
</script>

<style lang="scss" scoped>
.lookalike-wrapper {
  .lookalikes {
    .header {
      height: 40px;
    }
    .lookialike-destination {
      .rounded-sm {
        border: 1px solid var(--v-black-lighten2);
        border-radius: 12px !important;
        .v-card__title {
          background: var(--v-primary-lighten1);
        }
      }
    }
  }
  .no-lookalike {
    background: var(--v-primary-lighten1);
  }
}
::v-deep .titleColor {
  color: var(--v-black-base) !important;
}
</style>
