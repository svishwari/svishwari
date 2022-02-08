import faker from "faker"
import AllLogos from "../../../stories/logos/Logos.js"

export default {
  id: (index) => `${index + 1}`,
  type: () => AllLogos[faker.datatype.number({ min: 0, max: AllLogos.length })],
  name: (index) => `My client ${index + 1}`,
  description: (index) => `Client ${index + 1} description`,
  icon: () => AllLogos[faker.datatype.number({ min: 0, max: 20 })],
  url: (index) => `URL_Link ${index + 1}`,
  access_level: () => faker.random.arrayElement(["viewer", "admin", "editor"]),
  created_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  updated_by: () => faker.fake("{{name.firstName}} {{name.lastName}}"),
  create_time: () => faker.date.recent(),
  update_time: () => faker.date.recent(),
}
