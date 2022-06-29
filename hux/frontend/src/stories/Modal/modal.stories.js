import Modal from "./Modal.vue"
import HuxButton from "@/components/common/huxButton.vue"
import { action } from "@storybook/addon-actions"
import allIcons from "../icons/Icons"
import allColors from "../colors/allColors"

export default {
  component: Modal,

  title: "NewComponents/Modal",

  argTypes: {
    title: { control: "text" },
    icon: {
      options: allIcons,
      control: { type: "select" },
    },
    type: {
      options: ["primary", "secondary", "error", "warning"],
      control: { type: "select" },
    },
    iconColor: {
      options: allColors,
      control: { type: "select" },
    },
    body: { control: "text" },
    cancelBtnText: { control: "text" },
    backBtnText: { control: "text" },
    confirmBtnText: { control: "text" },
    value: { control: "boolean" },
    width: { control: "number" },
    isDisabled: { control: "boolean" },
    showBack: { control: "boolean" },
    showConfirm: { control: "boolean" },
    showCancel: { control: "boolean" },
  },

  args: {
    title: "Header",
    icon: "Cookie",
    iconColor: "primary-base",
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

export const ModalComponent = Template.bind({})
