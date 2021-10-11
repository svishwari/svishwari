<template>
  <v-dialog v-model="localModal" :width="width">
    <template #activator="{ on, attrs }">
      <slot name="activator" v-bind="attrs" v-on="on"></slot>
    </template>
    <div class="white text-center pt-10">
      <div class="px-15 modal-content">
        <icon type="exclamation_outline" :color="type" :size="44" />
        <div class="black--text text--darken-4 text-h3 py-3">{{ title }}</div>
        <slot name="body">
          <div class="black--text text--darken-4 text-h6 pb-10">{{ body }}</div>
        </slot>
      </div>
      <div
        class="
          modal-footer
          primary
          lighten-1
          d-flex
          justify-space-between
          align-center
          px-10
          py-5
        "
      >
        <huxButton
          size="large"
          variant="white"
          height="40"
          is-tile
          @click="onCancel()"
        >
          {{ leftBtnText }}
        </huxButton>
        <huxButton
          size="large"
          :variant="type"
          height="40"
          is-tile
          @click="onConfirm()"
        >
          {{ rightBtnText }}
        </huxButton>
      </div>
    </div>
  </v-dialog>
</template>

<script>
import huxButton from "@/components/common/huxButton"
import Icon from "@/components/common/Icon.vue"
export default {
  name: "ConfirmModal",

  components: {
    huxButton,
    Icon,
  },

  props: {
    type: {
      type: String,
      required: false,
      default: "primary",
    },

    title: {
      type: String,
      required: false,
      default: "title",
    },

    body: {
      type: String,
      required: false,
      default: "body",
    },

    leftBtnText: {
      type: String,
      required: false,
      default: "Cancel",
    },

    rightBtnText: {
      type: String,
      required: false,
      default: "Add",
    },

    value: {
      type: Boolean,
      required: true,
      default: false,
    },

    width: {
      type: Number,
      required: false,
      default: 600,
    },
  },

  data() {
    return {
      localModal: this.value,
    }
  },

  watch: {
    value: function () {
      this.localModal = this.value
    },

    localModal: function () {
      this.$emit("input", this.localModal)
      if (!this.localModal) {
        this.$emit("onClose")
      }
    },
  },

  methods: {
    onCancel: function () {
      this.$emit("onCancel")
    },
    onConfirm: function () {
      this.$emit("onConfirm")
    },
  },
}
</script>

<style lang="scss" scoped>
.modal-footer {
  box-shadow: 0px -0.5px 5px 1px rgba(0, 0, 0, 0.15);
}
</style>
