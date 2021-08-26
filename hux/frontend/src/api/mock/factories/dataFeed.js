import faker from "faker"

export default {
  name: (index) => `bluecore_data_feed_${index + 1}`,

  status: "Pending",

  records_received: faker.datatype.number(),

  records_processed: faker.datatype.number(),

  records_processed_percentage: faker.datatype.number({
    min: 0,
    max: 1,
    precision: 0.01,
  }),

  day_avg_30: faker.datatype.number({ min: 0, max: 1, precision: 0.01 }),

  last_processed: faker.date.recent(),
}
