import faker from "faker"
import { customersOverview } from "./customers"

/**
 * Identity resolution data feeds schema
 */
export const idrDataFeed = {
  datafeed_id: () => faker.datatype.hexaDecimal(22),

  data_source_type: () => "bluecore",

  new_ids_generated: () => faker.datatype.number({ min: 1, max: 2000 }),

  match_rate: () => faker.datatype.float({ min: 0.9, max: 1 }),

  last_run: () => faker.date.recent(21),

  datafeed_name: () => {
    const name = "Really_long_Feed_Name"
    const number = faker.datatype.number({ min: 100, max: 200 })
    return `${name}_${number}`
  },

  num_records_processed: () => {
    return faker.datatype.number({ min: 2000000, max: 2050000 })
  },
}

/**
 * Identity resolution overview schema
 */
export const idrOverview = {
  match_rate: customersOverview.match_rate,

  total_household_ids: customersOverview.total_household_ids,

  total_individual_ids: customersOverview.total_individual_ids,

  total_known_ids: customersOverview.total_known_ids,

  total_records: customersOverview.total_records,

  total_unique_ids: customersOverview.total_unique_ids,

  total_unknown_ids: customersOverview.total_unknown_ids,
}
