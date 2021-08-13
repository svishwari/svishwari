import faker from "faker"

const versionHistory = () => {
  return {
    lookback_window: 365,
    prediction_window: 60,
    description: "Predict the lifetime value of a customer.",
    version: faker.system.semver(),
    owner: () => `${faker.name.firstName()} ${faker.name.lastName()}`,
    name: "Lifetime Value",
    status: faker.random.arrayElement(["Active", "Delivering", "Stopped"]),
    trained_date: faker.date.recent(),
    fulcrum_date: faker.date.past(),
  }
}

const mockVersionHistory = (num = 3) => {
  return Array.from({ length: num }, versionHistory)
}

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
  status: "Pending",
  type: "unsubscribe",
  version_history: () => mockVersionHistory(5),
}
