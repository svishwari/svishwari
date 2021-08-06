import faker from "faker"

const deliveriesSchema = () => faker.datatype.number({ min: 1, max: 10 })

const destinationSchema = () => {
  return {
    id: faker.datatype.number({ min: 1, max: 10 }),
    data_extension_id: faker.datatype.number({ min: 1, max: 10 }),
    delivery_platform_config: {
      data_extension_name: "faker data",
    },
    delivery_platform_type: "facebook",
    name: "Facebook",
    latest_delivery: {
      update_time: "2021-07-30T13:28:51.450Z",
      status: "Delivered",
      size: 1000,
    },
  }
}

const audienceData = () => {
  return {
    id: faker.datatype.number({ min: 1, max: 10 }),
    destinations: mockDestinations(3),
    // TODO: this may need to be updated based on HUS-579...
    deliveries: mockDeliveries(2),
  }
}

const mockAudiences = (numAudiences = 3) => {
  return Array.from({ length: numAudiences }, audienceData)
}

const mockDestinations = (numDestinations = 3) => {
  return Array.from({ length: numDestinations }, destinationSchema)
}

const mockDeliveries = (numDeliveries = 3) => {
  return Array.from({ length: numDeliveries }, deliveriesSchema)
}

/**
 * Engagement schema
 */
export const engagement = {
  name: () => faker.address.state(),
  description: () => "",
  delivery_schedule: () => ({
    start_date: faker.date.recent(),
    end_date: faker.date.soon(),
  }),
  audiences: () => mockAudiences(1),
  size: () => faker.datatype.number({ min: 10000000, max: 999999999 }),
  create_time: () => faker.date.recent(),
  created_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  update_time: () => faker.date.recent(),
  updated_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  status: () => "Active",
  campaign_performance: {},
  campaign_mappings: {}, // This will enable us to maintain the mapping saved by user for the respective destination.
}
