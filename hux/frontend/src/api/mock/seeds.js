export default function (server) {
  // seed destinations
  server.create("destination")
  server.create("destination", {
    name: "Salesforce Marketing Cloud",
    type: "salesforce",
  })
  server.create("destination", {
    name: "Adobe Experience",
    type: "adobe-experience",
    is_enabled: false,
  })
  server.create("destination", {
    name: "Google Ads",
    type: "google-ads",
    is_enabled: false,
  })
  server.create("destination", {
    name: "Twilio",
    type: "twilio",
    is_enabled: false,
  })
  server.create("destination", {
    name: "Tableau",
    type: "tableau",
    is_enabled: false,
  })
}
