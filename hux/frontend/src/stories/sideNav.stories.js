import SideNav from "../components/SideMenu.vue"

export default {
  component: SideNav,
  title: "NewComponents/SideNav",
}

export const mySideNav = () => ({
  components: { SideNav },
  template: `
    <side-nav :toggle="true"></side-nav>
  `,
})
