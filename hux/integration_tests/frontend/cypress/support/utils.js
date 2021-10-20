import faker from "faker"

// function to create random name
export const randomName = () => {
  let randomName = faker.name.findName()
  return randomName
}
