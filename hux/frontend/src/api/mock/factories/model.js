import faker from "faker"

export default {
  description: "Propensity of a customer unsubscribing to emails.",
  fulcrum_date: () => faker.date.past(),
  last_trained: () => faker.date.recent(),
  latest_version: "0.0.2",
  lookback_window: 365,
  name: "Propensity to Unsubscribe",
  owner: () => `${faker.name.firstName()} ${faker.name.lastName()}`,
  past_version_count: 0,
  prediction_window: 60,
  status: "pending",
  type: "unsubscribe",
}
