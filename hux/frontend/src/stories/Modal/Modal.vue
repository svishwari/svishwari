<template>
  <v-dialog
    v-model="localModal"
    :width="width"
    max-width="952"
    max-height="500"
  >
    <template #activator="{ on, attrs }">
      <slot name="activator" v-bind="attrs" v-on="on"></slot>
    </template>
    <template #default>
      <div class="modal-wrapper">
        <div class="modal-body">
          <slot name="icon">
            <icon
              v-if="icon"
              :type="icon"
              :color="iconColor"
              :border-color="iconColor"
              outline
              :size="40"
              class="mb-8"
            />
          </slot>
          <slot name="title">
            <div v-if="title" class="black--text text--darken-4 new-h2 mb-6">
              {{ title }}
            </div>
          </slot>
          <slot name="body">
            <div
              v-if="body"
              class="
                black--text
                text--darken-4
                new-b1
                font-weight-regular
                mb-8
                lh-sm
              "
            >
              {{ body }}
            </div>
          </slot>
        </div>
        <div class="modal-footer">
          <slot name="footer">
            <huxButton
              v-if="showCancel"
              size="large"
              tile
              variant="secondary"
              :style="{ float: 'left' }"
              class="box-shadow-none button-padding"
              @click="onCancel()"
            >
              <span class="new-b3">{{ cancelBtnText }}</span>
            </huxButton>
            <huxButton
              v-if="showConfirm"
              size="large"
              tile
              variant="primary"
              :style="{ float: 'right' }"
              class="button-padding"
              @click="onSubmit()"
            >
              <span class="new-b3">{{ confirmBtnText }}</span>
            </huxButton>
            <huxButton
              v-if="showBack"
              size="large"
              tile
              variant="secondary"
              class="mr-2 box-shadow-none button-padding"
              :style="{ float: 'right' }"
              @click="onBack()"
            >
              <span class="new-b3">{{ backBtnText }}</span>
            </huxButton>
          </slot>
        </div>
      </div>
    </template>
  </v-dialog>
</template>

<script>
import huxButton from "../huxButton/huxButton2.vue"
import Icon from "../icons/Icon2.vue"
export default {
  name: "Modal",

  components: {
    huxButton,
    Icon,
  },

  props: {
    title: {
      type: String,
      required: false,
    },

    icon: {
      type: String,
      required: false,
    },

    iconColor: {
      type: String,
      required: false,
      default: "primary-base",
    },

    type: {
      type: String,
      required: false,
      default: "primary",
    },

    body: {
      type: String,
      required: false,
    },

    cancelBtnText: {
      type: String,
      required: false,
      default: "Cancel",
    },

    backBtnText: {
      type: String,
      required: false,
      default: "Back",
    },

    confirmBtnText: {
      type: String,
      required: false,
      default: "Submit",
    },

    value: {
      type: Boolean,
      required: true,
      default: false,
    },

    width: {
      type: Number,
      required: false,
      default: 552,
    },

    isDisabled: {
      type: Boolean,
      required: false,
      default: false,
    },

    showBack: {
      type: Boolean,
      required: false,
      default: false,
    },

    showConfirm: {
      type: Boolean,
      required: false,
      default: false,
    },

    showCancel: {
      type: Boolean,
      required: false,
      dafault: false,
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
    onBack: function () {
      this.$emit("onBack")
    },
    onSubmit: function () {
      this.$emit("onSubmit")
    },
  },
}
</script>

<style lang="scss" scoped>
.modal-wrapper {
  background: var(--v-white-base);
  text-align: center;
  padding-top: 48px;
  box-shadow: 0px 100px 200px rgba(30, 30, 30, 0.03),
    0px 16px 32px rgba(0, 85, 135, 0.15);
  .modal-body {
    margin-right: 24px;
    margin-left: 24px;
  }
  .modal-footer {
    box-shadow: inset 0px 1px 0px #dddddd;
    display: flow-root;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px;
    background: var(--v-primary-lighten1);
  }
}
.button-padding {
  padding: 10px 24px !important;
}
</style>
