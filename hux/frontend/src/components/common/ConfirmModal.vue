<template>
  <v-dialog v-model="localModal" :width="width">
    <template #activator="{ on, attrs }">
      <slot name="activator" v-bind="attrs" v-on="on"></slot>
    </template>
    <template #default>
      <div class="confirm-modal-wrapper">
        <div class="confirm-modal-body px-6">
          <slot name="icon">
            <icon
              v-if="icon"
              :type="icon"
              :color="localIconColor"
              :size="iconSize"
            />
          </slot>
          <slot name="title">
            <div v-if="title" class="black--text text--darken-4 text-h2 pt-3">
              {{ title }}
            </div>
          </slot>
          <slot name="sub-title">
            <div
              v-if="subTitle"
              class="black--text text--darken-4 text-h2 mt-n2"
            >
              {{ subTitle }}
            </div>
          </slot>
          <div class="body-slot mx-7">
            <slot name="body">
              <div
                v-if="body"
                class="
                  black--text
                  text--darken-4 text-subtitle-1
                  pt-6
                  font-weight-regular
                "
                v-html="body"
              ></div>
            </slot>
          </div>
        </div>
        <div class="confirm-modal-footer">
          <slot name="footer">
            <huxButton
              size="large"
              variant="white"
              height="40"
              is-tile
              class="btn-border box-shadow-none"
              :class="{ invisible: !showLeftButton }"
              @click="onCancel()"
            >
              <span class="primary--text">{{ leftBtnText }}</span>
            </huxButton>
            <huxButton
              size="large"
              :variant="type"
              height="40"
              is-tile
              :is-disabled="isDisabled"
              @click="onConfirm()"
            >
              {{ rightBtnText }}
            </huxButton>
          </slot>
        </div>
      </div>
    </template>
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
      default: 42,
    },

    type: {
      type: String,
      required: false,
      default: "primary",
    },

    title: {
      type: String,
      required: false,
    },

    subTitle: {
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
      default: "Nevermind!",
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

    isDisabled: {
      type: Boolean,
      required: false,
      default: false,
    },

    showLeftButton: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  emits: ["on-cancel", "on-confirm"],
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
    onConfirm: function () {
      this.$emit("onConfirm")
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
    padding: 20px 28px;
    background: var(--v-primary-lighten1);
  }
}
.invisible {
  visibility: hidden;
}
</style>
