export default function (server) {
  // seed destinations
  server.create("destination")
  server.create("destination", {
    name: "Salesforce Marketing Cloud",
    type: "salesforce",
  })
}
