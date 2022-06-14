<template>
  <div class="header-container">
    <v-row>
      <div>
        <icon type="abandoned_cart" size="38" class="header-icon"></icon>
        <div class="header-title text-h1">Title</div>
        <icon type="fav_blank" size="18" class="ml-2"></icon>
        <div class="header-right">
          <div class="action-menu">
            <icon type="fav_blank" size="18" class="ml-2"></icon>
            <icon type="fav_blank" size="18" class="ml-2"></icon>
            <icon type="fav_blank" size="18" class="ml-2"></icon>
          </div>
          <hux-button class="header-button">Active</hux-button>
        </div>
      </div>
    </v-row>
    <v-row>
      <div>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lolestie feugiat morbi enim, vel a non fermentum nam.
      </div>
    </v-row>
  </div>
</template>

<script>
import Icon from "../icons/Icon2.vue"
import HuxButton from "../huxButton/huxButton2.vue"
export default {
  name: "PageHeader",
  components: { Icon, HuxButton },
}
</script>

<style lang="scss" scoped>
.header-container {
  padding: 32px;
  border: 1px solid gray;
}
.header-title {
  display: inline-block;
  margin-left: 8px;
}
.header-icon {
  float: left;
}
.header-right {
  position: relative;
  float: right;
  margin-left: 1110px;
  .action-menu {
    margin-top: 13px;
    float: left;
  }
  .header-button {
    margin-top: 2px;
    margin-left: 20px;
    float: right;
  }
}
</style>