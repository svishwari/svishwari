import Tooltip from ""

export default {
  component: Tooltip,

  title: "NewComponents/Tooltip",

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
  components: { Tooltip },
  props: Object.keys(argTypes),
  template: `
    <tooltip v-bind="$props" >
      
    </tooltip>
  `,
})

export const Default = Template.bind({})
