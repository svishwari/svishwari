import HuxButton from "../components/common/huxButton.vue"

export default {
  title: "Button",
}

export const withDefaults = () => ({
  components: { HuxButton },
  template: `
    <hux-button
      variant="primary"
      is-tile
      width="80"
      height="40"
    >
      Add
    </hux-button>
  `,
})
