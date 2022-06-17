import GuideButton from "./GuideButton.vue"
import PageHeader from "@/components/PageHeader"
export default {
  component: GuideButton,
  title: "NewComponents/GuideButton",

  args: {
    header: "My custom header",
    panelListItems: [
      {
        id: 1,
        title: "Collapisble title",
        text: "Collapsible text",
      },
    ],
    rightPosition: "0",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=6852%3A134015",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { GuideButton, PageHeader },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
<template>
  <div>
    <page-header :header-height="110">
      <template #right>
        <guide-button v-bind="$props" v-on="$props" />
      </template>
    </page-header>
  </div>
</template>
        `,
})

export const myGuideButton = Template.bind({})
