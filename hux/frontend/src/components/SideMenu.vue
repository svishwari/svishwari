<template>
    <v-app>
        <v-navigation-drawer 
            v-model="sidebarMenu" 
            app
            floating
            :permanent="sidebarMenu"
            :mini-variant.sync="mini"
            >
            <v-list dense color="primary" dark class="logo-holder">
                <div class="hux_logo"> </div>
                <v-list-item> </v-list-item>
            </v-list>
            <v-list-item class="px-2 profile-name">
                <v-list-item-content class="text-truncate">
                    Pendieton
                </v-list-item-content>
                <v-menu bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon v-bind="attrs" v-on="on" class="chevron-icon profile-chevron-icon">mdi-chevron-down</v-icon>
                  </template>
                  <v-list>
                    <v-list-item>
                      <v-list-item-title> Profile </v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title> Settings </v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title> Log-out </v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
            </v-list-item>
            <v-divider></v-divider>
            <v-list>
              <v-list-group
                v-for="item in items" :key="item.title"
                v-model="item.active"
                :prepend-icon="item.action"
                no-action>
                <v-list-item slot="activator" :to="item.link">
                  <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-for="subItem in item.items" :key="subItem.title" :to="subItem.link">
                  <v-list-item-content>
                    <v-list-item-title>{{ subItem.title }}</v-list-item-title>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-icon>{{ subItem.action }}</v-icon>
                  </v-list-item-action>
                </v-list-item>
              </v-list-group>
            </v-list>

            <template v-slot:append v-if="!toggle">
              <div class="nav-footer">
                Hux by Deloitte Digital
              </div>
            </template>
        </v-navigation-drawer>
    </v-app>
</template>

<script>
import menuConfig from '@/menuConfig.json'

export default {
  name: "SideMenu",
  props: ['toggle'],
  computed: {
    layout() {
        // none-layout will be used if the meta.layout tag is not set
        // computed may not be best place in vue lifecycle for this but it works ok
        return `${this.$route.meta.layout || "none"}-layout`;
    },
    mini() {
        return (this.$vuetify.breakpoint.smAndDown) || this.toggle
    },
    buttonText() {
        return !this.$vuetify.theme.dark ? 'Go Dark' : 'Go Light'
    },
  },
  mounted() {
    window.addEventListener("load", () => {
      document.getElementsByClassName("loader-overlay")[0].remove();
    });
  },
  data: () => ({
    sidebarMenu: true,
    // items: menuConfig.menu
    items: [{
        action: 'mdi-home-outline',
        title: 'Overview',
        link: "overview",
        heading: null
      }, {
        action: 'mdi-bullhorn-outline',
        title: 'Hux Campaigns',
        active: false,
        link: "campaign",
        heading: "ORCHESTRATION"
      }, {
        action: 'mdi-flip-h mdi-account-plus-outline',
        title: 'Audiences',
        link: "audiences",
        heading: null
      }, {
        action: 'mdi-tune',
        title: 'Models',
        link: "models",
        heading: null
      }, {
        action: 'mdi-connection',
        title: 'Connections',
        link: "/connection",
        heading: null
      }, {
        action: 'mdi-account-search-outline',
        title: 'Indentity',
        link: "/indentity",
        heading: null
      }, {
        action: 'mdi-account-details-outline',
        title: 'Profiles',
        heading: null,
        items: [{ title: 'Settings', link: "settings" }, { title: 'Logout', link: "logout" }]
      }]
  }),
};
</script>

<style lang="scss">
  body {
    padding: 0;
    margin: 0;
    width: 100%;
    height: 100vh;
    background: #f8f9fa;
    #nprogress .bar {
      height: 6px;
    }
  }
  /* All delay classes will take half the time to start */
  :root {
    --animate-delay: 0.1s;
  }
  .logo-holder {
    height: 105px;
  }
  .v-navigation-drawer {
    width: 220px;
  }
  .v-application--wrap > .theme--light.v-navigation-drawer {
    background-color: #005587;
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
  div.v-list-item__icon.v-list-group__header__prepend-icon{
    div.v-list-item__title.primary--text, i.v-icon.notranslate.mdi {
      color: #ffffff;
      caret-color: #ffffff;
    }
  }
  .v-navigation-drawer .v-list {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 10px;
  }
  div.v-list-group__header.v-list-item.v-list-item--link{
    div.v-list-item__icon.v-list-group__header__prepend-icon {
      margin-right: 8.75px;
    }
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
    color: #FFFFFF;
    opacity: 0.5;
  }
  .v-list-item.v-list-item--link.theme--light {
    padding-left: 25px;
  }

  .v-application--wrap > nav.v-navigation-drawer--mini-variant {
    width: 90px !important;
  }
  .v-btn.v-btn--icon.v-btn--round.theme--light.v-size--small {
    margin-right: 25px;
  }
  .v-list-item__content.text-truncate {
    width: 148px;
    margin-left: calc(50% - 148px/2 - 11px);
    font-family: Open Sans;
    font-style: normal;
    font-weight: 600;
    font-size: 13px;
    line-height: 22px;
    display: flex;
    align-items: center;
    color: #FFFFFF;
  }
  .px-2.v-list-item.v-list-item--link.theme--light{
    background: rgba(0, 0, 0, 0.25);
  }
  .hux_logo {
    background-image: url('../assets/hux _logo_2 .svg');
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
    color: #FFFFFF;
    opacity: 0.8;
    margin-left: 15px;
    margin-right: 10px;
  }
  .profile-name {
    background: rgba(0, 0, 0, 0.25);
  }
  .v-list-item.v-list-item--link {
    div.v-list-item__content {
      color: #ffffff;
    }
  }
  .v-list.v-sheet.theme--light {
    i.v-icon.notranslate.mdi.mdi-chevron-down.theme--light {
      display: none;
    }
  }
  div.profile-name{
    .profile-chevron-icon {
      margin-right: 25px;
      color: #FFFFFF;
    }
  }
  .v-list-group--active {
    background: rgba(255, 255, 255, 0.1);
  }
</style>
