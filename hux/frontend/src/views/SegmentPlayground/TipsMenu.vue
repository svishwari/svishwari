<template>
  <span class="d-flex cursor-pointer mr-4 icon-bulb">
    <drop-menu
      :min-midth="300"
      :max-width="353"
      :close-on-click="false"
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
          <span class="ml-2 mt-1"> Segment Playground user guide </span>
        </div>
      </template>
      <template #menuBody>
        <div>
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
  data() {
    return {
      panelIndex: false,
      panel: [],
      panelListItems: [
        {
          id: 1,
          title: "What is Segment Playground?",
          text: "<b>Segment Playground </b>allows you to explore and segment your full customer list and enables you to see real time insights.",
          textPart: "",
        },
        {
          id: 2,
          title: "What is segmenting?",
          text: "<b>Segmenting</b> is the process of filtering your full customer list based on model scores or specific characteristics.",
          textPart: "",
        },
        {
          id: 3,
          title: "How do I use Segment Playground?",
          text: "First click <b>+ Attribute,</b> then select what characteristic you would like to segment your customer list. As you add attributes, the insights on the right hand will update accordingly.",
          textPart:
            "If you want to save this segment as an audience, click on <b >Save this segment as an audience.</b> By doing so you will not only save this segment as an audience, but you will also have the ability to deliver this audience to a 3rd party platform when you are ready OR add it to an engagement.",
        },
        {
          id: 4,
          title: "+ Attribute vs + Sections",
          text: "Adding an attibute will add another line rule under an <b>All</b> vs <b>Any</b> section rule.",
          textPart:
            "Adding another section enables you to create a new <b>All</b> vs <b>Any</b> section rule in addition to your previous section(s) where you can add new attributes.",
        },
        {
          id: 5,
          title: "“All” vs “Any”",
          text: "<b>All</b> means that a customer must match every attribute within the section in order to be included in the segment.",
          textPart:
            "<b>Any</b> means that a customer must match at least 1 of the attributes within the section in order to be included in the segment.",
        },
      ],
    }
  },
}
</script>
<style lang="scss" scoped>
.icon-bulb {
  margin-top: 8rem;
}
.drop-menu-div {
  width: 353 !important;
  z-index: 1;
}
.header-menu {
  background: #fffcf2;
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
.icon-left {
  margin-top: 2px !important;
  margin-right: 10px !important;
}
.icon-header-left {
  margin-top: 2px;
  position: absolute;
}
::v-deep .v-expansion-panel-header {
  padding: 10px 16px !important;
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
::v-deep .v-expansion-panel {
  height: 45px !important;
}
</style>
