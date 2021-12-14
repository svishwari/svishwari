import faker from "faker"

const modelFeatures = (modelId = 1) => {
  return {
    name: "8to12m-ITEMEXTCOST-sum",
    created_by: faker.fake("{{name.firstName}} {{name.lastName}}"),
    score: faker.datatype.float({ min: 0, max: 1, precision: 0.001 }),
    description: `Model feature for ${faker.address.state()}`,
    popularity: faker.datatype.number({ min: 1, max: 10 }),
    feature_service: "ltv",
    version: faker.system.semver(),
    data_source: "Ecommerce",
    status: faker.random.arrayElement(["Active", "Delivering", "Stopped"]),
    id: modelId,
  }
}

const mockModelFeature = (modelId = 1, num = 43) => {
  return Array.from({ length: num }, () => modelFeatures(modelId))
}

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
  category: () =>
    faker.random.arrayElement(["Web", "Salesforecasting", "Email", "TrustiId"]),
  description: "Propensity of a customer unsubscribing to emails.",
  fulcrum_date: () => faker.date.past(),
  last_trained: () => faker.date.recent(),
  latest_version: "0.0.2",
  lookback_window: 365,
  name: "Propensity to Unsubscribe",
  owner: () => `${faker.name.firstName()} ${faker.name.lastName()}`,
  past_version_count: 0,
  prediction_window: 60,
  status: () =>
    faker.random.arrayElement([
      "Active",
      "Requested",
      "Pending",
      "Inactive",
      "Informational",
    ]),
  type: () =>
    faker.random.arrayElement(["Classification", "Unknown", "Regression"]),
  version_history: () => mockVersionHistory(5),
  model_feature: (index) => mockModelFeature(index + 1),
}
