import ConfirmModal from "./ConfirmModal.vue"
import HuxButton from "./huxButton.vue"
import AllIcons from "@/stories/icons/Icons"

export default {
  component: ConfirmModal,

  title: "Components/Modal",

  argTypes: {
    default: {
      control: {
        type: "text",
      },
    },
    icon: {
      options: AllIcons,
      control: {
        type: "select",
      },
    },
    type: { control: { type: "text" } },
    title: { control: { type: "text" } },
    subTitle: { control: { type: "text" } },
    rightBtnText: { control: { type: "text" } },
    leftBtnText: { control: { type: "text" } },
    onConfirm: { action: "Confirmed" },
  },

  args: {
    icon: "sad-face",
    type: "primary",
    title: "You are about to delete",
    subTitle: "My Audience 1",
    rightBtnText: "Yes, delete it",
    leftBtnText: "Nevermind!",
  },

  parameters: {
    design: {
      type: "figma",
      url: "",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { ConfirmModal, HuxButton },
  props: Object.keys(argTypes),
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
      @onCancel="openModal = !openModal"
      @onConfirm="openModal = !openModal"
    >
    ${args.default}
    </confirm-modal>
    <hux-button @click="openModal = true"> Open Modal</hux-button>
    </div>`,
})

export const Modal = Template.bind({})
