// import { Response } from "miragejs"
// import { STATUS_CODES } from "http"

// const HTTPStatus = Object.keys(STATUS_CODES).reduce((ret, key) => {
//   ret[STATUS_CODES[key]] = key
//   return ret
// }, {})

export const routes = (server) => {
  // server.get("/ok", (schema) => {
  //   return new Response(HTTPStatus["OK"])
  // })

  server.get("/destinations", (schema) => {
    return schema.destinations.all().models
  })
}
