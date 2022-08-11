<template>
  <v-dialog v-model="localModal" :width="width" @click:outside="clickOutside()">
    <template #activator="{ on, attrs }">
      <slot name="activator" v-bind="attrs" v-on="on"></slot>
    </template>
    <template #default>
      <div class="session-modal-wrapper">
        <div class="session-modal-body px-6">
          <icon
            v-if="icon"
            :type="icon"
            :color="localIconColor"
            :size="iconSize"
          />
          <div class="black--text text--darken-4 text-h2 pt-3">
            You session will expire in
          </div>
          <div class="black--text text--darken-4 new-h1 pt-3">
            {{ visibleMin }} min {{ visibleSec }} seconds
          </div>
          <div class="body-slot mx-7">
            <div
              class="
                black--text
                text--lighten-4
                new-b1
                pt-6
                font-weight-regular
              "
            >
              You’re being timed out due to inactivity for the last 30 minutes.
              Please click “Continue” to keep working or click “Log out” to end
              your session now. Otherwise, you will be logged out automatically.
            </div>
          </div>
        </div>
        <div class="session-modal-footer">
          <huxButton
            size="large"
            variant="white"
            height="40"
            is-tile
            class="btn-border box-shadow-none"
            @click="logout()"
          >
            <span class="primary--text">{{ leftBtnText }}</span>
          </huxButton>
          <huxButton
            size="large"
            :variant="type"
            height="40"
            is-tile
            :is-disabled="true"
            @click="sessioncontinue()"
          >
            {{ rightBtnText }}
          </huxButton>
        </div>
      </div>
    </template>
  </v-dialog>
</template>

<script>
import huxButton from "@/components/common/huxButton"
import Icon from "@/components/common/Icon.vue"
export default {
  name: "SessionModal",

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
      default: "Log out",
    },

    rightBtnText: {
      type: String,
      required: false,
      default: "Continue",
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
      displayMin: 1,
      displaySec: 59,
      visibleMin: "01",
      visibleSec: "59",
      sessionInterval: {},
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
      if (this.value === true) {
        this.sessionInterval = setInterval(this.start, 1000)
      } else {
        this.displayMin = 1
        this.displaySec = 59
      }
    },
    localModal: function () {
      this.$emit("input", this.localModal)
      if (!this.localModal) {
        this.$emit("onClose")
      }
    },
  },

  methods: {
    clickOutside() {
      this.localModal = true
    },
    logout: function () {
      this.$emit("logout")
    },
    sessioncontinue: function () {
      this.$emit("sessioncontinue")
    },
    start() {
      if (this.displaySec > 0) {
        this.displaySec--
      }
      if (this.displayMin == 0 && this.displaySec == 0) {
        clearInterval(this.sessionInterval)
        this.logoutSession()
      }
      if (this.displaySec < 1) {
        this.displayMin = 0
        this.displaySec = 59
      }
      if (this.displaySec < 10) {
        this.visibleSec = "0" + this.displaySec
      } else {
        this.visibleSec = this.displaySec
      }
      if (this.displayMin <= 1) {
        this.visibleMin = "0" + this.displayMin
      }
    },
    async logoutSession() {
      this.localModal = false
      await this.$store.dispatch("users/getUserProfile")
      await this.$auth.logout()
      this.visibleMin = "00"
      this.visibleSec = "00"
    },
  },
}
</script>

<style lang="scss" scoped>
.session-modal-wrapper {
  background: var(--v-white-base);
  text-align: center;
  padding-top: 42px;
  .session-modal-footer {
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
