import faker from "faker"

const audienceFaker = {
  name(i) {
    return `Audience ${i + 1}`
  },

  size() {
    return faker.finance.account()
  },
  create_time() {
    return faker.date.past()
  },

  created_by() {
    return `${faker.name.firstName()} ${faker.name.lastName()}`
  },

  update_time() {
    return faker.date.past()
  },

  updated_by() {
    return `${faker.name.firstName()} ${faker.name.lastName()}`
  },
  audience_insights() {
    return {
      gender_men: faker.datatype.number({ min: 1, max: 50 }),
      gender_women: faker.datatype.number({ min: 51, max: 90 }),
      gender_other: faker.datatype.number({ min: 91, max: 100 }),
      min_age: faker.datatype.number({ min: 20, max: 40 }),
      max_age: faker.datatype.number({ min: 40, max: 70 }),
      total_countries: faker.datatype.number({ min: 5, max: 10 }),
      total_us_states: faker.datatype.number({ min: 5, max: 30 }),
      total_cities: faker.datatype.number({ min: 10, max: 50 }),
      total_customerss: faker.datatype.number(),
    }
  },
}

export default audienceFaker
