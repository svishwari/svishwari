<template>
  <div class="engagements-wrap grey lighten-5">
    <PageHeader>
      <template slot="left">
        <Breadcrumb :items="breadcrumbItems" />
      </template>
    </PageHeader>
    <PageHeader class="top-bar" :headerHeight="71">
      <template slot="left">
        <v-icon medium :disabled="true">mdi-filter-variant</v-icon>
        <v-icon medium :disabled="true" class="pl-6">mdi-magnify</v-icon>
      </template>

      <template slot="right">
        <v-icon medium :disabled="true" color="primary refresh"
          >mdi-refresh</v-icon
        >
        <router-link
          :to="{ name: 'AudienceConfiguration' }"
          class="text-decoration-none"
          append
        >
          <huxButton
            ButtonText="Engagement"
            icon="mdi-plus"
            iconPosition="left"
            variant="primary"
            size="large"
            isTile
            class="ma-2 font-weight-regular no-shadow mr-0"
          ></huxButton>
        </router-link>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <v-row class="pt-3 pb-7 pl-3" v-if="!loading">
      <EmptyPage>
        <template #icon>mdi-alert-circle-outline</template>
        <template #title>Oops! There’s nothing here yet</template>
        <template #subtitle>
          Plan your engagement ahead of time. You can create the <br />
          framework first then add audiences later. <br />
          Begin by selecting the button below.
        </template>
        <template #button>
          <router-link
            :to="{ name: 'AudienceConfiguration' }"
            class="route-link text-decoration-none"
            append
          >
            <huxButton
              ButtonText="Engagement"
              icon="mdi-plus"
              iconPosition="left"
              variant="primary"
              size="large"
              isTile
              class="ma-2 font-weight-regular"
            ></huxButton>
          </router-link>
        </template>
      </EmptyPage>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import PageHeader from "@/components/PageHeader"
import EmptyPage from "@/components/common/EmptyPage"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxDataTable from "../../components/common/dataTable/HuxDataTable.vue"
import Avatar from "../../components/common/Avatar.vue"
import Size from "../../components/common/huxTable/Size.vue"
import TimeStamp from "../../components/common/huxTable/TimeStamp.vue"
import MenuCell from "../../components/common/huxTable/MenuCell.vue"
export default {
  name: "engagements",
  components: {
    PageHeader,
    Breadcrumb,
    huxButton,
    EmptyPage,
    HuxDataTable,
    Avatar,
    Size,
    TimeStamp,
    MenuCell,
  },
  data() {
    return {
       breadcrumbItems: [
        {
          text: "Engagements",
          disabled: true,
          icon: "engagements",
        },
      ],
      loading: false,
    }
  },
}
</script>

<style lang="scss" scoped>
.engagements-wrap {
  ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
  }
  .page-header--wrap {
    box-shadow: 0px 1px 1px -1px var(--v-lightGrey-base),
      0px 1px 1px 0px var(--v-lightGrey-base),
      0px 1px 2px 0px var(--v-lightGrey-base) !important;
  }
  .top-bar {
    margin-top: 1px;
    .v-icon--disabled {
      color: var(--v-lightGrey-base) !important;
      font-size: 24px;
    }
    .text--refresh {
      margin-right: 10px;
    }
  }
  .hux-data-table {
    margin-top: 1px;
  }
  ::v-deep .menu-cell-wrapper :hover .action-icon {
    display: initial;
  }
}
</style>
