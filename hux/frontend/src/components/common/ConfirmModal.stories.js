import ConfirmModal from "./ConfirmModal.vue"
import HuxButton from "./huxButton.vue"
import { action } from "@storybook/addon-actions"

export default {
  component: ConfirmModal,

  title: "Components/Modal",

  argTypes: {
    default: {
      control: {
        type: "text",
      },
    },
    type: {
      options: ["success", "info", "warning", "error"],
      control: { type: "select" },
    },
    iconColor: {
      options: ["success", "info", "warning", "error"],
      control: { type: "select" },
    },
    subTitle: { control: { type: "text" } },
    rightBtnText: { control: { type: "text" } },
    leftBtnText: { control: { type: "text" } },
    icon: { table: { disable: true } },
    title: { table: { disable: true } },
    body: { table: { disable: true } },
    activator: { table: { disable: true } },
    "sub-title": { table: { disable: true } },
    footer: { table: { disable: true } },
    input: { table: { disable: true } },
    onClose: { table: { disable: true } },
    onCancel: { table: { disable: true } },
    onConfirm: { table: { disable: true } },
  },

  args: {
    icon: "sad-face",
    iconColor: "warning",
    type: "warning",
    title: "You are about to delete [Audience Name]",
    subTitle: "Are you sure you want to delete this audience?",
    rightBtnText: "Yes, delete it",
    leftBtnText: "Nevermind!",
    body: "",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=6852%3A108904",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { ConfirmModal, HuxButton },
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
    <confirm-modal
      v-model="openModal"
      v-bind="$props"
      v-on="$props"
      @onCancel="onCancel()"
      @onConfirm="onConfirm()"
    />
      <hux-button @click="openModal = true"> Open Modal</hux-button>
    </div>`,
})

export const BasicModal = Template.bind({})
export const InfoModal = Template.bind({})
InfoModal.args = {
  body: "Are you sure you want to delete this audience? By deleting this audience you will not be able to recover it and it may impact any associated engagements.",
}

export const ErrorModal = Template.bind({})
ErrorModal.args = {
  icon: "sad-face",
  type: "error",
  title: "Action Word",
  subTitle: "(i.e. Remove) ___________?",
  body: "Are you sure you want to stop the configuration and go to another page? You will not be able to recover it but will need to start the process again.",
}
