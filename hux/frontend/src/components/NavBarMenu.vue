<template>
    <v-app>
        <v-btn icon class="icon-btn">
          <v-icon class="mdi-plus">mdi-plus</v-icon>
        </v-btn>
        <Notification></Notification>
        <v-btn icon class="icon-btn">
          <v-icon class="mdi-help">mdi-help</v-icon>
        </v-btn>
        <v-divider vertical></v-divider>
        <UserAvatar></UserAvatar>
    </v-app>
</template>

<script>
import Notification from "@/components/Notification";
import UserAvatar from "@/components/UserAvatar";

export default {
  name: "NavBarMenu",
  components: { Notification, UserAvatar },
};
</script>

<style lang="scss">
.v-application--wrap {
  min-height: unset !important;
  flex-direction: row !important;
  button {
    margin: 5px;
  }
}
.icon-btn {
  box-shadow: 0px 1px 5px rgb(0 0 0 / 25%);
  i.v-icon.notranslate.mdi {
    color: #005587 !important;
  }
}
.icon-btn.v-btn.v-btn--icon.v-btn--round {
  margin-right: 9px;
  margin-left: 9px;
}
.v-divider.v-divider--vertical{
  border: 1px solid #D0D0CE;
  margin-right: 9px;
  margin-left: 9px;
}
</style>
