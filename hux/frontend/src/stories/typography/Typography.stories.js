const FontTypes = [
  "text-h1",
  "text-h2",
  "text-h3",
  "text-h4",
  "text-body-1",
  "text-body-2",
  "text-button",
  "text-body-4",
  "text-subtitle-2",
  "text-form",
]
const masterList = [
  {
    class: "text-h1",
    title: "H1 (Page header)",
    size: "32px",
    weight: "300",
    lineHeight: "40px",
    letterSpace: "0",
  },
  {
    class: "text-h2",
    title: "H2 (Modal, Drawer Header)",
    size: "28px",
    weight: "300",
    lineHeight: "40px",
    letterSpace: "0.25px",
  },
  {
    class: "text-h3",
    title: "H3 (Small card title)",
    size: "20px",
    weight: "700",
    lineHeight: "24px",
    letterSpace: "0.15px",
  },
  {
    class: "text-h4",
    title: "H4 (Large card title)",
    size: "20px",
    weight: "400",
    lineHeight: "24px",
    letterSpace: "0",
  },
  {
    class: "text-body-1",
    title: "B1 (Primary body text)",
    size: "16px",
    weight: "400",
    lineHeight: "24px",
    letterSpace: "0",
  },
  {
    class: "text-body-2",
    title: "B2 (Clickable text)",
    size: "14px",
    weight: "600",
    lineHeight: "24px",
    letterSpace: "0",
  },
  {
    class: "text-button",
    title: "B3 (Button text)",
    size: "14px",
    weight: "700",
    lineHeight: "20px",
    letterSpace: "0.2px",
  },
  {
    class: "text-body-4",
    title: "B4 (Hovers)",
    size: "14px",
    weight: "400",
    lineHeight: "20px",
    letterSpace: "0",
  },
  {
    class: "text-subtitle-2",
    title: "Pills & Chips",
    size: "12px",
    weight: "700",
    lineHeight: "20px",
    letterSpace: "0",
  },
  {
    class: "text-form",
    title: "Forms",
    size: "12px",
    weight: "400",
    lineHeight: "20px",
    letterSpace: "0",
  },
]

const Template = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  template: "<div><span v-bind='$props'>{{$props.label}}</span></div>",
})

export default {
  title: "Design System/Typography",
  argTypes: {
    class: {
      options: FontTypes,
      mapping: masterList,
      control: {
        type: "select",
        labels: {
          // 'labels' maps option values to string labels
          "text-h1": "H1 (Page header)",
          "text-h2": "H2 (Modal, Drawer Header)",
          "text-h3": "H3 (Small card title)",
          "text-h4": "H4 (Large card title)",
          "text-body-1": "B1 (Primary body text)",
          "text-body-2": "B2 (Clickable text)",
          "text-button": "B3 (Button text)",
          "text-body-4": "B4 (Hovers)",
          "text-subtitle-2": "Pills & Chips",
          "text-form": "Forms",
        },
      },
    },
    label: {
      defaultValue: "Heading",
      control: {
        type: "text",
      },
    },
  },
}

export const Default = Template.bind({})
