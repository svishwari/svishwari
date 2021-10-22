const FontTypes = [
  "text-h1",
  "text-h2",
  "text-h3",
  "text-h4",
  "text-body-1",
  "text-body-2",
  "text-button",
  "text-subtitle-1",
  "text-subtitle-2",
  "text-caption",
  "text-h5",
  "text-h6",
]
const masterList = [
  {
    class: "text-h1",
    title: "H1 (Large) (Main Pages)",
    size: "28px",
    weight: "300",
    lineHeight: "40px",
    letterSpace: "0",
  },
  {
    class: "text-h2",
    title: "H2 (Models & Drawers)",
    size: "24px",
    weight: "300",
    lineHeight: "40px",
    letterSpace: "0",
  },
  {
    class: "text-h3",
    title: "H3 (Sm) (Sectionals)",
    size: "18px",
    weight: "400",
    lineHeight: "25px",
    letterSpace: "0",
  },
  {
    class: "text-h4",
    title: "H4 (Card Headers)",
    size: "18px",
    weight: "300",
    lineHeight: "24px",
    letterSpace: "0",
  },
  {
    class: "text-body-1",
    title: "B1 (Reg)",
    size: "16px",
    weight: "400",
    lineHeight: "22px",
    letterSpace: "0",
  },
  {
    class: "text-body-2",
    title: "B2 (Sm) - Hovers & Labels",
    size: "14px",
    weight: "400",
    lineHeight: "16px",
    letterSpace: "0",
  },
  {
    class: "text-button",
    title: "Button Text",
    size: "16px",
    weight: "400",
    lineHeight: "20px",
    letterSpace: "0.5px",
  },
  {
    class: "text-subtitle-1",
    title: "Metric #s",
    size: "16px",
    weight: "600",
    lineHeight: "22px",
    letterSpace: "0",
  },
  {
    class: "text-subtitle-2",
    title: "Pill Text",
    size: "12px",
    weight: "600",
    lineHeight: "16px",
    letterSpace: "0.2px",
  },
  {
    class: "text-caption",
    title: "'optional'",
    size: "16px",
    weight: "600",
    lineHeight: "22px",
    letterSpace: "0",
  },
  {
    class: "text-h5",
    title: "Nav > Headers",
    size: "14px",
    weight: "400",
    lineHeight: "16px",
    letterSpace: "0.2",
  },
  {
    class: "text-h6",
    title: "Nav > Menu item 1",
    size: "14px",
    weight: "400",
    lineHeight: "22px",
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
          "text-h1": "H1 (Large) (Main Pages)",
          "text-h2": "H2 (Models & Drawers)",
          "text-h3": "H3 (Sm) (Sectionals)",
          "text-h4": "H4 (Card Headers)",
          "text-body-1": "B1 (Reg)",
          "text-body-2": "B2 (Sm) - Hovers & Labels",
          "text-button": "Button Text",
          "text-subtitle-1": "Metric #s",
          "text-subtitle-2": "Pill Text",
          "text-caption": "'optional'",
          "text-h5": "Nav > Headers",
          "text-h6": "Nav > Menu item",
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
