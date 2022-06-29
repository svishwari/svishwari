import PageHeader from "./PageHeader.vue"
import AllIcons from "../icons/Icons"
import Icon from "../icons/Icon2.vue"
import HuxButton from "../huxButton/huxButton2.vue"

export default {
  components: { PageHeader, AllIcons },

  title: "NewComponents/PageHeader",

  argTypes: {
    iconType: {
      control: { type: "select" },
      options: AllIcons,
    },
    title: { control: { type: "text" } },
    description: { control: { type: "text" } },
    breadcrumbs: { control: { type: "boolean" } },
    callToAction: { control: { type: "boolean" } },
  },

  args: {
    breadcrumbs: false,
    callToAction: false,
    iconType: "Icon Placeholder",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { PageHeader, Icon, HuxButton },
  props: Object.keys(argTypes),
  template: `
    <page-header v-bind="$props">
      <template #breadcrumbs v-if="$props.breadcrumbs">
        <span>adding</span>
        <icon type="Dropdown - right" size="18" color="primary" class="ml-2 mr-2 mt-1" />
        <span>some</span>
        <icon type="Dropdown - right" size="18" color="primary" class="ml-2 mr-2 mt-1" />
        <span>breadcrumbs</span>
      </template>
      <template #call-to-action v-if="$props.callToAction">
        <span>adding call to action</span>
        <hux-button class="ml-2">button</hux-button>
      </template>
    </page-header>
  `,
})

export const DefaultHeader = Template.bind({})
