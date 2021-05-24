import faker from "faker"

const audienceMock = {
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
}

export default audienceFaker
