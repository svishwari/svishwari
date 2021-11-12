<template>
  <span class="d-flex cursor-pointer mr-4 icon-bulb">
    <drop-menu :min-midth="300" :max-width="353" class="drop-menu-div">
      <template #menuActivator="activatorVal">
        <div class="circle-append">
          <span v-if="!activatorVal.activatorVal">
            <icon :type="'FAB-bulb'" :size="30" />
          </span>
          <span v-else><icon type="FAB-close" :size="20" /></span>
        </div>
      </template>
      <template #menuHeader>
        <div class="header-menu text-body-1 pt-5 pb-5 pr-4 pl-4">
          <span>
            <icon type="FAB-bulb" :size="22" />
          </span>
          <span class="header-text ml-2">
            Segment Playground user guide &nbsp; &nbsp;
            <span class="icon-header-left">
              <span v-if="!headerIcon" @click="all">
                <icon :type="'side-arrow'" :size="11" color="black" />
              </span>
              <span v-else @click="none">
                <icon
                  :type="'down-arrow'"
                  :size="11"
                  :color="'black'"
                  :variant="'base'"
                />
              </span>
            </span>
          </span>
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
      headerIcon: false,
      panelListItems: [
        {
          id: 1,
          title: "What is Segment playground?",
          text: "<b>Segment playground </b>allows you to explore and segment your full customer list and enables you to see real time insights.",
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
          title: "How do I use segment playground?",
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
  methods: {
    all() {
      this.headerIcon = false
      this.panel = [...Array(this.panelListItems.length).keys()].map(
        (k, i) => i
      )
      this.headerIcon = true
    },
    none() {
      this.panel = []
      this.headerIcon = false
    },
  },
}
</script>
<style lang="scss" scoped>
.icon-bulb {
  margin-top: 8rem;
}
.drop-menu-div {
  width: 353 !important;
}
.circle-append {
  height: 56px;
  width: 56px;
  border-radius: 40px;
  background: #ffffff;
  padding-top: 15px;
  box-shadow: 0px -1px 7px rgba(188, 186, 186, 0.25),
    0px 1px 5px rgba(188, 186, 186, 0.25);
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
}
::v-deep .v-expansion-panel-content__wrap {
  padding: 0 16px 8px !important;
}
::v-deep .v-expansion-panel--active:not(:first-child),
.v-expansion-panel--active + .v-expansion-panel {
  margin-top: 0px !important;
}
</style>
