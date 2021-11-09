<template>
  <v-dialog v-model="localModal" :width="width">
    <template #activator="{ on, attrs }">
      <slot name="activator" v-bind="attrs" v-on="on"></slot>
    </template>
    <template #default>
      <div class="confirm-modal-wrapper">
        <div class="confirm-modal-body px-6">
          <slot name="title">
            <div v-if="title" class="black--text text--darken-4 text-h1 pt-7">
              {{ title }}
            </div>
          </slot>
          <slot name="body">
            <div
              v-if="body"
              class="
                black--text
                text--darken-4 text-subtitle-1
                pt-6
                font-weight-regular
              "
            >
              {{ body }}
            </div>
          </slot>
        </div>
        <div class="confirm-modal-footer">
          <slot name="footer">
            <huxButton
              size="large"
              variant="white"
              height="40"
              is-tile
              @click="onCancel()"
            >
              <span class="primary--text">{{ leftBtnText }}</span>
            </huxButton>
          </slot>
        </div>
      </div>
    </template>
  </v-dialog>
</template>

<script>
import huxButton from "@/components/common/huxButton"
export default {
  name: "Modal",

  components: {
    huxButton,
  },

  props: {
    title: {
      type: String,
      required: false,
    },

    body: {
      type: String,
      required: false,
    },

    leftBtnText: {
      type: String,
      required: false,
      default: "Cancel",
    },

    value: {
      type: Boolean,
      required: true,
      default: false,
    },

    width: {
      type: Number,
      required: false,
      default: 900,
    },

    isDisabled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      localModal: this.value,
    }
  },

  computed: {
    localIconColor() {
      if (this.iconColor) {
        return this.iconColor
      }
      return this.type
    },
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
  },
}
</script>

<style lang="scss" scoped>
.confirm-modal-wrapper {
  background: var(--v-white-base);
  text-align: center;
  padding-top: 42px;
  .confirm-modal-footer {
    border-top: 1px solid var(--v-black-lighten3);
    margin-top: 36px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    background: var(--v-primary-lighten1);
  }
}
</style>
