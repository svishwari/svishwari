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
    type: {
      options: ["success", "info", "warning", "error"],
      control: { type: "select" },
    },
    iconColor: {
      options: ["success", "info", "warning", "error"],
      control: { type: "select" },
    },
    title: { control: { type: "text" } },
    subTitle: { control: { type: "text" } },
    rightBtnText: { control: { type: "text" } },
    leftBtnText: { control: { type: "text" } },
    onConfirm: { action: "Confirmed" },
  },

  args: {
    icon: "sad-face",
    iconColor: "warning",
    type: "warning",
    title: "You are about to delete",
    subTitle: "My Audience 1",
    rightBtnText: "Yes, delete it",
    leftBtnText: "Nevermind!",
    body: "",
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
    <template #body>${args.body}</template>
    
    </confirm-modal>
    <hux-button @click="openModal = true"> Open Modal</hux-button>
    </div>`,
})

export const BasicModal = Template.bind({})
export const Template1 = Template.bind({})
Template1.args = {
  body: `<div
          class="
            black--text
            text--darken-4 text-subtitle-1
            pt-6
            font-weight-regular
          "
        >
          Are you sure you want to delete this audience&#63;
        </div>
        <div
          class="black--text text--darken-4 text-subtitle-1 font-weight-regular"
        >
          By deleting this audience you will not be able to recover it and it
          may impact any associated engagements.
        </div>`,
}
