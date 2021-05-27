<template>
  <v-menu bottom offset-y open-on-hover class="cursor-default">
    <template v-slot:activator="{ on, attrs }">
      <span
        class="blue-grey d-flex align-center justify-center"
        v-bind="attrs"
        v-on="on"
        v-bind:style="{ 'border-color': userInfo.color }"
      >
        {{ userInfo.shortName }}
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title>{{ userInfo.fullName }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  name: "Avatar",
  props: {
    name: {
      type: String,
      default: "",
      required: true,
    },
  },
  computed: {
    userInfo() {
      if (this.name) {
        return {
          shortName: this.name
            .split(" ")
            .map((n) => n[0])
            .join(""),
          fullName: this.name,
          color: this.generateColor(this.name, 30, 60) + " !important",
        }
      } else {
        return {
          shortName: "",
          fullName: "",
          color: "",
        }
      }
    },
  },

  methods: {
    generateColor(str, s, l) {
      function hslToHex(h, s, l) {
        l /= 100
        const a = (s * Math.min(l, 1 - l)) / 100
        const f = (n) => {
          const k = (n + h / 30) % 12
          const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1)
          return Math.round(255 * color)
            .toString(16)
            .padStart(2, "0") // convert to Hex and prefix "0" if needed
        }
        return `#${f(0)}${f(8)}${f(4)}`
      }
      var hash = 0
      for (var i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash)
      }

      var h = hash % 360
      return hslToHex(h, s, l)
    },
    hsl2rgb(h, s, l) {
      let a = s * Math.min(l, 1 - l)
      let f = (n, k = (n + h / 30) % 12) =>
        l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1)
      return [f(0), f(8), f(4)]
    },
  },
}
</script>

<style lang="scss" scoped>
.blue-grey {
  border-width: 2px;
  border-style: solid;
  border-radius: 50%;
  font-size: 14px;
  width: 35px;
  height: 35px;
  line-height: 22px;
  color: var(--v-neroBlack-base) !important;
  cursor: default !important;
  background: transparent !important;
}
</style>
