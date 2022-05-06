import Modal from "./Modal.vue"
import HuxButton from "../../components/common/huxButton.vue"
import { action } from "@storybook/addon-actions"

export default {
  component: Modal,

  title: "Components/MyModal",

  argTypes: {
    title: { control: 'text' },
    icon: { table: { disable: true } },
    type: { table: { disable: true } },
    iconColor: {
      options: ["success", "info", "warning", "error"],
      control: { type: "select" },
    },
    body: { control: 'text' },
    cancelBtnText: { control: 'text' },
    backBtnText: { control: 'text' },
    confirmBtnText: { control: 'text' },
    value: { control: 'boolean' },
    width: { control: 'number' },
    isDisabled: { control: 'boolean' },
    showBack: { control: 'boolean' },
    showConfirm: { table: { disable: true } },
  },

  args: {
    title: "Header",
    icon: "exclamation_outline",
    iconColor: "warning",
    type: "warning",
    body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Amet suscipit maecenas egestas at sed.",
    showBack: "true",
  },
}

const Template = (args, { argTypes }) => ({
  components: { Modal, HuxButton },
  props: Object.keys(argTypes),
  methods: {
    openModal: action("openModal"),
    onCancel: action("onCancel"),
    onConfirm: action("onConfirm"),
  },
  argTypes: {
    onCancel: {},
    onConfirm: {},
  },
  data() {
    return {
      openModal: false,
    }
  },
  template: `
  <div>
    <modal
      v-model="openModal"
      v-bind="$props"
      v-on="$props"
      @onCancel="onCancel()"
      @onConfirm="onConfirm()"
    />
      <hux-button @click="openModal = true"> Open Modal</hux-button>
    </div>`,
})

export const Negative = Template.bind({})
export const Confirmative = Template.bind({})
Confirmative.args = {
  body: "Are you sure you want to delete this audience? By deleting this audience you will not be able to recover it and it may impact any associated engagements.",
}

export const Informative = Template.bind({})
Informative.args = {
  icon: "sad-face",
  type: "error",
  title: "Action Word",
  subTitle: "(i.e. Remove) ___________?",
  body: "Are you sure you want to stop the configuration and go to another page? You will not be able to recover it but will need to start the process again.",
}
