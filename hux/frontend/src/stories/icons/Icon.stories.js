import Icon from "@/components/common/Icon"
import AllIcons from "./Icons"

const BasicTemplate = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  components: { Icon },
  template: "<div><Icon v-bind='$props' /></div>",
})

const TemplateAll = (args) => ({
  props: Object.keys(args),
  components: { Icon },
  template: `
  <div>
      <h2 class="text-h2"> All Application Icons</h2>
      <Icon v-for="ico in $props.list" :key="ico" :type="ico" :size="40" color="primary" variant="lighten5" class="mr-5" />
  </div>`,
})

export default {
  title: "Design System/Icon",
  decorators: [() => ({ template: "<story/>" })],
  argTypes: {
    type: {
      defaultValue: "mapping",
      options: AllIcons,
      control: {
        type: "select",
      },
    },
    size: {
      defaultValue: 40,
      control: {
        type: "number",
      },
    },
    color: {
      defaultValue: "primary",
      options: [
        "primary",
        "secondary",
        "black",
        "success",
        "yellow",
        "info",
        "warning",
        "white",
        "error",
      ],
      control: {
        type: "select",
      },
    },
    varia: {
      defaultValue: "base",
      options: ["lighten1", "lighten2", "lighten3"],
      control: {
        type: "select",
      },
    },
  },
}

export const Default = BasicTemplate.bind({})

export const List = TemplateAll.bind({})
List.args = { list: AllIcons }
