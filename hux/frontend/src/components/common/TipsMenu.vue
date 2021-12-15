<template>
  <span class="cursor-pointer mr-6 icon-bulb" :style="{ right: rightPosition }">
    <drop-menu
      :min-midth="300"
      :max-width="353"
      :close-on-click="false"
      content-class="tips-menu"
      class="drop-menu-div"
    >
      <template #menuActivator="activatorVal">
        <span v-if="!activatorVal.activatorVal">
          <icon :type="'FAB_circle_bulb'" :size="56" />
        </span>
        <span v-else><icon type="FAB_circle_cross" :size="56" /></span>
      </template>
      <template #menuHeader>
        <div class="header-menu d-flex text-body-1 pt-5 pb-5 pr-4 pl-4">
          <span>
            <icon type="FAB-bulb" :size="24" />
          </span>
          <span class="ml-2 mt-1"> {{ header }} </span>
        </div>
      </template>
      <template #menuBody>
        <div class="tips-menu-body">
          <v-expansion-panels v-model="panel" multiple>
            <v-expansion-panel v-for="(data, i) in panelListItems" :key="i">
              <v-expansion-panel-header>
                <template v-slot:actions>
                  <div></div>
                </template>
                <span class="header d-flex">
                  <span
                    class="icon-left"
                    :class="panel.includes(i) ? 'rotate-icon-90' : ''"
                  >
                    <icon :type="'side-arrow'" :size="11" color="primary" />
                  </span>
                  <span class="text-body-1 primary--text">
                    {{ data.title }}
                  </span>
                </span>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <div class="text-body-1" v-html="data.text"></div>
                <br />
                <div
                  v-if="data.textPart"
                  class="text-body-1"
                  v-html="data.textPart"
                ></div>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
      </template>
    </drop-menu>
  </span>
</template>

<script>
import Icon from "@/components/common/Icon"
import DropMenu from "@/components/common/DropMenu"

export default {
  name: "TipsMenu",
  components: {
    Icon,
    DropMenu,
  },
  props: {
    panelListItems: {
      type: Array,
      required: true,
    },
    header: {
      type: String,
      required: false,
      default: "",
    },
    rightPosition: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      panelIndex: false,
      panel: [],
    }
  },
}
</script>
<style lang="scss" scoped>
.icon-bulb {
  position: absolute;
  bottom: -2.5rem;
  right: 0;
  z-index: 2;
}
.drop-menu-div {
  z-index: 1;
}
.tips-menu {
  .header-menu {
    background: var(--v-yellow-lighten1);
    .header-text {
      position: absolute;
    }
    .icon {
      order: 0;
    }
    .header {
      order: 1;
    }
  }
  .tips-menu-body {
    .icon-left {
      margin-top: 2px !important;
      margin-right: 10px !important;
    }
    .icon-header-left {
      margin-top: 2px;
      position: absolute;
    }
    ::v-deep .v-expansion-panel-header {
      padding: 12px 16px !important;
      border-top-left-radius: 0px !important;
      border-top-right-radius: 0px !important;
    }
    ::v-deep .v-expansion-panels {
      border-radius: 0px !important;
    }
    :v-deep
      .v-expansion-panels:not(.v-expansion-panels--accordion):not(.v-expansion-panels--tile)
      > .v-expansion-panel--active
      + .v-expansion-panel {
      border-top-left-radius: 0px !important;
      border-top-right-radius: 0px !important;
    }
    ::v-deep .v-expansion-panel-content__wrap {
      padding: 0 16px 8px !important;
      border-bottom: 1px solid var(--v-black-lighten2) !important;
    }
    ::v-deep .v-expansion-panel--active:not(:first-child),
    .v-expansion-panel--active + .v-expansion-panel {
      margin-top: 0px !important;
    }
    ::v-deep .v-application--is-ltr .v-expansion-panel-header {
      height: 45px !important;
    }
    ::v-deep .v-expansion-panel--active > .v-expansion-panel-header {
      border-top: 1px solid var(--v-black-lighten2) !important;
    }
  }
}
</style>
