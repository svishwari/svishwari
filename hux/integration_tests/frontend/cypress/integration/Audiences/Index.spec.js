import route from "../../support/routes"
import selector from "../../support/selectors"

describe("Orchestration > Audiences", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.audiences)
  })

  it("should be able to manage audiences", () => {
    // should navigate to audiences
    cy.location("pathname").should("eq", route.audiences)

    // should be able to view table of audiences
    cy.get(selector.audience.audiencelist).its("length").should("be.gt", 0)

    // should verify the columns of the audiences table
    const tableHeaders = [
      "Audience name",
      "Status",
      "Size",
      "Destinations",
      "Last delivered",
      "Last updated",
      "Last updated by",
      "Created",
      "Created by",
    ]

    cy.get(selector.audience.list.audienceTable)
      .find(selector.audience.list.audienceTableHeaders)
      .children()
      .each(($elm, i) => {
        expect($elm.text()).equal(tableHeaders[i])
      })

    // should check if audience menu options are working
    cy.get(selector.audience.audiencenameclick)
      .eq(0)
      .find("button")
      .eq(1)
      .click({ force: true })
    cy.get(".v-menu__content").should("exist")

    // should validate favourite an audience option is working
    cy.get(selector.audience.audiencenameclick)
      .eq(0)
      .find("button")
      .eq(0)
      .click({ force: true })
    cy.get(selector.audience.audiencenameclick)
      .eq(0)
      .find("button")
      .eq(0)
      .should("have.class", "mr-3 fixed-icon")
  })

  it("should delete the created audience", () => {
    // delete created audience
    cy.location("pathname").should("eq", route.audiences)
    cy.get(selector.audience.audiencelist).its("length").should("be.gt", 0)
    cy.get(selector.audience.audiencenameclick)
      .eq(0)
      .find("button")
      .eq(1)
      .click({ force: true })
    cy.get(".v-menu__content").should("exist")

    cy.contains("Delete audience").eq(0).click()

    cy.get(selector.audience.removeAudience)
      .get("button")
      .contains("Yes, delete it")
      .eq(0)
      .click()
  })
})
