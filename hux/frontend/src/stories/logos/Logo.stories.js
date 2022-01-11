import Logo from "@/components/common/Logo"
import AllLogos from "./Logos"

const BasicTemplate = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  components: { Logo },
  template: "<div><Logo v-bind='$props' /></div>",
})

const TemplateAll = (args) => ({
  props: Object.keys(args),
  components: { Logo },
  template: `
  <div>
      <h2 class="text-h2"> All Application Logos</h2>
      <Logo v-for="ico in $props.list" :key="ico" :type="ico" :size="40" class="mr-5" />
  </div>`,
})

export default {
  title: "Design System/Logo",
  decorators: [() => ({ template: "<story/>" })],
  argTypes: {
    type: {
      defaultValue: "youtube",
      options: AllLogos,
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
  },
}

export const Default = BasicTemplate.bind({})

export const List = TemplateAll.bind({})
List.args = { list: AllLogos }
