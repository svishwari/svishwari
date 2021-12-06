<template>
  <div class="team-members-wrapper">
    <empty-page type="lift-table-empty" >
      <template #title>
        <div class="title-no-notification">No data to show</div>
      </template>
      <template #subtitle>
        <div class="des-no-notification">
          Latest alerts table will appear here once you start getting alerts.
        </div>
      </template>
    </empty-page>
  </div>
</template>

<script>
import EmptyPage from "@/components/common/EmptyPage"

export default {
  name: "TeamMembers",
  components: { EmptyPage },
  data() {
    return {}
  },
  computed: {},
}
</script>

<style lang="scss" scoped>
.team-members-wrapper {
}
</style>
