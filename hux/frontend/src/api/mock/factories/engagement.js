import faker from "faker"

const audienceData = () => {
  return {
    id: aker.datatype.number({ min: 1, max: 10 }),
    destinations: {
      id: "60ae035b6c5bf45da27f17d6",
      data_extension_id: "data_extension_id",
      contact_list: "sfmc_extension_name",
    },
    deliveries: ["60ae035b6c5bf45da27f17e5", "60ae035b6c5bf45da27f17e6"],
  }
}

const createAudiences = (numAudiences = 3) => {
  return Array.from({ length: numAudiences }, audienceData)
}

const engagementMock = {
  name() {
    return `${faker.address.state()}`
  },

  description: `Engagement for ${faker.address.state()}`,

  delivery_schedule() {
    return {
      start_date: faker.date.past(),
      end_date: faker.date.past(),
    }
  },

  status() {
    return "Active"
  },

  size() {
    return 64000
  },

  audiences() {
    return createAudiences(2)
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
export default engagementMock
