<template>
  <v-navigation-drawer
    v-model="sidebarMenu"
    app
    floating
    :permanent="sidebarMenu"
    :mini-variant.sync="mini"
  >
    <v-list dense color="primary" dark class="logo-holder">
      <div class="hux_logo"></div>
      <v-list-item> </v-list-item>
    </v-list>
    <v-list-item class="px-2 profile-name">
      <v-select
        v-model="select"
        :items="userDropdown"
        item-text="state"
        item-value="abbr"
        return-object
        single-line
        class="user-profile"
      ></v-select>
    </v-list-item>
    <v-divider></v-divider>
    <v-list v-for="item in items" :key="item.title" no-action>
      <span class="list-group" v-if="item.label && !toggle">
        {{ item.label }}
      </span>
      <v-list-item v-if="!item.menu" :to="item.link">
        <v-list-item-icon>
          <v-icon color="primary"> {{ item.icon }} </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title class="primary--text">
            {{ item.title }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <div v-if="item.menu">
        <v-list-item
          v-for="menu in item.menu"
          :key="menu.title"
          :to="menu.link"
        >
          <v-list-item-icon>
            <v-icon color="primary"> {{ menu.icon }} </v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="primary--text">
              {{ menu.title }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </div>
    </v-list>

    <template v-slot:append v-if="!toggle">
      <div class="nav-footer">Hux by Deloitte Digital</div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import menuConfig from "@/menuConfig.json";

export default {
  name: "SideMenu",
  props: ["toggle"],
  computed: {
    layout() {
      // none-layout will be used if the meta.layout tag is not set
      // computed may not be best place in vue lifecycle for this but it works ok
      return `${this.$route.meta.layout || "none"}-layout`;
    },
    mini() {
      return this.$vuetify.breakpoint.smAndDown || this.toggle;
    },
    buttonText() {
      return !this.$vuetify.theme.dark ? "Go Dark" : "Go Light";
    },
  },
  mounted() {
    window.addEventListener("load", () => {
      document.getElementsByClassName("loader-overlay")[0].remove();
    });
  },
  data: () => ({
    sidebarMenu: true,
    items: menuConfig.menu,
    select: { state: "Pendieton", abbr: "FL" },
    userDropdown: [
      { state: "Pendieton", abbr: "FL" },
      { state: "Georgia", abbr: "GA" },
      { state: "Nebraska", abbr: "NE" },
      { state: "California", abbr: "CA" },
      { state: "New York", abbr: "NY" },
    ],
  }),
};
</script>

<style lang="scss">
.logo-holder {
  height: 105px;
}
.v-navigation-drawer {
  width: 220px;
}
.theme--light.v-navigation-drawer {
  background-color: #005587 !important;
}
.v-list-item__title {
  font-size: 13px;
  font-weight: 600;
  font-family: Open Sans;
  font-style: normal;
  font-weight: 600;
  line-height: 22px;
  letter-spacing: 0px;
  text-align: left;
}
div.v-list-item__title.primary--text,
i.v-icon.notranslate.mdi {
  color: #ffffff !important;
  caret-color: #ffffff !important;
}
.v-list .v-list-item--active {
  color: inherit;
}
div .v-list .v-list-item--active::before {
  background-color: #a0dcff !important;
  opacity: 0.2 !important;
}
.v-navigation-drawer .v-list {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 10px;
}

div.v-list-item__icon.v-list-group__header__prepend-icon {
  margin-right: 8.75px !important;
}
.list-group {
  margin-left: 17px;
  height: 40px;
  width: 199px;
  left: 17px;
  top: 218px;
  font-family: Open Sans;
  font-style: normal;
  font-weight: 600;
  font-size: 12px;
  line-height: 16px;
  display: flex;
  align-items: center;
  color: #ffffff;
  opacity: 0.5;
}
.v-list-item.v-list-item--link.theme--light {
  padding-left: 25px;
}
.v-navigation-drawer--mini-variant {
  width: 90px !important;
}
.v-btn.v-btn--icon.v-btn--round.theme--light.v-size--small {
  margin-right: 25px;
}
.v-list-item__content.text-truncate {
  width: 148px;
  margin-left: calc(50% - 148px / 2 - 11px);
  font-family: Open Sans;
  font-style: normal;
  font-weight: 600;
  font-size: 13px;
  line-height: 22px;
  display: flex;
  align-items: center;
  color: #ffffff;
}
.px-2.v-list-item.v-list-item--link.theme--light {
  background: rgba(0, 0, 0, 0.25);
}
.hux_logo {
  background-image: url("../assets/images/hux_logo_2.svg");
  width: 55px;
  height: 55px;
  margin-top: 17px;
  margin-left: 17px;
}
.nav-footer {
  height: 35px;
  left: 6.82%;
  right: 4.55%;
  bottom: 0px;
  font-family: Open Sans;
  font-style: normal;
  font-weight: 600;
  font-size: 12px;
  line-height: 16px;
  color: #ffffff;
  opacity: 0.8;
  margin-left: 15px;
  margin-right: 10px;
}
.profile-name {
  background: rgba(0, 0, 0, 0.25);
}
.profile-chevron-icon {
  margin-right: 25px !important;
  color: #ffffff !important;
}
a.v-list-item--active {
  background-color: unset !important;
}
.v-list.v-select-list.v-sheet {
  div.v-list-item__content {
    color: #0c0b0b !important;
  }
}
.profile-name {
  .v-select__selections {
    color: #ffffff !important;
  }
}
.theme--light.v-text-field > .v-input__control > .v-input__slot:before {
  border: none;
}
.v-text-field.v-input--is-focused > .v-input__control > .v-input__slot:after {
  border: none;
}
.v-select__selection.v-select__selection--comma {
  width: 148px;
  height: 15px;
  left: calc(50% - 148px / 2 - 11px);
  top: 117px;
  font-family: Open Sans;
  font-style: normal;
  font-weight: 600;
  font-size: 13px;
  line-height: 22px;
  display: flex;
  align-items: center;
  color: #ffffff;
}
</style>
