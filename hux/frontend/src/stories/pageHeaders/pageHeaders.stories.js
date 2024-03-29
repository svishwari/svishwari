import PageHeader from "./PageHeader.vue"
import AllIcons from "../icons/Icons"
import Icon from "../icons/Icon2.vue"
import HuxButton from "../huxButton/huxButton2.vue"
import Breadcrumb from "./NewBreadcrumb.vue"

export default {
  components: { PageHeader, AllIcons },

  title: "NewComponents/PageHeader",

  argTypes: {
    iconType: {
      control: { type: "select" },
      options: AllIcons,
    },
    title: { control: { type: "text" } },
    titleIcon: { control: { type: "boolean" } },
    titleFavorite: { control: { type: "boolean" } },
    breadcrumbItems: {
      control: { type: "object" },
    },
    titleDisabled: {
      control: { type: "boolean" },
    },
    description: { control: { type: "text" }, icon: [""] },
    callToAction: { control: { type: "boolean" } },
    ctaIcons: {
      control: { type: "array" },
    },
  },

  args: {
    callToAction: false,
    iconType: "Icon Placeholder",
    titleIcon: false,
    titleFavorite: false,
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { PageHeader, Icon, HuxButton, Breadcrumb },
  props: Object.keys(argTypes),
  template: `
    <page-header v-bind="$props">
      <template #breadcrumbs >
          <breadcrumb :items="$props.breadcrumbItems"></breadcrumb>
      </template>
      <template #call-to-action v-if="$props.callToAction" class="new-b3">
        <icon v-for="icons in $props.ctaIcons" :type="icons" size="24" color="primary" class="ml-2 mr-2 mt-1" />
        <hux-button class="ml-2 new-b3">button</hux-button>
      </template>
    </page-header>
  `,
})

export const DefaultHeader = Template.bind({})
