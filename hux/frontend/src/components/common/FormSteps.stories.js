import FormSteps from "./FormSteps.vue"
import FormStep from "./FormStep.vue"

export default {
  component: FormSteps,
  title: "Components",
  parameters: {},
}

const Template = () => ({
  components: { FormSteps, FormStep },
  data() {
    return {}
  },
  template: `
    <div>
    <v-subheader> Form Steps </v-subheader>
    <form-steps class="white pa-10">
      <form-step :step="1" label="General information" optional>
        Contents for step 1
      </form-step>

      <form-step :step="2" label="Select attribute(s)" border="inactive">
        Contents for step 2
      </form-step>

      <form-step :step="3" :disabled="true">
        Contents for disabled step 3
      </form-step>
    </form-steps>
        </div>`,
})

export const formSteps = Template.bind({})
