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
        v-for="client in clients"
        :key="client.id"
        width="255"
        height="225"
        :icon="client.icon"
        :title="client.name"
        description=""
        logo-option="true"
        data-e2e="client"
        logo-size="44"
        logo-box-padding="8px"
        top-right-adjustment="mt-6 mr-0"
        interactable="false"
        to="home"
        no-description
      >
        <template slot="default">
          <v-chip color="yellow" text-color="black" class="height-pill mt-n2">
            {{ accessLevel(client.access_level) }} access
          </v-chip>
        </template>
      </descriptive-card>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

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

  computed: {
    ...mapGetters({
      getClients: "clients/getClients",
    }),

    clients() {
      return this.getClients.length ? this.getClients : []
    },
  },

  async mounted() {
    this.loading = true
    try {
      await this.getClientProjects()
    } finally {
      this.loading = false
    }
  },

  methods: {
    ...mapActions({
      getClientProjects: "clients/getClientProjects",
    }),
    accessLevel(lvl) {
      switch (lvl) {
        case "admin":
          return "Admin"

        case "editor":
          return "Edit"

        default:
          return "View-only"
      }
    },
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
