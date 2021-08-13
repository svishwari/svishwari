import faker from "faker"

export default {
  id: `${faker.datatype.number({ min: 1, max: 10 })}`,
  lookback_window: 365,
  prediction_window: 60,
  description: "Predict the lifetime value of a customer.",
  version: "21.7.30",
  owner: () => `${faker.name.firstName()} ${faker.name.lastName()}`,
  name: "Lifetime Value",
  status: faker.random.arrayElement(["Active", "Delivering", "Stopped"]),
  trained_date: faker.date.recent(),
  fulcrum_date: faker.date.past(),
}
