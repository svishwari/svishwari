import route from "../../support/routes"
import selector from "../../support/selectors"

describe("Orchestration > Audiences", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.audiences)
  })

  it("should be able to check audience filters", () => {
    // should navigate to audiences
    cy.location("pathname").should("eq", route.audiences)

    //open filter drawer and attributes dropdown
    cy.get(selector.audience.audienceFilterToggle).click()
    cy.get(selector.audience.audienceFilters).contains("Attributes").click()

    //verify if most checkboxes are present and click on them
    cy.get(selector.audience.audienceFilters)
      .contains("My favorites only")
      .click()
    cy.get(selector.audience.audienceFilters).contains("ve worked on").click()
    cy.get(selector.audience.audienceFilters).contains("Attributes").click()
    cy.get(selector.audience.audienceFilters).contains("unsubscribe").click()
    cy.get(selector.audience.audienceFilters)
      .contains("Propensity to purchase")
      .click()
    cy.get(selector.audience.audienceFilters).contains("Age").click()
    cy.get(selector.audience.audienceFilters).contains("Email").click()
    cy.get(selector.audience.audienceFilters).contains("Gender").click()
    cy.get(selector.audience.audienceFilters).contains("Country").click()
    cy.get(selector.audience.audienceFilters).contains("State").click()
    cy.get(selector.audience.audienceFilters).contains("City").click()
    cy.get(selector.audience.audienceFilters).contains("Zip").click()
    cy.get(selector.audience.audienceFilters).contains("Filter (11)")

    //clear all checkboxes and close the drawer
    cy.get(selector.audience.audienceFilters).contains("Clear").click()
    cy.get(selector.audience.audienceFilters).contains("Filter")
    cy.get(selector.audience.audienceFilters)
      .contains("Filter (11)")
      .should("not.exist")

    cy.get(selector.audience.audienceFilters).contains("Close").click()
  })
})
