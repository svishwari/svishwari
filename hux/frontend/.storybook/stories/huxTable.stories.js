import HuxTable from '../../src/components/huxTable.vue';

export default {
  component: HuxTable,
  title: 'Components/HuxTable',
};

export const Primary = () => ({
  components: { HuxTable },
  template: '<HuxTable primary label="Button" />',
});