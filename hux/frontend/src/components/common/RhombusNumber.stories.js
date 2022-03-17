import RhombusNumber from './RhombusNumber'
export default {
    component: RhombusNumber,
    title: "Components",
}

const Template = () => ({
  components: { RhombusNumber },
  template: `
    <RhombusNumber value="10" color="blue"/>
  `,
})
export const Rhombus = Template.bind({})