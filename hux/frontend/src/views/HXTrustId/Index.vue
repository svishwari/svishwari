<template>
  <div>
    <page max-width="100%" class="hx-trust-id-wrapper">
      <template #header>
        <page-header
          class="page-header py-5"
          header-min-height="110"
          header-max-height="120"
        >
          <template #left>
            <div>
              <breadcrumb
                :items="[
                  {
                    text: 'HX TrustID',
                    disabled: true,
                    href: '/hx-trustid',
                    icon: 'hx-trustid-colored',
                    iconSize: 36,
                    iconColor: 'black',
                    iconColorVariant: 'base',
                  },
                ]"
              />
            </div>
            <div class="text-subtitle-1 font-weight-regular pt-0 pl-0">
              Measure the signals of trust, predict how trust sentiment will
              impact customer &nbsp; employee behaviors, and identify actions to
              (re)build trust.
            </div>
          </template>
        </page-header>
        <v-progress-linear :active="loading" :indeterminate="loading" />
      </template>
      <template>
        <div class="d-flex">
          <div>
            <score-card :width="150" :height="90" />
          </div>
          <div>
            <v-btn class="ml-5" @click="filterToggle()"> helllo </v-btn>
          </div>
          <div class="ml-auto segment-drawer">
            <add-segment-drawer
              ref="filters"
              v-model="isFilterToggled"
              view-height="calc(100vh - 180px)"
            />
          </div>
        </div>
      </template>
    </page>
  </div>
</template>

<script>
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader.vue"
import scoreCard from "@/components/common/scoreCard/scoreCard.vue"
import AddSegmentDrawer from "@/views/HXTrustId/Drawers/AddSegmentDrawer.vue"

export default {
  name: "HXTrustID",
  components: {
    Page,
    PageHeader,
    Breadcrumb,
    scoreCard,
    AddSegmentDrawer,
  },
  data() {
    return {
      loading: false,
      isFilterToggled: false,
    }
  },
  methods: {
    filterToggle() {
      this.isFilterToggled = !this.isFilterToggled
    },
  },
}
</script>

<style lang="scss" scoped>
.hx-trust-id-wrapper {
  ::v-deep .v-breadcrumbs {
    li {
      font-family: Open Sans Light;
      font-size: 28px;
      font-style: normal;
      font-weight: 400 !important;
      line-height: 40px;
      letter-spacing: 0px;
      text-align: left;
    }
  }
  .overview-card {
    border-radius: 12px !important;
  }
  .segment-drawer {
    margin-top: -30px;
    margin-right: -30px;
  }
}
::v-deep .hux-filters-drawer {
  width: 320px !important;
}
::v-deep .header-height-fix {
  height: 70px !important;
}
::v-deep .wrapper {
  width: 320px !important;
}
</style>
