import TabsContainer from "./TabsContainer.vue"

export default {
  component: TabsContainer,

  title: "NewComponents/Tabs",

  argTypes: {},

  args: {},

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { TabsContainer },
  props: Object.keys(argTypes),
  template: `
    <tabs-container v-bind="$props" >
      <template #web>no way</template>
      <template #shopping>no wayyyyyy</template>
      <template #videos>no wayyyyyyyyyyyyyyyyyyy</template>
      <template #images>this is so cool</template>
      <template #news>soooooooooo cool bro</template>
    </tabs-container>
  `,
})

export const Default = Template.bind({})
