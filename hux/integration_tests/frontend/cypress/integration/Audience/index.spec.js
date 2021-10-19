import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Tests Audience", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to navigate to Audiences", () => {
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)

    //click on engagement on side nav bar and route in engagement screen
    cy.get(selector.audiences).click()
    cy.location("pathname").should("eq", route.audiences)
  })

  // Verifying the table columns names of the Engagement table
  it("verify the columns of the audiences list", () => {
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
  })

  it("should be able to view Audiences List", () => {
    cy.get(selector.audience.audiencelist).its("length").should("be.gt", 0)
  })

  it("check if menu options are working", () => {
    cy.get(selector.audience.audiencenameclick)
      .eq(2)
      .find("button")
      .eq(1)
      .click({ force: true })
    cy.get(".v-menu__content").should("exist")
  })

  it("check if favourite option is working", () => {
    cy.get(selector.audience.audiencenameclick)
      .eq(2)
      .find("button")
      .eq(0)
      .click({ force: true })
    cy.get(selector.audience.audiencenameclick)
      .eq(2)
      .find("button")
      .eq(0)
      .should("have.class", "mr-3 fixed-icon")
  })
})
