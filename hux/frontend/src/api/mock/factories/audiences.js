import faker from "faker"

const audienceMock = {
  name(i) {
    return `Audience ${i + 1}`
  },

  size() {
    return faker.datatype.number({ min: 10000000, max: 999999999 })
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
  /*
   * TO DO
   * Later this need to be mapped to destination IDs and engagement IDs
   */
  destinations() {
    return faker.datatype.array(faker.datatype.hexaDecimal)
  },
  engagements() {
    return faker.datatype.array(faker.datatype.hexaDecimal)
  },
}
export default audienceMock
