import PageHeader from "./PageHeader.vue"
import Breadcrumb from "@/components/common/Breadcrumb"

export default {
  component: PageHeader,

  title: "Components/Header",

  argTypes: {
    items: { control: "array" },
  },

  args: {
    items: [
      {
        text: "Home",
        disabled: false,
        icon: "home",
      },
      {
        text: "Connections",
        disabled: false,
        icon: "connections",
      },
      {
        text: "Destinations",
        disabled: true,
        icon: "destinations",
      },
    ],
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=2048%3A14220",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { PageHeader, Breadcrumb },

  props: Object.keys(argTypes),

  template: `
    <page-header>
      <template slot="left">
        <breadcrumb v-bind="$props" />
      </template>
    </page-header>
  `,
})

export const Header = Template.bind({})
