import faker from "faker"

export default {
  name: "Facebook",

  type: "facebook",

  engagements() {
    return faker.datatype.number({ min: 0, max: 10 })
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
    ad_account_id: {
      name: "Ad Account ID",
      type: "password",
      required: true,
      description: "This field is required for...",
    },
    app_id: {
      name: "App ID",
      type: "password",
      required: true,
      description: "This field is required for...",
    },
    access_token: {
      name: "Access Token",
      type: "password",
      required: true,
      description: "This field is required for...",
    },
    app_secret: {
      name: "App Secret",
      type: "password",
      required: true,
      description: "This field is required for...",
    },
  },
}
