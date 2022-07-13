import Icon from "../icons/Icon2.vue"
import Tooltip2 from "./Tooltip2.vue"

export default {
  component: Tooltip2,
  title: "NewComponents/Tooltip2",

  argTypes: { default: { control: { type: "text" } } },

  args: { default: "Some hover text" },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/eCWUinup52AoHQw1FBVJkd/HDS-(Hux-Design-System)?node-id=9409%3A68520",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { Tooltip2, Icon },
  props: Object.keys(argTypes),
  template: `
  <tooltip2 v-bind="$props">
    <template #label-content>
      <icon
        type="Informative"
        :size="20"
        color="white-base"
        outline
        borderColor="primary-base"
        bgColor="primary-base"
      />
    </template>
    <template #hover-content>
      ${args.default}
    </template>
  </tooltip2>`,
})

export const Tooltip = Template.bind({})
