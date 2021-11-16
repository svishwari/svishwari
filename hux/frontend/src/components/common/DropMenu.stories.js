import TipsMenu from "../../views/SegmentPlayground/TipsMenu"
export default {
  component: TipsMenu,
  title: "Components/TipsMenu",
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=6852%3A134015",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { TipsMenu },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div class="ml-5 mt-n10">
        <tips-menu />
    </div>
        `,
})

export const Tips = Template.bind({})
