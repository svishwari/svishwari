import faker from "faker"
import { customersOverview } from "./customers"

/**
 * Identity resolution data feed last run / waterfall report schema
 */
export const idrDataFeedReport = {
  pinning: {
    new_company_ids: 1,
    filename: "Input.csv",
    address_id_match: 1,
    new_household_ids: 1,
    db_reads: 1,
    company_id_match: 1,
    db_writes: 1,
    new_address_ids: 1,
    output_records: 2,
    empty_records: 0,
    household_id_match: 1,
    input_records: 2,
    individual_id_match: 1,
    pinning_timestamp: "2021-08-03T20:35:26.103Z",
    process_time: 6.43,
    new_individual_ids: 1,
  },
  stitched: {
    stitched_timestamp: "2021-08-03T20:35:26.103Z",
    records_source: "Input waterfall",
    merge_rate: 0,
    match_rate: 0.6606,
    digital_ids_merged: 6,
    digital_ids_added: 3,
  },
}

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
export const idrOverview = (state = "default") => {
  const defaultValues = [
    customersOverview.match_rate,
    customersOverview.total_household_ids,
    customersOverview.total_individual_ids,
    customersOverview.total_known_ids,
    customersOverview.total_records,
    customersOverview.total_unique_ids,
    customersOverview.total_unknown_ids,
  ]

  const nullValues = Array.from(Array(3), () => null)

  let values = defaultValues

  if (state === "unavailable") values = nullValues

  return {
    match_rate: values[0],
    total_household_ids: values[1],
    total_individual_ids: values[2],
    total_known_ids: values[3],
    total_records: values[4],
    total_unique_ids: values[5],
    total_unknown_ids: values[6],
  }
}
