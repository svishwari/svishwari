<template>
  <v-dialog v-model="localModal" :width="width" max-width="952">
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
              :color="localIconColor"
              :size="iconSize"
              class="mb-7"
            />
          </slot>
          <slot name="title">
            <div v-if="title" class="black--text text--darken-4 text-h2 mb-6">
              {{ title }}
            </div>
          </slot>
          <slot name="body">
            <div
              v-if="body"
              class="
                black--text
                text--darken-4 text-body-1
                font-weight-regular
                mb-8
              "
            >
              {{ body }}
            </div>
          </slot>
        </div>
        <div class="modal-footer">
          <slot name="footer">
            <huxButton
              size="large"
              variant="white"
              height="40"
              width="88"
              :style="{ float: 'left' }"
              class="mr-2 btn-border box-shadow-none"
              @click="onCancel()"
            >
              <span class="primary--text">{{ cancelBtnText }}</span>
            </huxButton>
            <huxButton
              v-if="showBack"
              size="large"
              variant="white"
              height="40"
              class="btn-border box-shadow-none"
              :style="{ float: 'left' }"
              @click="onBack()"
            >
              <span class="primary--text">{{ backBtnText }}</span>
            </huxButton>
            <huxButton
              v-if="showConfirm"
              size="large"
              variant="primary"
              height="40"
              :style="{ float: 'right' }"
              @click="onSubmit()"
            >
              <span>{{ confirmBtnText }}</span>
            </huxButton>
          </slot>
        </div>
      </div>
    </template>
  </v-dialog>
</template>

<script>
import huxButton from "@/components/common/huxButton"
import Icon from "../../components/common/Icon.vue"
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
    },

    iconSize: {
      type: [Number, String],
      required: false,
      default: 40,
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
  .modal-body {
    margin-right: 24px;
    margin-left: 24px;
  }
  .modal-footer {
    border-top: 1px solid var(--v-black-lighten3);
    display: flow-root;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px;
    background: var(--v-primary-lighten1);
  }
}
</style>
