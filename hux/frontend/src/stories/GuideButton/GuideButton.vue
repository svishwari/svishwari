<template>
  <span class="cursor-pointer mr-6 icon-bulb" :style="{ right: rightPosition }">
    <drop-menu
      :min-midth="300"
      :max-width="353"
      close-on-click
      content-class="guide-button"
      class="drop-menu-div"
    >
      <template #menuActivator="activatorVal">
        <div class="guide-container">
          <span v-if="!activatorVal.activatorVal" class="square-and-bulb">
            <div class="guide-square"></div>
            <icon
              class="guide-bulb"
              type="Guide"
              color="black-base"
              bg-color="yellow-lighten3"
              outline
              border-color="white-base"
              :size="40"
            />
          </span>
          <span v-else>
            <div class="guide-square-active"></div>
            <icon
              class="guide-cross"
              type="Close & Remove"
              color="black"
              :size="40"
            />
          </span>
        </div>
      </template>
      <template #menuHeader>
        <div class="header-menu d-flex text-body-1 pt-5 pb-5 pr-4 pl-4">
          <span>
            <icon type="Guide" :size="24" />
          </span>
          <span class="ml-2 mt-1"> {{ header }} </span>
        </div>
      </template>
      <template #menuBody>
        <div class="guide-button-body">
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
                <div
                  class="text-body-1"
                  v-bind.prop="formatInnerHTML(data.text)"
                ></div>
                <br />
                <div
                  v-if="data.textPart"
                  class="text-body-1"
                  v-bind.prop="formatInnerHTML(data.textPart)"
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
import Icon from "../icons/Icon2"
import DropMenu from "@/components/common/DropMenu"
import { formatInnerHTML } from "@/utils"

export default {
  name: "GuideButton",
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
  methods: {
    formatInnerHTML: formatInnerHTML,
  },
}
</script>
<style lang="scss" scoped>
.guide-container {
  position: relative;
  bottom: 8px !important;
}
.square-and-bulb {
  &:hover {
    .guide-square {
      transform: rotate(45deg);
    }
  }
}
.guide-square {
  @extend .box-shadow-15-16;
  position: relative;
  top: 48px;
  width: 56px;
  height: 56px;
  background-color: var(--v-yellow-lighten3);
  border-radius: 3px;
  border: 1px solid var(--v-white-base);
  ::before {
    content: "";
    display: block;
    width: 50%;
    padding-bottom: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 2;
    transform: translate(-50%, -50%);
    border: solid 400px rgba(31, 44, 122, 0.5);
    border-radius: 50%;
  }
}
.guide-square-active {
  @extend .guide-square;
  top: 32px !important;
  background-color: var(--v-white-base);
}
.guide-bulb {
  z-index: 9;
  position: relative;
}
.guide-cross {
  bottom: 16px;
  position: relative;
}
.icon-bulb {
  position: absolute;
  bottom: -2.5rem;
  right: 0;
  z-index: 8;
}
.drop-menu-div {
  z-index: 1;
}
.guide-button {
  top: 165px !important;
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
  .guide-button-body {
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
