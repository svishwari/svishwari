<template>
  <v-card class="card-wrapper mb-3" height="60" tile>
    <v-card-actions>
      <v-list-item class="grow">
        <v-list-item-avatar width="26" height="26" min-width="26">
          <slot name="logo"></slot>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>
            <slot name="title"></slot>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>
<script>
export default {
  name: "DestinationListCard",
}
</script>
