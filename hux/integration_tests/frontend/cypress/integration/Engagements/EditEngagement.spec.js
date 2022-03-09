import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Orchestration > Engagement > Edit Engagement", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.engagements)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)
  })

  it("should be able to modify an existing engagement", () => {
    cy.location("pathname").should("eq", route.engagements)

    cy.get(".menu-cell-wrapper")
      .eq(0)
      .find(".mdi-dots-vertical")
      .invoke("attr", "aria-expanded", "true")
      .click({ force: true })

    cy.contains("Edit engagement").click()
    cy.contains("Yes, edit").click()
    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)

    cy.location().should((loc) => {
      expect(loc.pathname.toString()).to.contain("/update")
    })

    // Edit engagement description
    cy.get(selector.engagement.enagagementDescription)
      .eq(0)
      .type(`E2E test edited engagement`)

    cy.contains("Update").click()
    cy.contains("Yes, edit")
  })
})
