<template>
  <div class="empty-audiences">
    <v-row class="empty-icon" align="center" justify="center">
      <v-icon color="blue" x-large> <slot name="icon"></slot> </v-icon>
    </v-row>
    <v-row class="empty-title font-weight-light mt-3 pt-3" align="center" justify="center">
       <slot name="title"></slot>
    </v-row>
    <v-row class="empty-subtitle font-weight-regular mt-3 pt-3" align="center" justify="center">
       <slot name="subtitle"></slot>
    </v-row>
    <v-row class="empty-action mt-3 pt-3" align="center" justify="center">
       <slot name="button"></slot>
    </v-row>
  </div>
</template>
<script>
export default {
  name: "EmptyPage",
}
</script>
<style lang="scss" scoped>
.empty-audiences {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    .empty-title {
      font-size: large;
    }
    .empty-subtitle {
      text-align: center;
    }
  }
</style>
