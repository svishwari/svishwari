import faker from "faker"

export const driftData = () => {
  return Array.from({ length: 4 }, drift)
}

const drift = () => {
  return {
    drift: `${faker.datatype.number({ min: 216, max: 482 })}`,
    run_date: faker.date.between("2021-01-01", "2021-01-04"),
  }
}
