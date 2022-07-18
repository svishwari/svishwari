<template>
  <div class="seperator mt-5 mb-1">
    <hr class="primary lighten-7" />
    <v-chip
      small
      class="px-2 section-chip-icon cursor-pointer"
      text-color="white"
      color="primary lighten-7"
      :ripple="false"
    >
      <span class="new-pills">+ New section</span>
    </v-chip>
  </div>
</template>

<script>
export default {
  name: "SectionalButton",
}
</script>
<style lang="scss" scoped>
$btn-active-opacity: 0 !important;
$btn-hover-opacity: 0 !important;
.seperator {
  position: relative;
  hr {
    border-style: solid;
    border-bottom: 0px !important;
  }
  .v-chip {
    position: absolute;
    top: -12px;
    left: 50%;
    ::v-deep .new-pills {
      padding-top: 2px;
      padding-bottom: 2px;
    }
  }
  &:hover,
  &:active {
    .v-chip,
    hr {
      background-color: var(--v-primary-base) !important;
    }
  }
}
</style>
