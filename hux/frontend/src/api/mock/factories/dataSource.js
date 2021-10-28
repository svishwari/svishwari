import faker from "faker"

export default {
  name: "Bluecore",

  type: "bluecore",

  is_enabled: false,

  is_added: false,

  status: "Pending",

  feed_count: () => faker.datatype.number({ min: 1, max: 20 }),

  category: () =>
    faker.random.arrayElement([
      "Internet",
      "Productivity",
      "Marketing",
      "Databases",
    ]),
}

/**
 * Data source's single data feed schema
 *
 * @param {string} type data type
 * @returns {object} datafeed
 */
const dataFeed = (type) => {
  return {
    name: `${type}_data_feed_${faker.name.firstName()}`.toLowerCase(),

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

/**
 * Data source's data feeds schema
 *
 * @param {object} dataFeed config
 * @param {string} dataFeed.name data feed name
 * @param {string} dataFeed.type data feed type
 * @returns {object} data feeds response schema
 */
export const dataFeeds = ({ name, type }) => {
  let num = faker.datatype.number(100)

  if (type === "aqfer") num = 0

  return {
    name: name,

    type: type,

    datafeeds: Array.from({ length: num }, () => dataFeed(type)),
  }
}
