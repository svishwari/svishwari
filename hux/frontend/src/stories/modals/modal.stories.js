import Modal from "./Modal.vue"
import HuxButton from "../../components/common/huxButton.vue"
import { action } from "@storybook/addon-actions"

export default {
  component: Modal,

  title: "Components/NewModal",

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
    showConfirm: { control: 'boolean' },
    showCancel: { control: 'boolean' },
  },

  args: {
    title: "Header",
    icon: "exclamation_outline",
    iconColor: "warning",
    type: "warning",
    body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Amet suscipit maecenas egestas at sed.",
    showBack: "false",
    showConfirm: "true",
    showCancel: "true",
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
Negative.args = {
  type: "error",
  icon: "trash_in_circle",
  confirmBtnText: "Danger",
  width: 600,
  showBack: false,
}
export const Confirmative = Template.bind({})
Confirmative.args = {
  type: "primary",
}

export const Informative = Template.bind({})
Informative.args = {
  icon: "FAB_circle_bulb",
  type: "error",
  showCancel: "false",
  showBack: "false",
  type: "primary",
  confirmBtnText: "OK"
}
