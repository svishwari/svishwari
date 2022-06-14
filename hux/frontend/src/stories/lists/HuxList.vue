<template>
  <div>
    <div v-for="i in numListItems" :key="i" class="list-card">
      <div class="pl-4 pt-2">Label</div>
      <v-card>
        <v-list-item>
          <v-list-item-content>
            <div>
              <div class="list-title">Content</div>
              <hux-button
                class="list-button"
                variant="secondary"
                :icon="buttonText == `Selected` ? 'mdi-check' : ''"
                @click="handleClick()"
                >{{ buttonText }}</hux-button
              >
            </div>
          </v-list-item-content>
        </v-list-item>
      </v-card>
    </div>
  </div>
</template>

<script>
import HuxButton from "../huxButton/huxButton2.vue"

export default {
  name: "HuxList",
  components: { HuxButton },
  data() {
    return {
      buttonText: "Request",
    }
  },
  props: {
    numListItems: {
      type: [String, Number],
      required: false,
      default: 4,
    },
  },
  methods: {
    handleClick() {
      this.buttonText = "Selected"
    },
  },
}
</script>

<style lang="scss" scoped>
.list-card {
  width: 552px;
  justify-content: center;
  margin: 8px;
}
.list-title {
  float: left;
  height: 40px;
  padding-top: 12px;
}
.list-button {
  float: right;
}
</style>
