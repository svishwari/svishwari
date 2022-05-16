import Header from "../components/PageHeader.vue"

export default {
  title: "NewComponents/Header",
  components: { Header },
}

export const header = () => ({
  components: { Header },
  template: `<header title="plzwork"></header>`,
})
