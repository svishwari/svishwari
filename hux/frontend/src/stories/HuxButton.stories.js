import huxButton from "../components/common/huxButton.vue"

export default {
  title: "Library/HuxButton",
  component: huxButton,
  argTypes: {
    variant: {
      control: {
        type: "select",
        options: ["primary", "tertiary", "success", "secondary"],
      },
    },
  },
}

const Template = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  components: { huxButton },
  template: `<huxButton 
              size="large" 
              class="ma-2" 
              v-bind="$props"> 
              Added 
            </huxButton>`,
})

export const Primary = Template.bind({})
