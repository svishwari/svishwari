import faker from "faker"

export default {
  name: "Default",

  type: "default",

  engagements() {
    return faker.datatype.number({ min: 0, max: 9 })
  },

  added() {
    return faker.date.past()
  },

  added_by() {
    return `${faker.name.firstName()} ${faker.name.lastName()}`
  },

  updated() {
    return faker.date.past()
  },

  updated_by() {
    return `${faker.name.firstName()} ${faker.name.lastName()}`
  },

  is_enabled: true,

  is_added: false,

  auth_details: {
    access_token: {
      name: "Access Token",
      type: "password",
      required: true,
      description: "This field is required for...",
    },
  },
}
