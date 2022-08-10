import Icon from "../icons/Icon2.vue"
import Hover from "./Hover.vue"

export default {
  component: Hover,
  title: "NewComponents/Hover",

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
  components: { Hover, Icon },
  props: Object.keys(argTypes),
  template: `
  <hover v-bind="$props">
    <template #label-content>
      <icon
        type="Informative"
        :size="16"
        color="white-base"
        outline
        borderColor="primary-base"
        bgColor="primary-base"
      />
    </template>
    <template #hover-content>
      ${args.default}
    </template>
  </hover>`,
})

export const MyHover = Template.bind({})
