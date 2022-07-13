import PlainCard from "./PlainCard.vue"
import Icon from "../icons/Icon2.vue"
import EmptyPage from "@/components/common/EmptyPage"
import AllIcons from "../icons/Icons"
import AllColors from "../colors/allColors"

export default {
  component: PlainCard,
  title: "NewComponents/Cards",
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
    iconType: {
      options: AllIcons,
      control: {
        type: "select",
      },
    },
    iconColor: {
      options: AllColors,
      control: {
        type: "select",
      },
    },
    iconBorderColor: {
      options: AllColors,
      control: {
        type: "select",
      },
    },
    iconBgColor: {
      options: AllColors,
      control: {
        type: "select",
      },
    },
    error: {
      control: { type: "boolean" },
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
            <icon type="Icon Placeholder" size="22" color="primary-base" />
            <icon type="Icon Placeholder" size="22" color="primary-base" />
            <icon type="Icon Placeholder" size="22" color="primary-base" />
            <icon type="Icon Placeholder" size="22" color="primary-base" />
          </span>
        </template>
        <template #body>
          <empty-page
            v-if="$props.error"
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
          <div v-else>Empty content</div>
        </template>
      </plain-card>
    </div>`,
})

export const Default = Template.bind({})
