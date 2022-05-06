import SideNav from "./SideNav.vue"

export default {
  component: SideNav,
  title: "Components/SideNav",
}

const Template = () => ({
  components: { SideNav },
  template: `
    <side-nav/>
  `,
})

export const temp = Template.bind({})