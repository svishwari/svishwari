import faker from "faker"

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
      next_delivery: "2021-08-12T14:23:11.250Z",
      delivery_schedule: faker.random.arrayElement([
        "Daily",
        "Weekly",
        "Monthly",
      ]),
      status: faker.random.arrayElement([
        "Delivered",
        "Delivering",
        "Not Delivered",
        "Error",
      ]),
      size: faker.datatype.number({ min: 0, max: 10000 }),
      match_rate: faker.datatype.number({ min: 0, max: 1, precision: 0.001 }),
    },
    create_time: () => faker.date.recent(),
    created_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
    update_time: () => faker.date.recent(),
    updated_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  }
}

const audienceData = () => {
  return {
    id: `${faker.datatype.number({ min: 1, max: 10 })}`,
    name: `Audience for ${faker.company.companyName()}`,
    status: faker.random.arrayElement([
      "Delivered",
      "Delivering",
      "Not Delivered",
      "Error",
    ]),
    create_time: () => faker.date.recent(),
    created_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
    update_time: () => faker.date.recent(),
    updated_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
    destinations: mockDestinations(3),
  }
}

const mockAudiences = (numAudiences = 3) => {
  return Array.from({ length: numAudiences }, audienceData)
}

const mockDestinations = (numDestinations = 3) => {
  return Array.from({ length: numDestinations }, destinationSchema)
}

/**
 * Engagement schema
 */
export const engagement = {
  name: () => faker.address.state(),
  description: () => "",
  delivery_schedule: () => ({
    start_date: faker.date.past(),
    end_date: faker.date.soon(),
  }),
  audiences: () => mockAudiences(faker.datatype.number({ min: 2, max: 5 })),
  size: () => faker.datatype.number({ min: 10000000, max: 999999999 }),
  create_time: () => faker.date.recent(),
  created_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  update_time: () => faker.date.recent(),
  updated_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  status: faker.random.arrayElement(["Active", "Delivering", "Not Delivered"]),
  campaign_performance: {},
  campaign_mappings: {}, // This will enable us to maintain the mapping saved by user for the respective destination.
}
