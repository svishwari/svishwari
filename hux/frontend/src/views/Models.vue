<template>
  <div>
    <page-header>
      <template slot="left">
        <breadcrumb
          :items="[
            {
              text: 'Models',
              disabled: false,
              icon: 'mdi-tune-vertical-variant',
            },
          ]"
        />
      </template>
    </page-header>
    <v-row class="pa-14">
      <DescriptiveCard
        icon="model-unsubscribe"
        title="Propensity to Unsubscribe"
        description="Propensity of a customer making a purchase after receiving an email."
      >
        <template slot="top">
          <Status status="pending" collapsed class="d-flex" />
        </template>

        <template slot="default">
          <p class="text-caption gray--text">Sarah Miller</p>

          <div class="d-flex justify-center mb-6">
            <CardStat label="Version" value="0.02" stat-class="border-0">
              <div class="mb-3">
                Trained date<br />
                12/22/2021 at 12:45pm
              </div>
              <div class="mb-3">
                Fulcrum date<br />
                12/20/2021
              </div>
              <div class="mb-3">
                Lookback period (days)<br />
                365
              </div>
              <div>
                Lookback period (days)<br />
                60
              </div>
            </CardStat>
            <CardStat label="Last trained" value="2 hrs ago">12:45pm</CardStat>
          </div>
        </template>
      </DescriptiveCard>
    </v-row>
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Status from "@/components/common/Status"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"
import CardStat from "@/components/common/Cards/Stat"

export default {
  name: "models",

  components: {
    PageHeader,
    Breadcrumb,
    Status,
    DescriptiveCard,
    CardStat,
  },
}
</script>
