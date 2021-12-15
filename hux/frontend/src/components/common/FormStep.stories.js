import FormStep from "./FormStep.vue"

export default {
  component: FormStep,
  title: "Components",
  argTypes: {
    step: { control: { type: "number" } },
    label: { control: { type: "text" } },
    optional: { control: { type: "text" } },
    disabled: { control: { type: "boolean" } },
    border: { options: ["active", "inactive"], control: { type: "select" } },
  },
  args: {
    step: 1,
    label: "General Information",
    disabled: false,
    border: "active",
  },
  parameters: {},
}

const Template = (args, { argTypes }) => ({
  components: { FormStep },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div>
    <v-subheader> Form Step </v-subheader>
      <form-step 
      v-bind="$props"
      v-on="$props">
        Contents for step 1
      </form-step>
        </div>`,
})

export const formStep = Template.bind({})
