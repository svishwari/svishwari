import CardHorizontal from "./CardHorizontal.vue"
import AllLogos from "@/stories/logos/Logos"

export default {
  component: CardHorizontal,
  title: "Components",
  argTypes: {
    icon: {
      options: AllLogos,
      control: { type: "select" },
    },

    title: {
      control: { type: "text" },
    },

    isAdded: {
      control: { type: "boolean" },
    },

    isAvailable: {
      control: { type: "boolean" },
    },

    isAlreadyAdded: {
      control: { type: "boolean" },
    },

    hideButton: {
      control: { type: "boolean" },
    },

    enableBlueBackground: {
      control: { type: "boolean" },
    },

    to: {
      control: { type: "object" },
    },
    requestedButton: {
      control: { type: "boolean" },
    },
    isModelRequested: {
      control: { type: "boolean" },
    },
  },
  args: {
    icon: "google-ads",

    title: "Google Ads",

    isAdded: false,

    isAvailable: true,

    isAlreadyAdded: false,

    hideButton: false,

    enableBlueBackground: false,

    to: () => {},

    requestedButton: false,
    isModelRequested: false,
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A235247",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { CardHorizontal },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div class="mx-auto" style="width:40%">
      <card-horizontal
        v-bind="$props"
        v-on="$props"
      />
    </div>`,
})

export const cardHorizontal = Template.bind({})
