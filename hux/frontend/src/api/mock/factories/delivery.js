import faker from "faker"

export default {
  size: () => faker.datatype.number({ min: 1000, max: 100000 }),
  status: "Delivered",
  update_time: () => faker.date.recent(),
}