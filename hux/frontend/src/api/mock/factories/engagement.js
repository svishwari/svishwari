import faker from "faker"

export default {
  name() {
    return `${faker.address.state()}`
  },
  description: `Engagement for ${faker.address.state()}`,
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
