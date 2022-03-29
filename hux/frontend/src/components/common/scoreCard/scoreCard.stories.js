import ScoreCard from "./scoreCard.vue"
const ICON = [
    'hx-trustid',
    'hx-trustid-colored'
]
const TITLE = [
    'Transparency',
    'Humanity'
]
export default {
    component: scoreCard,
    title: "Components",
    argTypes: {
        width: {
            control: { type: "number" },
        },
        height: {
            control: { type: "number" },
        },
        active: {
            control: { type: "boolean" },
        },
        icon: {
            options: ICON,
            control: { type: "select" },
        },
        title: {
            options: TITLE,
            control: { type: "select" },
        },
        value: {
            control: { type: "number" },
        },
    },
    args: {
        width: 150,
        height: 90,
        active: false,
        icon: "hx-trustid",
        title: "Humanity",
        value: 89,
    },
    parameters: {
        design: {
            type: "figma",
            url: "",
        },
    },
}
const Template = (args, { argTypes }) => ({
    components: { ScoreCard },
    props: Object.keys(argTypes),
    data() {
        return {}
    },
    template: `<score-card  v-bind="$props" v-on="$props" />`,
})
export const scoreCard = Template.bind({})
