import SideNav from "../components/SideMenu.vue"

export default {
  component: SideNav,
  title: "NewComponents/SideNav",

  argTypes: {
    toggle: { control: 'boolean' },
  }, 

  args: {
    toggle: "true",
  },
}

const Template = (args, { argTypes }) => ({
  components: { SideNav },
  props: Object.keys(argTypes),
  template: `
    <side-nav :toggle="$props"></side-nav>
  `,
})

export const Temp = Template.bind({})