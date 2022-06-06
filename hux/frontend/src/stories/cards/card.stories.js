import PlainCard from "./PlainCard.vue"
import Icon from "../icons/Icon2.vue"
import EmptyPage from "@/components/common/EmptyPage"

export default {
  component: PlainCard,
  title: "Design System/Cards",
  argTypes: {
    title: { control: { type: "text" } },
    size: {
      defaultValue: "small",
      options: ["small", "medium", "large"],
      control: {
        type: "select",
      },
    },
    actionMenu: {
      control: { type: "boolean" },
    },
    cardBody: {
      defaultValue: "empty",
      options: ["empty", "error"],
      control: {
        type: "select",
      },
    },
  },
  args: {
    title: "Card Title",
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A256774",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { PlainCard, Icon, EmptyPage },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div>
      <plain-card v-bind="$props">
        <template #call-to-action v-if="$props.actionMenu">
          <span>
            <icon type="success" size="22" />
            <icon type="success" size="22" />
            <icon type="success" size="22" />
            <icon type="success" size="22" />
          </span>
        </template>
        <template #body>
          <div v-if="$props.cardBody == 'empty'">Empty content</div>
          <empty-page
            v-else
            type="error-on-screens"
            :size="40"
          >
            <template #title>
              <div>Unavailable</div>
            </template>
            <template #subtitle>
              <div>
                Our team is working hard to fix it. Please be patient and try again soon!
              </div>
            </template>
          </empty-page>
        </template>
      </plain-card>
    </div>`,
})

export const Default = Template.bind({})
