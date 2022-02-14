import faker from "faker"

export const domainData = () => {
  return {
    sent: Array.from({ length: 20 }, domain),
    open_Rate: Array.from({ length: 20 }, domain),
    delivered_rate: Array.from({ length: 20 }, domain),
    click_rate: Array.from({ length: 20 }, domain),
    unsubscribe_rate: Array.from({ length: 20 }, domain),
    complaints_rate: Array.from({ length: 20 }, domain),
  }
}

const domain = () => {
  return {
    domain_1: faker.datatype.number({ min: 1000, max: 100000 }),
    date: faker.date.between("2021-08-01", "2021-12-31"),
  }
}

export default domainData
