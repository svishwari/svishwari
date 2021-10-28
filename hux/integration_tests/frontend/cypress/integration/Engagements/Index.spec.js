import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Orchestration > Engagements", () => {
  beforeEach(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
    cy.visit(route.engagements)
  })
  it("should be able to navigate to Engagements", () => {
    cy.location("pathname").should("eq", route.engagements)
  })

  // Verifying the table columns names of the Engagement table
  it("verify the columns of the engagement list", () => {
    const tableHeaders = [
      "Engagement name",
      "Audiences",
      "Destinations",
      "Status",
      "Last delivered",
      "Delivery schedule",
      "Last updated",
      "Last updated by",
      "Created",
      "Created by",
    ]

    cy.get(selector.engagement.list.engagementTable)
      .find(selector.engagement.list.engagementTableHeaders)
      .children()
      .each(($elm, i) => {
        expect($elm.text()).equal(tableHeaders[i])
      })
  })

  // Verifying the expand feature of the table.
  it("should be able to expand the last engagement", () => {
    cy.get(selector.engagement.list.engagementTable)
      .get(selector.engagement.list.engagementTableExpand)
      .last()
      .scrollIntoView()
    cy.get(selector.engagement.list.engagementTable)
      .get(selector.engagement.list.engagementTableExpand)
      .last()
      .click()
  })

  // Verifying the hover of the last delivered column of the audience table.
  it("should have hover on the last delivered column of audience table", () => {
    cy.get(selector.engagement.list.engagementTable)
      .get(selector.engagement.list.engagementTableExpand)
      .last()
      .click()
    cy.get(selector.engagement.list.engagementTable)
      .find(selector.engagement.list.audienceTable)
      .scrollIntoView({
        easing: "linear",
      })
    cy.get(selector.engagement.list.engagementTable)
      .find(selector.engagement.list.audienceTable)
      .find(selector.engagement.list.lastDeliveredColumn)
      .first()
      .scrollIntoView({ easing: "linear" })
      .trigger("mouseover", {
        force: true,
        eventConstructor: "MouseEvent",
      })
  })

  // Verifying the expand feature of the audience table.
  it("should have ability to expand the destinations under an audience table", () => {
    cy.get(selector.engagement.list.engagementTable)
      .get(selector.engagement.list.engagementTableExpand)
      .last()
      .click()
    cy.get(selector.engagement.list.engagementTable)
      .find(selector.engagement.list.audienceTable)
      .find(selector.engagement.list.audienceTableExpand)
      .first()
      .click()
  })
})
