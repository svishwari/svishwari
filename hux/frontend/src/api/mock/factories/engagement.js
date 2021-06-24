import faker from "faker"

const deliveriesData = () => faker.datatype.number({ min: 1, max: 10 })

const destinationData = () => {
  return {
    id: faker.datatype.number({ min: 1, max: 10 }),
    data_extension_id: faker.datatype.number({ min: 1, max: 10 }),
    contact_list: "faker data",
  }
}

const audienceData = () => {
  return {
    id: faker.datatype.number({ min: 1, max: 10 }),
    destinations: createDestinations(3),
    deliveries: createDeliveries(2),
  }
}

const createAudiences = (numAudiences = 3) => {
  return Array.from({ length: numAudiences }, audienceData)
}

const createDestinations = (numDestinations = 3) => {
  return Array.from({ length: numDestinations }, destinationData)
}

const createDeliveries = (numDeliveries = 3) => {
  return Array.from({ length: numDeliveries }, deliveriesData)
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
