<template>
  <div class="background-color-change">
    <page-header data-e2e="client-header" :header-height="110">
      <template #left>
        <div>
          <breadcrumb
            :items="[
              {
                text: 'Client projects',
                icon: 'clients',
              },
            ]"
          />
        </div>
        <div class="text-subtitle-1 font-weight-regular">
          Get started and access your clients’ Hux journey!
        </div>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />

    <v-row v-if="!loading" class="pa-11" data-e2e="clients-list">
      <descriptive-card
        width="255"
        height="225"
        icon="demo-client"
        title="Client"
        description=""
        logo-option="true"
        data-e2e="client"
        logo-size="60"
        logo-box-padding="0px"
        top-right-adjustment="mt-6 mr-0"
        interactable="false"
        no-description
      >
        <template slot="default">
          <v-chip color="yellow" text-color="black" class="height-pill mt-n2">
            Admin access
          </v-chip>
        </template>
      </descriptive-card>
    </v-row>
  </div>
</template>

<script>
import Breadcrumb from "@/components/common/Breadcrumb"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"
import PageHeader from "@/components/PageHeader"

export default {
  name: "ClientPanel",

  components: {
    Breadcrumb,
    DescriptiveCard,
    PageHeader,
  },

  data() {
    return {
      loading: false,
    }
  },
}
</script>

<style lang="scss" scoped>
.height-pill {
  height: 20px !important;
  font-weight: 600;
  font-size: 12px;
  letter-spacing: 0.2px;
}
.background-color-change {
  background: var(--v-black-lighten2);
}
</style>
