<template>
  <div class="lookalike-wrapper">
    <div v-if="isDataExists" class="rounded-sm lookalikes box-shadow-none">
      <div class="header d-flex mx-6 pr-3 py-5">
        <hux-icon type="lookalike" :size="24" class="mr-2" />
        <span class="float-left text-h3 black--text text--base">
          Lookalikes
        </span>
      </div>
      <div
        v-for="data in lookalikeData"
        :key="data.id"
        class="lookialike-destination mx-6 my-6"
      >
        <v-card class="rounded-sm status-card mr-2 box-shadow-none">
          <v-card-title class="d-flex pa-2">
            <logo
              :type="data.delivery_platform_type"
              :size="26"
              class="ml-2"
            ></logo>
            <span class="mx-2 float-left">
              {{ data.delivery_platform_name }}
            </span>
          </v-card-title>
          <v-list dense class="" :height="52">
            <v-list-item>
              <icon type="lookalike" :size="20" class="mr-2" />
              <router-link
                :to="`/audiences/${data.id}/insight`"
                class="text-decoration-none menu-link"
                append
              >
                <span class="text-body-1 primary--text">{{ data.name }}</span>
              </router-link>
              <v-spacer> </v-spacer>
              <span class="text-body-1">
                <size :value="data.size" />
              </span>
            </v-list-item>
          </v-list>
        </v-card>
      </div>
      <v-list
        dense
        class="add-lookalike add-lookalike-width mx-6 mb-6"
        :height="22"
      >
        <v-list-item>
          <hux-icon type="plus" :size="16" color="primary" class="mr-2" />
          <v-btn
            text
            min-width="7rem"
            height="2rem"
            class="primary--text text-body-1"
            data-e2e="drawerToggle"
            @click="$emit('openCreateLookalike')"
          >
            A lookalike
          </v-btn>
        </v-list-item>
      </v-list>
    </div>
    <div v-if="!isDataExists && !lookalikeable" class="no-lookalike">
      <metric-card
        class=""
        title="Lookalikes"
        :height="156"
        :interactable="false"
        title-class="text-h3"
        icon-type="Lookalikes"
        title-icon="lookalike"
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

    <div v-if="!isDataExists && lookalikeable" class="no-lookalike mx-6 my-6">
      <metric-card
        title="Lookalikes"
        :height="230"
        :interactable="false"
        title-class="text-h3"
        icon-type="Lookalikes"
        title-icon="lookalike"
      >
        <template #extra-item>
          <div class="black--text text--lighten-4 mt-4 mb-3 text-body-2">
            This seed audience has no lookalike audiences.
            <br />
            <br />
            Create a lookalike audience in an advertising platform by clicking
            “+ A lookalike” below.
          </div>
          <v-list class="add-lookalike no-data-width" :height="22">
            <v-list-item>
              <hux-icon
                type="plus"
                :size="16"
                color="primary"
                class="mr-4 ml-2"
              />
              <v-btn
                text
                min-width="7rem"
                height="2rem"
                class="primary--text text-body-1"
                data-e2e="drawerToggle"
                @click="$emit('openCreateLookalike')"
              >
                A lookalike
              </v-btn>
            </v-list-item>
          </v-list>
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
import Size from "@/components/common/huxTable/Size.vue"

export default {
  name: "Lookalikes",
  components: { HuxIcon, Logo, Icon, MetricCard, Size },
  props: {
    lookalikeData: {
      type: Array,
      required: false,
      default: () => [],
    },
    lookalikeable: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    isDataExists() {
      return this.lookalikeData.length > 0 ? true : false
    },
  },
}
</script>

<style lang="scss" scoped>
.lookalike-wrapper {
  background-color: var(--v-primary-lighten1) !important;
  box-sizing: border-box;
  border-radius: 5px !important;
  border: 1px solid var(--v-black-lighten2);
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
    border-radius: 5px !important;
    ::v-deep .metric-card-wrapper {
      border: 0 !important;
      .titleColor {
        svg {
          padding-top: 0 !important;
          width: 24px !important;
          height: 24px !important;
        }
      }
    }
  }
}
::v-deep .titleColor {
  color: var(--v-black-base) !important;
}
::v-deep .metric-card-wrapper {
  padding: 20px 24px !important;
  border-radius: 5px !important;
}
.add-lookalike {
  height: 60px !important;
  display: inline-table;
  background: var(--v-white-base);
  border: 1px solid var(--v-black-lighten2);
  border-radius: 5px;
}
.add-lookalike-width {
  width: 90%;
}
.no-data-width {
  width: 100%;
}
</style>
