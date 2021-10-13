import CardInfo from "./CardInfo.vue"

export default {
  component: CardInfo,
  title: "Components/CardInfo",
}

export const withDefaults = () => ({
  components: { CardInfo },
  template: `
    <card-info></card-info>
  `,
})
