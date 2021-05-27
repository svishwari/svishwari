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
