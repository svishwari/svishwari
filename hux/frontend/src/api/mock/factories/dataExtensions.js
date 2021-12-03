import faker from "faker"

const dataExtensionsMock = {
  name: () => faker.name.firstName(),
  data_extension_id() {
    return faker.datatype.uuid()
  },
  create_time: faker.date.past(),
}
export default dataExtensionsMock
