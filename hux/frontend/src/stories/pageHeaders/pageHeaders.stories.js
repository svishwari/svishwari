import PageHeader from "./PageHeader.vue"
import AllIcons from "../icons/Icons"
import Icon from "../icons/Icon2.vue"
import HuxButton from "../huxButton/huxButton2.vue"
import Breadcrumb from "../../components/common/Breadcrumb.vue"

export default {
  components: { PageHeader, AllIcons },

  title: "NewComponents/PageHeader",

  argTypes: {
    iconType: {
      control: { type: "select" },
      options: AllIcons,
    },
    title: { control: { type: "text" } },
    titleIcon: {control: {type: "boolean"}},
    titleIconSel: { 
      control: {type: 'select'}, 
      options: AllIcons,
    },
    breadcrumbItems: {
      control: {type: 'object'},
    },
    maxBreadcrumbs: {
      control: {type: 'select'},
      options: ["None", "1", "2", "3", "4", "5"]
    },
    description: { control: { type: "text" }, icon: [''] },
    callToAction: { control: { type: "boolean" } },
    ctaIcon1: { 
      control: { type: 'select'},
      options: AllIcons,
    },
    ctaIcon2: { 
        control: { type: 'select'},
        options: AllIcons,
    },
    ctaIcon3: { 
      control: { type: 'select'},
      options: AllIcons,
    },
    ctaIcon4: { 
      control: { type: 'select'},
      options: AllIcons,
    },
  },

  args: {
    callToAction: false,
    iconType: "Icon Placeholder",
    titleIcon: false,
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
      <icon v-if="$props.ctaIcon1" :type="$props.ctaIcon1" size="24" color="primary" class="ml-2 mr-2 mt-1" /><icon v-if="$props.ctaIcon2" :type="$props.ctaIcon2" size="24" color="primary" class="ml-2 mr-2 mt-1" />
      <icon v-if="$props.ctaIcon3" :type="$props.ctaIcon3" size="24" color="primary" class="ml-2 mr-2 mt-1" />
      <icon v-if="$props.ctaIcon4" :type="$props.ctaIcon4" size="24" color="primary" class="ml-2 mr-2 mt-1" />
        <hux-button class="ml-2">button</hux-button>
      </template>
    </page-header>
  `,
})

export const DefaultHeader = Template.bind({})
