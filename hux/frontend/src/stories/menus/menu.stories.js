import HuxMenu from "./HuxMenu.vue"

export default {
  component: HuxMenu,

  title: "NewComponents/Menu",

  argTypes: {
    
  },

  args: {
    
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { HuxMenu },
  props: Object.keys(argTypes),
  template: `
    <hux-menu v-bind="$props" >
      
    </hux-menu>
  `,
})

export const Default = Template.bind({})
