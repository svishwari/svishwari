import CardInfo from "../components/common/CardInfo.vue"

export default {
  title: "Components/Card Info",
}

export const withDefaults = () => ({
  components: { CardInfo },
  template: `
    <card-info></card-info>
  `,
})
