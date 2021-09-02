import faker from "faker"

export default {
  name: "Bluecore",

  type: "bluecore",

  is_enabled: false,

  is_added: false,

  status: "Pending",
}

/**
 * Data source's data feed schema
 */
const dataFeed = () => {
  return {
    name: `bluecore_data_feed_${faker.name.firstName()}`,

    status: "Pending",

    records_received: faker.datatype.number(),

    records_processed: faker.datatype.number(),

    records_processed_percentage: faker.datatype.number({
      min: 0,
      max: 1,
      precision: 0.01,
    }),

    thirty_days_avg: faker.datatype.number({ min: 0, max: 1, precision: 0.01 }),

    last_processed: faker.date.recent(),
  }
}

export const mockDataFeeds = (num = 3) => {
  return {
    name: "Bluecore",
    type: "bluecore",
    data_feeds: Array.from({ length: num }, dataFeed),
  }
}
