<template>
  <div class="team-members-wrapper">
    <v-row>
      <v-col>
        <v-card class="rounded-lg box-shadow-5" :height="280">
          <v-row class="team-members-table-frame py-14">
            <empty-page type="user" :size="50">
              <template #title>
                <div class="title-no-notification">No team members</div>
              </template>
              <template #subtitle>
                <div class="des-no-notification">
                  The list of team mebers will appear here once the invitation
                  has been accepted. Please check back later.
                </div>
              </template>
            </empty-page>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
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
  .team-members-table-frame {
    background-image: url("../../../assets/images/no-lift-chart-frame.png");
    background-position: center;
  }
}
</style>
