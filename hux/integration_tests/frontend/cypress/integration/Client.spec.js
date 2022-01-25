import route from "../support/routes.js"
import selector from "../support/selectors.js"

describe("Client", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.home)
  })

  it("should have the client panel show up", () => {
    cy.get(selector.client.clientDropdown).click()
    cy.get(selector.client.clientPanelOpen).click()
    cy.get(selector.client.clientHeader).contains(
      "Get started and access your clients’ Hux journey!",
    )
    cy.get(selector.client.clientHeader).contains("Client projects")
    cy.get(selector.client.clientLists).should("exist")
    cy.get(selector.client.client).its("length").should("gt", 0)
  })
})
