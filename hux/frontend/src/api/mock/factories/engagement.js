import faker from "faker"

export default {
  name: "New York Engagement",
  description: "Engagement for New York",
  delivery_schedule: {
    schedule_type: "recurring",
    start_date: "01/05/2021",
    end_date: "01/14/2021",
  },

  audiences() {
    return faker.datatype.number({ min: 0, max: 9 })
  },

  created() {
    return faker.date.past()
  },

  created_by() {
    return `${faker.name.firstName()} ${faker.name.lastName()}`
  },

  updated() {
    return faker.date.past()
  },

  updated_by() {
    return `${faker.name.firstName()} ${faker.name.lastName()}`
  },

}
