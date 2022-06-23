<template>
  <div class="ma-2">
    <slot name="default">
      <div class="pl-2">Header</div>
      <v-card class="small-list-card">
        Content
        <icon type="cross" size="15" color="primary" class="close-icon" />
      </v-card>
    </slot>
  </div>
</template>

<script>
import Icon from "../icons/Icon2.vue"

export default {
  name: "FormListItem",
  components: { Icon },
}
</script>

<style lang="scss" scoped>
.small-list-card {
  display: inline-block;
  padding: 12px;
}
.close-icon {
  float: right;
  margin-top: 4px;
  margin-left: 20px;
}
</style>
