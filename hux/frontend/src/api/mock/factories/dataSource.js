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
 * @param {string} date data date
 * @returns {object} datafeed
 */
const dataFeed = (type, date = null) => {
  return {
    name: `${type}_data_feed_${faker.name.firstName()}`.toLowerCase(),

    status: faker.random.arrayElement(["Pending", "Active", "Error"]),

    records_received: faker.datatype.number(),

    records_processed: faker.datatype.number(),

    records_processed_percentage: faker.datatype.number({
      min: 0,
      max: 1,
      precision: 0.01,
    }),

    thirty_days_avg: faker.datatype.number({ min: 0, max: 1, precision: 0.01 }),

    last_processed: date ? date : faker.date.recent(),
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

/**
 * Data source's single data feed schema
 *
 * @param {string} type data type
 * @returns {object} datafeed
 */
export const dataFeedDetailsSchema = (type) => {
  let num = faker.datatype.number(100)
  let date = faker.date.recent()

  return {
    name: date,

    status: faker.random.arrayElement([
      "Success",
      "Failed",
      "Running",
      "Canceled",
    ]),

    records_received: faker.datatype.number(),

    records_processed: faker.datatype.number(),

    records_processed_percentage: faker.datatype.number({
      min: 0,
      max: 1,
      precision: 0.01,
    }),

    thirty_days_avg: faker.datatype.number({ min: 0, max: 1, precision: 0.01 }),

    last_processed: date,
    data_files: Array.from({ length: num }, () => dataFeed(type, date)),
  }
}

/**
 * Data source's data feeds details schema
 *
 * @param {string} type data feed type
 * @returns {Array} data feeds response schema
 */
export const dataFeedDetails = (type) => {
  let num = faker.datatype.number(100)
  return Array.from({ length: num }, () => dataFeedDetailsSchema(type))
}
