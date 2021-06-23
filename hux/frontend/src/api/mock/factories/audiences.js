import faker from "faker"

export default {
  name: (index) => `My audience ${index + 1}`,
  size: () => faker.datatype.number({ min: 10000000, max: 999999999 }),
  last_delivered: () => faker.date.recent(),
  create_time: () => faker.date.recent(),
  created_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  update_time: () => faker.date.recent(),
  updated_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  audience_insights() {
    return {
      gender_men: 0.47,
      gender_women: 0.49,
      gender_other: 0.04,
      min_age: faker.datatype.number({ min: 20, max: 40 }),
      max_age: faker.datatype.number({ min: 40, max: 70 }),
      total_countries: faker.datatype.number({ min: 5, max: 10 }),
      total_us_states: faker.datatype.number({ min: 5, max: 30 }),
      total_cities: faker.datatype.number({ min: 10, max: 50 }),
      total_customers: faker.datatype.number(),
    }
  },
}
