import faker from "faker"

export const genderSpendData = () => {
  return Array.from({ length: 238 }, spend)
}

const spend = () => {
  return {
    known_ids: `${faker.datatype.number({ min: 101982, max: 155851 })}`,
    unique_hux_ids:`${faker.datatype.number({ min: 101982, max: 155851 })}`,
    date: faker.date.between("2021-01-01", "2021-08-18"),
    anonymous_ids: 0
  }
}
