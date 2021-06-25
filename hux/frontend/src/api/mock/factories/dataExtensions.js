import faker from "faker"

const dataExtensionsMock = {
  name: () => faker.name.firstName(),
  data_extension_id() {
    return faker.datatype.uuid()
  },
}
export default dataExtensionsMock
