<template>
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
    <div class="ma-1">
      <score-card :width="150" :height="90" title="Transparency" :value="73" />
    </div>
    <div class="ma-1">
      <score-card :width="150" :height="90" title="Humanity" :value="71">
        <template #stack-bar-chart>
          <single-horizontal-stack-bar-chart
            :width="81"
            :height="6"
            :show-percentage="false"
          />
        </template>
      </score-card>
    </div>
    <div>
      <single-horizontal-stack-bar-chart
        :width="180"
        :height="6"
        :show-percentage="true"
      />
    </div>
  </page>
</template>

<script>
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader.vue"
import scoreCard from "@/components/common/scoreCard/scoreCard.vue"
import SingleHorizontalStackBarChart from "@/components/common/Charts/SingleHorizontalStackBarChart/SingleHorizontalStackBarChart.vue"

export default {
  name: "HXTrustID",
  components: {
    Page,
    PageHeader,
    Breadcrumb,
    scoreCard,
    SingleHorizontalStackBarChart,
  },
  data() {
    return {
      loading: false,
    }
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
}
</style>
