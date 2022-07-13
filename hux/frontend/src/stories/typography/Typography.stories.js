const FontTypes = [
  "new-h1",
  "new-h2",
  "new-h3",
  "new-h4",
  "new-b1",
  "new-b2",
  "new-b3",
  "new-b4",
  "new-pills",
  "new-secondary-label",
]
const masterList = [
  {
    class: "new-h1",
    title: "H1 (Page header)",
    size: "32px",
    weight: "300",
    lineHeight: "40px",
    letterSpace: "0",
  },
  {
    class: "new-h2",
    title: "H2 (Modal, Drawer Header)",
    size: "28px",
    weight: "300",
    lineHeight: "40px",
    letterSpace: "0.25px",
  },
  {
    class: "new-h3",
    title: "H3 (Small card title)",
    size: "20px",
    weight: "700",
    lineHeight: "24px",
    letterSpace: "0.15px",
  },
  {
    class: "new-h4",
    title: "H4 (Large card title)",
    size: "20px",
    weight: "400",
    lineHeight: "24px",
    letterSpace: "0",
  },
  {
    class: "new-b1",
    title: "B1 (Primary body text)",
    size: "16px",
    weight: "400",
    lineHeight: "24px",
    letterSpace: "0",
  },
  {
    class: "new-b2",
    title: "B2 (Clickable text)",
    size: "14px",
    weight: "600",
    lineHeight: "24px",
    letterSpace: "0",
  },
  {
    class: "new-b3",
    title: "B3 (Button text)",
    size: "14px",
    weight: "700",
    lineHeight: "20px",
    letterSpace: "0.2px",
  },
  {
    class: "new-b4",
    title: "B4 (Hovers)",
    size: "14px",
    weight: "400",
    lineHeight: "20px",
    letterSpace: "0",
  },
  {
    class: "new-pills",
    title: "Pills & Chips",
    size: "12px",
    weight: "700",
    lineHeight: "20px",
    letterSpace: "0",
  },
  {
    class: "new-secondary-label",
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
          "new-h1": "H1 (Page header)",
          "new-h2": "H2 (Modal, Drawer Header)",
          "new-h3": "H3 (Small card title)",
          "new-h4": "H4 (Large card title)",
          "new-b1": "B1 (Primary body text)",
          "new-b2": "B2 (Clickable text)",
          "new-b3": "B3 (Button text)",
          "new-b4": "B4 (Hovers)",
          "new-pills": "Pills & Chips",
          "new-secondary-label": "Forms",
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
